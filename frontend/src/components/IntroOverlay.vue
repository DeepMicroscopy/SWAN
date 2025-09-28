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

  const showUpDown = ref(false);
</script>


<template>
  <div v-if="props.isVisible" class="overlay">
    <HandSwipingAnimation :vertical="showUpDown" />

    <div class="overlay-content">
      <div v-if="!showUpDown" id="left-decision">
        <p>Swipe left or right to classify the image.</p>
        <v-btn class="mt-3" color="pink-accent-4" size="small" @click="showUpDown = !showUpDown">Next</v-btn>
      </div>

      <div v-if="showUpDown" id="right-decision">
        <p>In this study you can also swipe up or down to classify the image.</p>
        <v-btn class="mt-3" color="pink-accent-4" size="small" @click="close">close</v-btn>
      </div>
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
  padding: 10px;
  margin-top: 66vh;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 20vh;
  color: #4A148C;
  background: #F3E5F5;
  text-align: center;
}

</style>
