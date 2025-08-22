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

  const route = useRoute<'/studies.[id].[[tag]]'>();

  if ((route.params.tag?.length ?? 0) > 0) {
    document.cookie = `anonymous=${route.params.tag}; path=/; Secure`;
  }

  const fatalError = ref<ErrorData>(getError())
  const error = ref<ErrorData>(getError())
  const failed = ref(false)

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
  const showStudy = ref(false)

  const decisionText = ref('')
  const decisionIcon = ref('mdi-checkbox-blank-off-outline')
  const showDecision = ref(false)

  const currentImage = ref('')
  const education = ref<Education>({} as Education)
  const showSolution = ref(false)

  if (index.value === 0) {
    showStudy.value = true
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
          currentImage.value = cards.value[index.value - 1]?.image ?? ''
          education.value = result.data?.education
          showSolution.value = true
        }
      })
      .catch(error => console.log(error))
  }

  function getIcon (choice: string):string {
    return {
      up: 'mdi-arrow-up-bold',
      down: 'mdi-arrow-down-bold',
      left: 'mdi-arrow-left-bold',
      right: 'mdi-arrow-right-bold',
    }[choice] ?? 'mdi-checkbox-blank-off-outline'
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
      :index="index"
      :labels="study.ui.labels"
      :title="study.title"
      :total="cards.length"
      @back="backward"
    />
  </v-container>

  <StudySolution
    v-if="study.educational"
    :current="currentImage"
    :education="education"
    :show="showSolution"
    :study="study"
    @close="showSolution = false"
  />

  <StudyDescription :show="showStudy" :study="study" @close="showStudy = false" />

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
</template>
