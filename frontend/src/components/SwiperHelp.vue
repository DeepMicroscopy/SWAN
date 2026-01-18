<script setup lang="ts">
  import type { Ui } from '@/api.ts';
  import { useAppStore } from '@/stores/app.ts';
  import { DEFAULTS } from '@/const.ts';

  const store = useAppStore()

  interface Props {
    show?: boolean
    ui?: Ui
    study?: string
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
    ui: () => ({} as Ui),
    study: () => 'n/a',
  })

  const emit = defineEmits<{
    close: [event: void]
  }>()

  const showHelp = computed({
    get () {
      return props.show
    },
    set () {
      emit('close')
    },
  })

  const imageZoom = ref(store.studySettings[props.study]?.imageZoom ?? props.ui.default_scale ?? DEFAULTS.IMAGE_ZOOM)
  const thresholdSwipe = ref(store.studySettings[props.study]?.thresholdSwipe ?? DEFAULTS.SWIPE_THRESHOLD)
  const thresholdDoubleTap = ref(store.studySettings[props.study]?.thresholdDoubleTap ?? DEFAULTS.DOUBLE_TAP_THRESHOLD)

  watch(imageZoom, newValue => {
    store.updateSettings(props.study, { imageZoom: newValue })
  }, { immediate: true })

  watch(thresholdSwipe, newValue => {
    store.updateSettings(props.study, { thresholdSwipe: newValue })
  }, { immediate: true })

  watch(thresholdDoubleTap, newValue => {
    store.updateSettings(props.study, { thresholdDoubleTap: newValue })
  }, { immediate: true })

</script>

<template>
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
            v-if="props.ui.labels.up"
            prepend-icon="mdi-arrow-up"
            :subtitle="`Classify as ${props.ui.labels.up.text}`"
            title="Swipe Up"
          />
          <v-list-item
            v-if="props.ui.labels.down"
            prepend-icon="mdi-arrow-down"
            :subtitle="`Classify as ${props.ui.labels.down.text}`"
            title="Swipe Down"
          />
          <v-list-item
            v-if="props.ui.labels.left"
            prepend-icon="mdi-arrow-left"
            :subtitle="`Classify as ${props.ui.labels.left.text}`"
            title="Swipe Left"
          />
          <v-list-item
            v-if="props.ui.labels.right"
            prepend-icon="mdi-arrow-right"
            :subtitle="`Classify as ${props.ui.labels.right.text}`"
            title="Swipe Right"
          />

          <v-divider class="mt-2" />

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

        <v-list>
          <v-list-subheader>User Settings</v-list-subheader>

          <v-list-item>
            <v-list-subheader>Image Zoom (%)</v-list-subheader>
            <v-slider
              v-model="imageZoom"
              append-icon="mdi-magnify-plus-outline"
              color="deep-purple-darken-3"
              hide-details
              max="150"
              min="10"
              prepend-icon="mdi-magnify-minus-outline"
              step="5"
              thumb-label
              thumb-size="10"
            />
          </v-list-item>
          <v-list-item>
            <v-list-subheader>Swipe Distance (px)</v-list-subheader>
            <v-slider
              v-model="thresholdSwipe"
              append-icon="mdi-gesture-swipe"
              color="light-blue-darken-3"
              hide-details
              max="400"
              min="50"
              prepend-icon="mdi-gesture-swipe-horizontal"
              step="25"
              thumb-label
              thumb-size="10"
            />
          </v-list-item>
          <v-list-item>
            <v-list-subheader>Double Tap (ms)</v-list-subheader>
            <v-slider
              v-model="thresholdDoubleTap"
              append-icon="mdi-timer-plus-outline"
              color="cyan-darken-3"
              hide-details
              max="1000"
              min="100"
              prepend-icon="mdi-timer-minus-outline"
              step="100"
              thumb-label
              thumb-size="10"
            />
          </v-list-item>
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
</template>

<style scoped lang="sass">

</style>
