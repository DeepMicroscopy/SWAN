<route lang="yaml">
meta:
  layout: swipe
</route>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { Card, SwipeEvent } from '@/components/ImageSwiper.vue';
  import { useRoute } from 'vue-router';
  import client from '@/client.ts';
  import type { UiLabel } from '@/api.ts';

  const route = useRoute<'/studies.[id].[[tag]]'>();

  if ((route.params.tag?.length ?? 0) > 0) {
    document.cookie = `anonymous=${route.params.tag}; path=/; Secure`;
  }

  const { data: study, error } = await client.GET('/v1/studies/{id}/', { params: { path: { id: route.params.id } } });
  if (error) {
    throw error;
  }

  const result: Card[] = []
  for (let index = 0; index < study.length; index++) {
    result.push({ index, image: `/v1/studies/${study.id}/${index}/` })
  }

  const cards = ref<Card[]>(result);
  const index = ref(study.index + 1);
  const showStudy = ref(false)

  const decisionText = ref('')
  const decisionIcon = ref('mdi-checkbox-blank-off-outline')
  const showDecision = ref(false)

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
      .then(response => {
        console.log(response.data)
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
      .then(response => {
        if (!response.data) return

        if (response.data.choice in study.ui.labels) {
          const label = study.ui.labels[response.data.choice as keyof UiLabel]

          showDecision.value = true
          decisionText.value = `${label?.text}`
          decisionIcon.value = label?.icon ?? getIcon(response.data.choice)
        }
      })
      .catch(error => console.log(error))
  }
</script>

<template>
  <ImageSwiper
    :cards="cards"
    :index="index"
    :labels="study.ui.labels"
    :title="study.title"
    @swiped="forward"
  />

  <StudyDescription :show="showStudy" :study="study" @close="showStudy = false" />

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
</template>
