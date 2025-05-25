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
            size="64"
            :color="getSwipeColor(swipeDirection)"
          >
            {{ getSwipeIcon(swipeDirection) }}
          </v-icon>
          <p class="swipe-text">{{ getSwipeText(swipeDirection) }}</p>
        </div>
      </v-fade-transition>

      <div class="cards-stack position-absolute">
        <div
          v-for="(card, index) in visibleCards"
          :key="card.id"
          class="card-wrapper"
          :class="{ 'active-card': index === 0 }"
          :style="getCardStyle(index)"
          @touchstart.prevent="handleSwipeStartTouch"
          @touchmove.prevent="handleSwipeMoveTouch"
          @touchend.prevent="handleSwipeEnd"
          @mousedown.prevent="handleSwipeStartMouse"
          @mousemove.prevent="handleSwipeMoveMouse"
          @mouseup.prevent="handleSwipeEnd"
          @mouseleave.prevent="handleSwipeEnd"
        >
          <v-card
            class="card-item elevation-8"
            :class="{ 'card-swiping': index === 0 && isSwiping }"
          >
            <div class="image-container" @wheel.prevent="handleMouseWheel">
              <v-img
                :src="card.imageUrl"
                :alt="card.title"
                class="image-zoom"
                :style="getImageStyle()"
                @touchstart.prevent="handleDragStartTouch"
                @touchmove.prevent="handleDragMoveTouch"
                @touchend.prevent="handleDragEnd"
                @mousedown.prevent="handleStartMouse"
                @mousemove.prevent="handleDragMoveMouse"
                @mouseup.prevent="handleDragEnd"
                @mouseleave.prevent="handleDragEnd"
              />
            </div>
          </v-card>
        </div>
      </div>
    </div>

    <v-container width="auto" class="pt-2">
      <v-progress-linear
        color="green"
        class="progress-bar"
        rounded
        :model-value="progress"
      />

      <v-toolbar
        rounded
        class="pa-2"
        density="compact"
        color="rgba(0,0,0,0.5)"
      >
        <v-btn
          icon="mdi-arrow-left"
          @click="backward"
          color="white"
          :disabled="currentIndex === 0"
        />

        <v-spacer/>

        <v-toolbar-title class="text-center">SWAN</v-toolbar-title>

        <v-spacer/>

        <v-btn
          icon="mdi-help-circle"
          @click="showHelp = true"
          color="white"
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
              prepend-icon="mdi-arrow-up"
              title="Swipe Up"
              subtitle="Classify as A"
            />
            <v-list-item
              prepend-icon="mdi-arrow-down"
              title="Swipe Down"
              subtitle="Classify as B"
            />
            <v-list-item
              prepend-icon="mdi-arrow-left"
              title="Swipe Left"
              subtitle="Classify as C"
            />
            <v-list-item
              prepend-icon="mdi-arrow-right"
              title="Swipe Right"
              subtitle="Classify as D"
            />

            <v-divider/>

            <v-list-subheader inset>Inspect</v-list-subheader>
            <v-list-item
              prepend-icon="mdi-magnify"
              title="Zoom"
              subtitle="Pinch or Mouse-Whell"
            />
            <v-list-item
              prepend-icon="mdi-magnify-expand"
              title="Reset"
              subtitle="Double-Tap or -Click"
            />
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn color="primary" @click="showHelp = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue'

// TODO
// - dragging should be scaled to the zoom factor
// - double click reset zoom factor
// - implement lazy loading for cards (nextCard() -> (card, hasNext)

export interface Card {
  id: string
  imageUrl: string
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
  cards: Card[]
}

const props = withDefaults(defineProps<Props>(), {
  cards: () => [],
})

const emit = defineEmits<{
  swiped: [event: SwipeEvent]
}>()

const currentIndex = ref(0)
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

// data holder
const swipeDirections: Record<string, SwipeDirection> = {
  up: {direction: 'up', action: 'Favorit', color: 'success', icon: 'mdi-heart'},
  down: {direction: 'down', action: 'Ablehnen', color: 'error', icon: 'mdi-close'},
  left: {direction: 'left', action: 'Später', color: 'warning', icon: 'mdi-clock'},
  right: {direction: 'right', action: 'Teilen', color: 'info', icon: 'mdi-share'}
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
      opacity: 1 - Math.abs(deltaX) / 1000 - Math.abs(deltaY) / 1000
    }
  }

  return {
    transform: baseTransform,
    opacity: 1 - index * 0.2
  }
}

const getImageStyle = () => {
  return {
    transform: `scale(${imageZoom.value}) translate(${imageX.value}px, ${imageY.value}px)`,
    transformOrigin: 'center center',
    transition: isDragging.value ? 'none' : 'transform 0.3s ease'
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
    swipeStart(e.touches[0])
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
    swipeMove(e.touches[0])
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

  const delta = {x: currentX.value - startX.value, y: currentY.value - startY.value}

  const threshold = 50;

  if (Math.abs(delta.x) > threshold || Math.abs(delta.y) > threshold) {
    if (Math.abs(delta.x) > Math.abs(delta.y)) {
      swipeDirection.value = delta.x > 0 ? 'right' : 'left'
    } else {
      swipeDirection.value = delta.y > 0 ? 'down' : 'up'
    }
  } else {
    swipeDirection.value = null
  }
}

const handleSwipeEnd = () => {
  if (!isSwiping.value) return

  const delta = {x: currentX.value - startX.value, y: currentY.value - startY.value}

  const threshold = 100

  if (Math.abs(delta.x) > threshold || Math.abs(delta.y) > threshold) {
    let direction

    if (Math.abs(delta.x) > Math.abs(delta.y)) {
      direction = delta.x > 0 ? 'right' : 'left'
    } else {
      direction = delta.y > 0 ? 'down' : 'up'
    }

    emit('swiped', <SwipeEvent>{
      card: props.cards[currentIndex.value],
      direction: direction,
    })

    forward()
  }

  swipeReset();
}

function swipeReset() {
  isSwiping.value = false

  swipeDirection.value = null

  currentX.value = startX.value
  currentY.value = startY.value
}

// Drag Events
const handleDragStartTouch = (e: TouchEvent) => {
  if (e.touches.length === 1) {
    dragStart(e.touches[0])
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
    dragMove(e.touches[0])
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
  return Math.hypot(touch1.clientX - touch2.clientX, touch1.clientY - touch2.clientY);
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
