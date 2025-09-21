<script setup lang="ts">
  import { defineEmits, defineProps } from 'vue';

  const props = defineProps({
    isVisible: {
      type: Boolean,
      required: true,
    },
  });

  const emits = defineEmits(['close']);

  const close = () => {
    emits('close');
  };
</script>


<template>
  <div v-if="isVisible" class="overlay">
    <div class="overlay-content">
      <slot />
      <v-btn @click="close">Schließen</v-btn>
    </div>
  </div>
</template>

<style scoped lang="scss">
.overlay {
  position: fixed; /* Über allem, fixiert auf der Seite */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* Transparenter schwarzer Hintergrund */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Stellt sicher, dass das Overlay über anderen Elementen liegt */
}

.overlay-content {
  //background: white;
  padding: 20px;
  //border-radius: 8px;
  //box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}
</style>
