<template>
  <v-container fluid>
    <div @touchmove.prevent>
      <v-fade-transition>
        <div
          v-if="swipeDirection"
          class="swipe-indicator"
          :class="`swipe-${swipeDirection}`"
        >
          <v-icon
            :color="getSwipeColor(swipeDirection)"
            size="64"
          >
            {{ getSwipeIcon(swipeDirection) }}
          </v-icon>
          <p class="swipe-text">{{ getSwipeText(swipeDirection) }}</p>
        </div>
      </v-fade-transition>

      <div class="cards-stack position-absolute">
        <div v-if="props.index === props.cards.length" class="absolute-center">
          <v-icon color="white" size="64">mdi-cancel</v-icon>

          <p class="mt-2">
            No more images
          </p>
        </div>

        <div
          v-for="(card, i) in visibleCards"
          :key="card.index"
          class="card-wrapper"
          :class="{ 'active-card': i === 0 }"
          :style="getCardStyle(i)"
          @dblclick="zoomReset"
          @mousedown.prevent="handleSwipeStartMouse"
          @mouseleave.prevent="handleSwipeEnd"
          @mousemove.prevent="handleSwipeMoveMouse"
          @mouseup.prevent="handleSwipeEnd"
          @touchend.prevent="handleSwipeEnd"
          @touchmove.prevent="handleSwipeMoveTouch"
          @touchstart.prevent="handleSwipeStartTouch"
        >
          <v-card
            class="card-item elevation-8 no-border-radius"
            :class="{ 'card-swiping': i === 0 && isSwiping }"
          >
            <div class="image-container" @wheel.prevent="handleMouseWheel">
              <v-img
                :alt="card.title"
                class="image-zoom"
                :class="props.ui.pixelated ? 'image-pixelated' : ''"
                :src="card.image"
                :style="getImageStyle()"
                @mousedown.prevent="handleStartMouse"
                @mouseleave.prevent="handleDragEnd"
                @mousemove.prevent="handleDragMoveMouse"
                @mouseup.prevent="handleDragEnd"
                @touchend.prevent="handleDragEnd"
                @touchmove.prevent="handleDragMoveTouch"
                @touchstart.prevent="handleDragStartTouch"
              />
            </div>
          </v-card>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue'
  import type { Direction, Ui, UiDirection } from '@/api.ts';
  import { useAppStore } from '@/stores/app.ts';

  // TODO
  // - dragging should be scaled to the zoom factor
  // - move threshold and position to user-settings
  // - also add image-rendering to some settings
  // - add intro

  // in ms
  const thresholdSwipe = 100
  const thresholdDoubleTap = 500

  const store = useAppStore()

  export interface Card {
    index: number
    image: string
    title?: string
    description?: string
  }

  interface SwipeDirection {
    direction: Direction
    action: string
    color: string
    icon: string
  }

  export interface SwipeEvent {
    card: Card
    direction: Direction
  }

  interface Props {
    study?: string
    title?: string
    cards?: Card[]
    index?: number
    ui?: Ui
  }

  const props = withDefaults(defineProps<Props>(), {
    study: () => 'n/a',
    title: () => 'n/a',
    cards: () => [],
    index: () => -1,
    ui: () => ({} as Ui),
  })

  const emit = defineEmits<{
    swiped: [event: SwipeEvent]
  }>()

  // Card swipe
  const isSwiping = ref(false)
  const swipeDirection = ref<string | null>(null)
  const startX = ref(0)
  const startY = ref(0)
  const currentX = ref(0)
  const currentY = ref(0)

  // Image drag
  const isDragging = ref(false)
  const imageX = ref(0)
  const imageY = ref(0)
  const imageStartX = ref(0)
  const imageStartY = ref(0)

  // Image zoom
  const isZooming = ref(false)
  const imageZoom = ref(1)
  const currentDistance = ref(0)
  const lastTap = ref(Date.now())

  function labelToDirection (direction: Direction, label: UiDirection | null): SwipeDirection {
    return {
      direction,
      action: label?.text ?? 'n/a',
      color: label?.color ?? 'white',
      icon: label?.icon ?? `mdi-arrow-${direction}-bold`,
    }
  }
  // data holder
  const swipeDirections: Record<string, SwipeDirection> = {
    up: labelToDirection('up', props.ui.labels.up),
    down: labelToDirection('down', props.ui.labels.down),
    left: labelToDirection('left', props.ui.labels.left),
    right: labelToDirection('right', props.ui.labels.right),
  }

  // Computed
  const visibleCards = computed(() => {
    return props.cards.slice(props.index, props.index + 2)
  })
  const imageScale = computed(() => {
    return (store.studySettings[props.study]?.imageZoom ?? props.ui.default_scale ?? 100) / 100
  })

  // Methods
  const getCardStyle = (index: number) => {
    const baseTransform = `translateZ(${-index * 10}px) scale(${1 - index * 0.05})`

    if (index === 0 && isSwiping.value) {
      const deltaX = currentX.value - startX.value
      const deltaY = currentY.value - startY.value
      const rotation = deltaX * 0.1

      return {
        transform: `${baseTransform} translateX(${deltaX}px) translateY(${deltaY}px) rotateZ(${rotation}deg)`,
        opacity: 1,
      }
    }

    return {
      transform: baseTransform,
      opacity: 1 - index * 0.5,
    }
  }

  const getImageStyle = () => {
    return {
      transform: `scale(${imageZoom.value * imageScale.value}) translate(${imageX.value}px, ${imageY.value}px)`,
      transformOrigin: 'center center',
      transition: isDragging.value ? 'none' : 'transform 0.3s ease',
    }
  }

  const getSwipeIcon = (direction: string) => {
    return swipeDirections[direction]?.icon || 'mdi-help'
  }

  const getSwipeColor = (direction: string) => {
    return swipeDirections[direction]?.color || 'primary'
  }

  const getSwipeText = (direction: string) => {
    return swipeDirections[direction]?.action || ''
  }

  // Swipe events
  const handleSwipeStartTouch = (e: TouchEvent) => {
    if (e.touches.length === 1) {
      swipeStart(e.touches[0]!)
    }
  }

  const handleSwipeStartMouse = (e: MouseEvent) => {
    if (e.button === 0) {
      swipeStart(e)
    }
  }

  const swipeStart = (e: MouseEvent | Touch) => {
    if (imageZoom.value !== 1) return

    isSwiping.value = true

    startX.value = currentX.value = e.clientX
    startY.value = currentY.value = e.clientY
  }

  const handleSwipeMoveTouch = (e: TouchEvent) => {
    if (e.touches.length === 1 && isSwiping.value) {
      swipeMove(e.touches[0]!)
    }
  }

  const handleSwipeMoveMouse = (e: MouseEvent) => {
    if (isSwiping.value) {
      swipeMove(e)
    }
  }

  function directionForDeltas (x: number, y: number): Direction|null {
    if (Math.abs(x) > thresholdSwipe || Math.abs(y) > thresholdSwipe) {
      if (Math.abs(x) > Math.abs(y)) {
        const isRight = x > 0

        if (props.ui.labels.left && !isRight) {
          return 'left'
        } else if (props.ui.labels.right && isRight) {
          return 'right'
        }
      } else {
        const isDown = y > 0

        if (props.ui.labels.up && !isDown) {
          return 'up'
        } else if (props.ui.labels.down && isDown) {
          return 'down'
        }
      }
    }

    return null
  }

  const swipeMove = (e: MouseEvent | Touch) => {
    if (!isSwiping.value) return

    currentX.value = e.clientX
    currentY.value = e.clientY

    swipeDirection.value = directionForDeltas(currentX.value - startX.value, currentY.value - startY.value)
  }

  const handleSwipeEnd = () => {
    if ((Date.now() - lastTap.value) < thresholdDoubleTap) {
      zoomReset()
      return
    } else {
      lastTap.value = Date.now()
    }

    if (!isSwiping.value) return

    const direction = directionForDeltas(currentX.value - startX.value, currentY.value - startY.value)

    if (direction !== null) {
      emit('swiped', <SwipeEvent>{
        card: props.cards[props.index],
        direction,
      })
    }

    swipeReset()
  }

  function swipeReset () {
    isSwiping.value = false

    swipeDirection.value = null

    currentX.value = startX.value
    currentY.value = startY.value
  }

  // Drag Events
  const handleDragStartTouch = (e: TouchEvent) => {
    if (e.touches.length === 1) {
      dragStart(e.touches[0]!)
    } else if (e.touches.length === 2) {
      zoomStart(e.touches)
    }
  }

  const handleStartMouse = (e: MouseEvent) => {
    dragStart(e)
  }

  const dragStart = (e: MouseEvent | Touch) => {
    if (imageZoom.value === 1) return

    isDragging.value = true

    imageStartX.value = e.clientX - imageX.value
    imageStartY.value = e.clientY - imageY.value
  }

  const handleDragMoveTouch = (e: TouchEvent) => {
    if (e.touches.length === 1 && isDragging.value) {
      dragMove(e.touches[0]!)
    } else if (e.touches.length === 2) {
      zoomMove(e.touches)
    }
  }

  const handleDragMoveMouse = (e: MouseEvent) => {
    if (isDragging.value) {
      dragMove(e)
    }
  }

  const dragMove = (e: MouseEvent | Touch) => {
    if (!isDragging.value) return

    imageX.value = e.clientX - imageStartX.value
    imageY.value = e.clientY - imageStartY.value
  }

  const handleDragEnd = () => {
    isDragging.value = false
    isZooming.value = false

    currentDistance.value = 0
  }

  // Zoom Events
  const handleMouseWheel = (e: WheelEvent) => {
    zoomChange(e.deltaY > 0)
  }

  const zoomStart = (touches: TouchList) => {
    isZooming.value = true

    currentDistance.value = distance(touches)
  }

  const zoomMove = (touches: TouchList) => {
    const delta = distance(touches)

    zoomChange(currentDistance.value > delta)

    currentDistance.value = delta
  }

  const zoomChange = (dir: boolean) => {
    imageZoom.value = Math.max(0.1, Math.min(3, imageZoom.value + (dir ? -0.1 : 0.1)))

    if (imageZoom.value === 1) {
      zoomReset()
    }
  }

  const zoomReset = () => {
    imageZoom.value = 1

    imageX.value = 0
    imageY.value = 0
  }

  const distance = (touches: TouchList) => {
    const [touch1, touch2] = touches;
    return Math.hypot(touch1!.clientX - touch2!.clientX, touch1!.clientY - touch2!.clientY);
  }
