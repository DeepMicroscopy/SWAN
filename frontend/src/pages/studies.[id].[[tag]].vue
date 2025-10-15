<route lang="yaml">
meta:
  layout: swipe
</route>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { Card, SwipeEvent } from '@/components/ImageSwiper.vue';
  import { useRoute } from 'vue-router';
  import client from '@/client.ts';
  import type { Education, UiLabel } from '@/api.ts';
  import { type ErrorData, getError, setError } from '@/util/fetch-errors.ts';
  import { useIntro } from '@/composables/useIntro.ts';

  const route = useRoute<'/studies.[id].[[tag]]'>();

  if ((route.params.tag?.length ?? 0) > 0) {
    document.cookie = `anonymous=${route.params.tag}; path=/; Secure`;
  }

  const fatalError = ref<ErrorData>(getError())
  const error = ref<ErrorData>(getError())
  const failed = ref(false)

  const showOverlay = ref(false);

  const { data: study, error: err, response } = await client.GET('/v1/studies/{id}/', { params: { path: { id: route.params.id } } });
  if (err) {
    setError(fatalError.value, err, response)
    failed.value = true
  }

  const result: Card[] = []
  for (let index = 0; index < study?.length; index++) {
    result.push({ index, image: `/v1/studies/${study.id}/${index}/` })
  }

  const cards = ref<Card[]>(result);
  const index = ref(study?.index + 1);
  const showDescription = ref(false)

  const decisionText = ref('')
  const decisionIcon = ref('mdi-checkbox-blank-off-outline')
  const showDecision = ref(false)

  const currentImage = ref('')
  const currentEducation = ref<Education>({} as Education)
  const showSolution = ref(false)

  const showAppreciation = ref(false)

  if (index.value === 0) {
    showDescription.value = true
  }

  const infoPromise = client.GET('/v1/auth/info/')

  watch(index, () => {
    if (index.value === cards.value.length) {
      showAppreciation.value = true
    }
  }, { immediate: true })

  const closeAppreciation = async () => {
    showAppreciation.value = false

    const { data: postponed, error: err, response } = await client.GET('/v1/studies/{id}/postponed/', { params: { path: { id: route.params.id } } })
    if (err) {
      setError(error.value, err, response)
      return
    }

    const result: Card[] = []

    for (const index of postponed.images) {
      result.push({ index, image: `/v1/studies/${study.id}/${index}/` })
    }

    cards.value = cards.value.concat(result)
  }

  const forward = (event: SwipeEvent) => {
    index.value++
    showDecision.value = false

    console.log(`card "${event.card.index}" swiped ${event.direction}`)

    client.POST('/v1/classify/', {
      body: {
        study: study.id,
        choice: event.direction,
        index: event.card.index,
      },
    })
      .then(result => {
        if (!result.response.ok) {
          setError(error.value, result.error, result.response)
          index.value--
          return
        }

        if (result.data?.education) {
          showSolution.value = true
          currentImage.value = cards.value[index.value - 1]?.image ?? ''
          currentEducation.value = result.data?.education
        }
      })
      .catch(error => {
        console.log('FORWARD ERROR', error)
        index.value--
      })
  }

  const backward = () => {
    index.value--

    client.GET('/v1/classify/{id}/{index}/', {
      params: {
        path: {
          id: study.id,
          index: index.value.toString(),
        },
      },
    })
      .then(result => {
        if (!result.response.ok) {
          setError(error.value, result.error, result.response)
          return
        }

        if (!result.data) return

        if (result.data.choice in study.ui.labels) {
          const label = study.ui.labels[result.data.choice as keyof UiLabel]

          showDecision.value = true
          decisionText.value = `${label?.text}`
          decisionIcon.value = label?.icon ?? getIcon(result.data.choice)
        }
      })
      .catch(error => console.log(error))
  }

  function getIcon (choice: string): string {
    return {
      up: 'mdi-arrow-up-bold',
      down: 'mdi-arrow-down-bold',
      left: 'mdi-arrow-left-bold',
      right: 'mdi-arrow-right-bold',
    }[choice] ?? 'mdi-checkbox-blank-off-outline'
  }

  const currentIntroGeneral = 1
  const currentIntroSwiping = 1

  const closeDescription = async () => {
    showDescription.value = false

    infoPromise.then(result => {
      if (!result.response.ok) {
        setError(error.value, result.error, result.response)
        return
      }

      const lastIntroGeneral = result.data?.intro_general ?? 0
      const lastIntroSwiping = result.data?.intro_swiping ?? 0
      if (lastIntroGeneral < currentIntroGeneral) {
        intro.drive()
      } else if (lastIntroSwiping < currentIntroSwiping) {
        showOverlay.value = true
      }
    })
  }

  const closeIntro = () => {
    showOverlay.value = true

    client.POST('/v1/auth/info/', {
      body: {
        intro_general: currentIntroGeneral,
      },
    })
  }

  const closeOverlay = () => {
    showOverlay.value = false

    client.POST('/v1/auth/info/', {
      body: {
        intro_swiping: currentIntroSwiping,
      },
    })
  }

  const intro = useIntro([
    {
      child: 'toolbar',
      ref: 'titleStudy',
      title: 'Title',
      description: 'Here you can see the title of the current study.',
    },
    {
      child: 'toolbar',
      ref: 'buttonHelp',
      title: 'Help',
      description: 'View a guide to the user controls.',
    },
    {
      child: 'toolbar',
      ref: 'buttonBack',
      title: 'Back',
      description: 'Navigate back to the previous image and decision point in the study.',
    },
    {
      child: 'toolbar',
      ref: 'progressBar',
      title: 'Progress',
      description: 'This indicates your progress through the current study.',
    },
    {
      child: 'toolbar',
      ref: 'buttonExit',
      title: 'Exit',
      description: 'Close the study and return to the overview page. Your progress will be saved.',
      onNext: closeIntro,
    },
  ])
