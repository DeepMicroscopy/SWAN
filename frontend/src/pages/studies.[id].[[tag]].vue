<route lang="yaml">
meta:
  layout: swipe
</route>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { Card, SwipeEvent } from '@/components/CardSwiper.vue';
  import { useRoute } from 'vue-router';
  import client from '@/client.ts';

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

  const handleSwipe = (event: SwipeEvent) => {
    console.log(`card "${event.card.index}" swiped ${event.direction}`)

    client.POST('/v1/classify/', {
      body: {
        study: study.id,
        choice: event.direction,
        index: event.card.index,
      },
    })
      .then(response => console.log(response.data))
      .catch(error => console.log(error))
  }
</script>

<template>
  <CardSwiper
    :cards="cards"
    :index="index"
    :labels="study.ui.labels"
    :title="study.title"
    @swiped="handleSwipe"
  />
</template>
