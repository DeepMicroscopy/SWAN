<script setup lang="ts">
  import { ref } from 'vue';

  const showDynamicElement = ref(true);

</script>

<template>
  <div id="highlight-me" class="hand-wrapper">
    <v-img
      v-if="showDynamicElement"
      ref="hand-icon"
      alt="Hand Icon"
      class="hand"
      src="@/assets/hand_no_touching.svg"
    />
    <!--    <v-img alt="Hand Icon" class="hand_touching" src="@/assets/hand_with_touching.svg" />-->
  </div>

</template>

<style scoped lang="scss">

.hand-wrapper {
  position: relative;
  display: flex;
  //display: none;
  justify-content: center; /* Horizontale Zentrierung */
  align-items: center; /* Vertikale Zentrierung */
  height: 80vh; /* Beispiel: Ganze Viewport-Höhe */
}

.hand {
  z-index: 0;
  position: absolute;
  top: 35%;
  left: 55%;
  width: 100px;
  height: auto;
  animation: gesture 3s ease-in-out infinite;
  transform-origin: center;
}

.hand_touching {
  z-index: 1;
  position: absolute;
  top: 35%;
  left: 55%;
  width: 100px;
  height: auto;
  animation: touching_point 3s ease-in-out infinite;
  transform-origin: center;
}

@keyframes gesture {
  0% {
    transform: translate(0, 0) scale(1.5) rotate(-20deg);

  }

  10% {
    transform: translate(0, 10px) scale(1) rotate(-10deg);
    /* Touch down */
  }

  30% {
    transform: translate(0, 10px) scale(1) rotate(-10deg);
    /* Hold */
  }

  60% {
    transform: translate(80px, 10px) rotate(10deg);
    /* Slide right while held */
  }

  90% {
    transform: translate(80px, 0px) scale(1.5) rotate(0deg);
    /* Lift slightly up (release) */
  }

  100% {
    transform: translate(0, 0) scale(1.5) rotate(-20deg);
  }
}

@keyframes touching_point {
  0% {
    transform: translate(0, 0) scale(1.5) rotate(-20deg);
    opacity: 0;

  }

  10% {
    transform: translate(0, 10px) scale(1) rotate(-10deg);
    opacity: 1;
    /* Touch down */
  }

  30% {
    transform: translate(0, 10px) scale(1) rotate(-10deg);
    opacity: 1;
    /* Hold */
  }

  60% {
    transform: translate(80px, 10px) rotate(10deg);
    opacity: 1;
    /* Slide right while held */
  }

  90% {
    transform: translate(80px, 0px) scale(1.5) rotate(0deg);
    opacity: 0;
    /* Lift slightly up (release) */
  }

  100% {
    transform: translate(0, 0) scale(1.5) rotate(-20deg);
    opacity: 0;

  }
}
</style>
