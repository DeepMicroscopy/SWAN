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
            class="card-item elevation-8"
            :class="{ 'card-swiping': i === 0 && isSwiping }"
          >
            <div class="image-container" @wheel.prevent="handleMouseWheel">
              <v-img
                :alt="card.title"
                class="image-zoom"
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

    <v-container class="pt-2" width="auto">
      <v-progress-linear
        class="progress-bar"
        color="green"
        :model-value="progress"
        rounded
      />

      <v-toolbar
        class="pa-2"
        color="rgba(0,0,0,0.5)"
        density="compact"
        rounded
      >
        <v-btn
          color="white"
          :disabled="currentIndex === 0"
          icon="mdi-arrow-left"
          @click="backward"
        />

        <v-spacer />

        <p>{{ props.title }}</p>

        <v-btn
          color="white"
          icon="mdi-help-circle"
          @click="showHelp = true"
        />

        <v-spacer />

        <v-btn
          color="white"
          :disabled="!store.loggedIn"
          icon="mdi-close"
          @click="close"
        />
      </v-toolbar>
    </v-container>

    <v-dialog v-model="showHelp" width="auto">
      <v-card>
        <v-card-title class="text-h5">
          <v-icon class="mr-2">mdi-help-circle</v-icon>

          Help
        </v-card-title>

        <v-card-text>
          <v-list>
            <v-list-subheader>User Controls</v-list-subheader>

            <v-list-subheader inset>Swipe or Drag</v-list-subheader>
            <v-list-item
              v-if="props.labels.up"
              prepend-icon="mdi-arrow-up"
              :subtitle="`Classify as ${props.labels.up.text}`"
              title="Swipe Up"
            />
            <v-list-item
              v-if="props.labels.down"
              prepend-icon="mdi-arrow-down"
              :subtitle="`Classify as ${props.labels.down.text}`"
              title="Swipe Down"
            />
            <v-list-item
              prepend-icon="mdi-arrow-left"
              :subtitle="`Classify as ${props.labels.left.text}`"
              title="Swipe Left"
            />
            <v-list-item
              prepend-icon="mdi-arrow-right"
              :subtitle="`Classify as ${props.labels.right.text}`"
              title="Swipe Right"
            />

            <v-divider />

            <v-list-subheader inset>Inspect</v-list-subheader>
            <v-list-item
              prepend-icon="mdi-magnify"
              subtitle="Pinch or Mouse-Wheel"
              title="Zoom"
            />
            <v-list-item
              prepend-icon="mdi-magnify-expand"
              subtitle="Double-Tap or -Click"
              title="Reset"
            />
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="showHelp = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router';
  import type { UiLabel } from '@/api.ts';
  import { useAppStore } from '@/stores/app.ts';

  const router = useRouter()
  const store = useAppStore()

  // TODO
  // - dragging should be scaled to the zoom factor
  // - move threshold and position to user-settings
  // - also add image-rendering to some settings
  // - add intro

  // in ms
  const thresholdSwipe = 100
  const thresholdDoubleTap = 500

  export interface Card {
    index: number
    image: string
    title?: string
    description?: string
  }

  interface SwipeDirection {
    direction: 'up' | 'down' | 'left' | 'right'
    action: string
    color: string
    icon: string
  }

  export interface SwipeEvent {
    card: Card
    direction: 'up' | 'down' | 'left' | 'right'
  }

  interface Props {
    title?: string
    cards?: Card[]
    index?: number
    labels?: UiLabel
  }

  const props = withDefaults(defineProps<Props>(), {
    title: () => 'n/a',
    cards: () => [],
    index: () => -1,
    labels: () => ({
      'left': {
        'text': 'n/a',
      },
      'right': {
        'text': 'n/a',
      },
      'up': {
        'text': 'n/a',
      },
      'down': {
        'text': 'n/a',
      },
    } as UiLabel),
  })

  const emit = defineEmits<{
    swiped: [event: SwipeEvent]
  }>()

  const currentIndex = ref(props.index)
  const showHelp = ref(false)

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

  // data holder
  const swipeDirections: Record<string, SwipeDirection> = {
    up: {
      direction: 'up',
      action: props.labels.up?.text ?? 'n/a',
      color: props.labels.up?.color ?? 'white',
      icon: props.labels.up?.icon ?? 'mdi-arrow-up-bold',
    },
    down: {
      direction: 'down',
      action: props.labels.down?.text ?? 'n/a',
      color: props.labels.down?.color ?? 'white',
      icon: props.labels.down?.icon ?? 'mdi-arrow-down-bold',
    },
    left: {
      direction: 'left',
      action: props.labels.left.text,
      color: props.labels.left?.color ?? 'white',
      icon: props.labels.left?.icon ?? 'mdi-arrow-left-bold',
    },
    right: {
      direction: 'right',
      action: props.labels.right.text,
      color: props.labels.right?.color ?? 'white',
      icon: props.labels.right?.icon ?? 'mdi-arrow-right-bold',
    },
  }

  // Computed
  const visibleCards = computed(() => {
    return props.cards.slice(currentIndex.value, currentIndex.value + 2)
  })

  const progress = computed(() => {
    return 100 * (currentIndex.value / props.cards.length)
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
        opacity: 1 - Math.abs(deltaX) / 1000 - Math.abs(deltaY) / 1000,
      }
    }

    return {
      transform: baseTransform,
      opacity: 1 - index * 0.2,
    }
  }

  const getImageStyle = () => {
    return {
      transform: `scale(${imageZoom.value}) translate(${imageX.value}px, ${imageY.value}px)`,
      transformOrigin: 'center center',
      transition: isDragging.value ? 'none' : 'transform 0.3s ease',
    }
  }

  const forward = () => {
    currentIndex.value++

    // unclear if needed
    zoomReset()
  }

  const backward = () => {
    currentIndex.value--

    // unclear if needed
    zoomReset()
  }

  const close = () => {
    router.back()
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
    swipeStart(e)
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

  const swipeMove = (e: MouseEvent | Touch) => {
    if (!isSwiping.value) return

    currentX.value = e.clientX
    currentY.value = e.clientY

    const delta = { x: currentX.value - startX.value, y: currentY.value - startY.value }

    const threshold = 50;

    if (Math.abs(delta.x) > threshold || Math.abs(delta.y) > threshold) {
      if (Math.abs(delta.x) > Math.abs(delta.y)) {
        swipeDirection.value = delta.x > 0 ? 'right' : 'left'
      } else {
        const isDown = delta.y > 0

        if (props.labels.up && !isDown) {
          swipeDirection.value = 'up'
        } else if (props.labels.down && isDown) {
          swipeDirection.value = 'down'
        } else if (delta.x > threshold) {
          swipeDirection.value = delta.x > 0 ? 'right' : 'left'
        } else {
          swipeDirection.value = null
        }
      }
    } else {
      swipeDirection.value = null
    }
  }

  const handleSwipeEnd = () => {
    if ((Date.now() - lastTap.value) < thresholdDoubleTap) {
      zoomReset()
      return
    } else {
      lastTap.value = Date.now()
    }

    if (!isSwiping.value) return

    const delta = { x: currentX.value - startX.value, y: currentY.value - startY.value }

    if (Math.abs(delta.x) > thresholdSwipe || Math.abs(delta.y) > thresholdSwipe) {
      let direction

      if (Math.abs(delta.x) > Math.abs(delta.y)) {
        direction = delta.x > 0 ? 'right' : 'left'
      } else {
        direction = delta.y > 0 ? 'down' : 'up'
      }

      if (direction === 'down' && !props.labels.down || direction === 'up' && !props.labels.up) {
        if (delta.x > thresholdSwipe) {
          direction = delta.x > 0 ? 'right' : 'left'
        } else {
          swipeReset()
          return
        }
      }

      emit('swiped', <SwipeEvent>{
        card: props.cards[currentIndex.value],
        direction,
      })

      forward()
    }

    swipeReset();
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
    imageZoom.value = Math.max(1, Math.min(3, imageZoom.value + (dir ? -0.1 : 0.1)))

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
</style>
