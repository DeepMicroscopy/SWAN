<!-- Beispiel: CardStackView.vue -->
<template>
  <CardSwiper
    :cards="cards"
    @swiped="handleSwipe"
  />
</template>

<route lang="yaml">
meta:
  layout: swipe
</route>

<script setup lang="ts">
  import { ref } from 'vue'
  import type { Card, SwipeEvent } from '@/components/CardSwiper.vue';

  const cards = ref<Card[]>([
    {
      id: '1',
      imageUrl: 'https://picsum.photos/200/300?random=1',
    },
    {
      id: '2',
      imageUrl: 'https://picsum.photos/300/300?random=2',
    },
    {
      id: '3',
      imageUrl: 'https://picsum.photos/300/200?random=3',
    },
    {
      id: '4',
      imageUrl: 'https://picsum.photos/1000/1000?random=4',
    },
  ])

  const handleSwipe = (event: SwipeEvent) => {
    console.log(`card "${event.card.id}" swiped ${event.direction}`)
  }
</script>