</script>

<style lang="scss" scoped>
.cards-stack {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
}

.card-wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  cursor: grab;

  &.active-card {
    z-index: 1;
  }
}

.card-item {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  transition: transform 0.3s ease, opacity 0.3s ease;

  &.card-swiping {
    transition: none;
  }
}

.image-container {
  height: 100%;
  overflow: hidden;
  position: relative;
  cursor: zoom-in;
}

.image-zoom {
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
  -webkit-user-drag: none;
}

.image-pixelated {
  image-rendering: pixelated;
}

.swipe-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  text-align: center;
  pointer-events: none;

  .swipe-text {
    margin-top: 8px;
    font-weight: bold;
    font-size: 1.2em;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  &.swipe-up {
    animation: bounce-up 0.6s ease infinite;
  }

  &.swipe-down {
    animation: bounce-down 0.6s ease infinite;
  }

  &.swipe-left {
    animation: bounce-left 0.6s ease infinite;
  }

  &.swipe-right {
    animation: bounce-right 0.6s ease infinite;
  }
}

@keyframes bounce-up {
  0%, 100% {
    transform: translate(-50%, -50%) translateY(0);
  }
  50% {
    transform: translate(-50%, -50%) translateY(-10px);
  }
}

@keyframes bounce-down {
  0%, 100% {
    transform: translate(-50%, -50%) translateY(0);
  }
  50% {
    transform: translate(-50%, -50%) translateY(10px);
  }
}

@keyframes bounce-left {
  0%, 100% {
    transform: translate(-50%, -50%) translateX(0);
  }
  50% {
    transform: translate(-50%, -50%) translateX(-10px);
  }
}

@keyframes bounce-right {
  0%, 100% {
    transform: translate(-50%, -50%) translateX(0);
  }
  50% {
    transform: translate(-50%, -50%) translateX(10px);
  }
}

.absolute-center {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  display: flex;
  flex-direction: column;

  justify-content: center;
  align-items: center;
}

.no-border-radius {
  border-radius: 0 !important;
}
</style>
