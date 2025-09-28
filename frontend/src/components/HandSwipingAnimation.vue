<script setup lang="ts">
  interface Props {
    vertical?: boolean
  }

  const props = withDefaults(defineProps<Props>(), {
    vertical: () => false,
  })
</script>

<template>
  <v-img
    ref="hand-icon"
    alt="Hand Icon"
    class="hand-switch"
    :class="props.vertical ? 'hand-vertical' : 'hand-horizontal'"
    src="@/assets/hand_no_touching.svg"
  />
</template>

<style scoped lang="scss">
.hand-switch {
  z-index: 0;
  position: absolute;
  width: 100px;
  height: 128px;
  margin-top: 64px;
  transform-origin: center;
}

.hand-switch.hand-horizontal {
  animation: gesture 3s ease-in-out infinite alternate;
}

.hand-switch.hand-vertical {
  animation: gesture-up-down 3s ease-in-out infinite alternate;
}

@keyframes gesture {
  0% {
    transform: translate(-50px, 0px) scale(1.5) rotate(-20deg);
  }

  10% {
    transform: translate(-50px, 0px) scale(1.5) rotate(-20deg);
  }

  30% {
    transform: translate(-50px, 10px) scale(1.0) rotate(-10deg);
    /* Hold */
  }

  70% {
    transform: translate(50px, 10px) scale(1.0) rotate(10deg);
    /* Slide */
  }

  90% {
    transform: translate(50px, 0px) scale(1.5) rotate(0deg);
    /* Lift */
  }

  100% {
    transform: translate(50px, 0px) scale(1.5) rotate(0deg);
  }
}

@keyframes gesture-up-down {
  0% {
    transform: translate(0px, -50px) scale(1.5) rotate(-20deg);
  }

  20% {
    transform: translate(0px, -50px) scale(1.5) rotate(-20deg);
  }

  30% {
    transform: translate(10px, -50px) scale(1.0) rotate(-10deg);
    /* Hold */
  }

  70% {
    transform: translate(10px, 50px) scale(1.0) rotate(10deg);
    /* Slide */
  }

  80% {
    transform: translate(0px, 50px) scale(1.5) rotate(0deg);
    /* Lift */
  }

  100% {
    transform: translate(0px, 50px) scale(1.5) rotate(0deg);
  }
}
</style>