</script>

<template>
  <v-container v-if="!failed">
    <ImageSwiper
      :cards="cards"
      :index="index"
      :labels="study.ui.labels"
      :title="study.title"
      @swiped="forward"
    />

    <PastDecision
      class="mb-6"
      :icon="decisionIcon"
      :show="showDecision"
      :text="decisionText"
      @close="showDecision = false"
    />

    <SwiperToolbar
      ref="toolbar"
      :index="index"
      :labels="study.ui.labels"
      :title="study.title"
      :total="cards.length"
      @back="backward"
    />
  </v-container>

  <StudySolution
    v-if="study.solution"
    :config="study.solution"
    :current="currentImage"
    :education="currentEducation"
    :show="showSolution"
    :study="study"
    @close="showSolution = false"
  />

  <StudyDescription :postpone="study.ui.postpone" :show="showDescription" :study="study" @close="closeDescription" />

  <StudyAppreciation :postpone="!!study.ui.postpone" :show="showAppreciation" :study="study" @close="closeAppreciation" />

  <FetchError
    class="mb-6"
    :code="error.code"
    :show="error.show"
    :text="error.text"
    @close="error.show = false"
  />

  <FetchError
    class="mb-6"
    :closable="false"
    :code="fatalError.code"
    :show="fatalError.show"
    :text="fatalError.text"
    :timeout="-1"
    @close="fatalError.show = false"
  />

  <IntroOverlay :is-visible="showOverlay" @close="closeOverlay" />
</template>

<style lang="scss">
.driver-popover {
  color: #4A148C;
  background-color: #F3E5F5;
}

.driver-popover-progress-text {
  color: #BA68C8;
}

.driver-popover-footer button {
  color: #F3E5F5;
  background-color: #c51162 !important;
  text-shadow: initial;
  height: 28px;
  min-width: 50px;
  padding: 0 12px;
  margin-left: 5px;
  border-radius: 4px;
  box-sizing: initial;
  letter-spacing: 0.09em;
  line-height: normal;
  font-weight: 500;
  font-size: 80%;
  text-transform: uppercase;
}
</style>
