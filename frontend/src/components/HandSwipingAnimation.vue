<script setup lang="ts">
  interface Props {
    vertical?: boolean
  }

  const props = withDefaults(defineProps<Props>(), {
    vertical: () => false,
  })
</script>

<template>
  <svg
    ref="hand-icon"
    class="hand-switch"
    :class="props.vertical ? 'hand-vertical' : 'hand-horizontal'"
    viewBox="0 0 267.11 338.92"
  >
    <path class="pointer" d="M133.82,46.57c0,18.46-14.97,33.43-33.43,33.43s-33.43-14.97-33.43-33.43,14.97-33.43,33.43-33.43,33.43,14.97,33.43,33.43Z" />
    <g>
      <path class="hand-area" d="M240.94,165.9c-.93-37.39-15.91-42.81-25.88-44.09-9.32-1.2-17.07,6.47-17.07,6.47,0-9.01-7.4-22.19-19.91-22.28-13.85-.1-18.36,10.76-18.36,10.76,0,0-.65-17.47-17.49-18.54-10.52-.67-19.22,7.66-19.22,7.66l-.46-39.53c-.1-11.02-9.12-19.88-20.14-19.78h0c-11.02.1-19.88,9.12-19.78,20.14l3.18,119.15c.11,4.48-5.48,6.59-8.36,3.15-3.84-4.58-8.83-11.07-14.7-19.92-24.06-36.31-60.98-22.65-41.78,18.57,20.46,43.93,51.5,134.08,69.1,133.92h117.37c46.78,0,33.51-155.68,33.51-155.68Z" />
      <line
        class="hand-lines"
        x1="159.66"
        x2="160.2"
        y1="115.04"
        y2="163.6"
      />
      <line
        class="hand-lines"
        x1="197.99"
        x2="198.43"
        y1="128.51"
        y2="156.68"
      />
      <line
        class="hand-lines"
        x1="122.55"
        x2="123.72"
        y1="67.64"
        y2="170.76"
      />
    </g>
  </svg>
</template>

<style scoped lang="scss">
svg.hand-switch {
  .pointer {
    fill: #111;
    stroke-width: 5px;
    stroke: #eee;
  }

  .hand-area {
    fill: #eee;
  }

  .hand-area, .hand-lines {
    stroke: #000;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-width: 6px;
  }
}

.hand-switch {
  z-index: 0;
  position: absolute;
  width: 100px;
  height: 128px;
  margin-top: 64px;
  transform-origin: center;

  &.hand-horizontal {
    animation: gesture-left-right 4s ease-in-out infinite alternate;

    .pointer {
      animation: gesture-touch-horizontal 4s infinite alternate;
    }
  }

  &.hand-vertical {
    animation: gesture-up-down 4s ease-in-out infinite alternate;

    .pointer {
      animation: gesture-touch-vertical 4s infinite alternate;
    }
  }
}

@keyframes gesture-left-right {
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

@keyframes gesture-touch-horizontal {
  0%, 25% {
    opacity: 0;
  }

  30%, 70% {
    opacity: 1;
  }

  75%, 100% {
    opacity: 0;
  }
}

@keyframes gesture-touch-vertical {
  0%, 25% {
    opacity: 0;
  }

  30%, 70% {
    opacity: 1;
  }

  75%, 100% {
    opacity: 0;
  }
}
</style>
