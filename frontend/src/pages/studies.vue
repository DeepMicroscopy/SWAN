<!-- Beispiel: CardStackView.vue -->
<template>
  <CardSwiper
    :cards="cards"
    :index="index"
    @swiped="handleSwipe"
  />
</template>

<route lang="yaml">
meta:
  layout: swipe
</route>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { Study } from '@/api.ts';
  import type { Card, SwipeEvent } from '@/components/CardSwiper.vue';
  import { default as axios } from 'axios';
  import { useRoute } from 'vue-router';
  const route = useRoute()

  const study = await axios.get<Study>(`/v1/studies/${route.params?.id}`);
  const lastIndex = await axios.get<number>(`/v1/studies/${route.params?.id}/index`);

  const result: Card[] = []
  for (let index = 0; index < study.data.length; index++) {
    result.push({ index, image: `/v1/studies/${study.data.id}/${index}/` })
  }

  const cards = ref<Card[]>(result);
  const index = ref(lastIndex.data+1);

  const handleSwipe = (event: SwipeEvent) => {
    console.log(`card "${event.card.index}" swiped ${event.direction}`)
    axios.post(`/v1/classify/`, {
      'study': study.data.id,
      'choice': event.direction,
      'index': event.card.index,
    }).then(response => console.log(response.data))
      .catch(error => {
        console.log(error)
      })
  }
</script>
