<script setup lang="ts">
  import type { Ui } from '@/api.ts';
  import { useAppStore } from '@/stores/app.ts';

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

  const imageZoom = ref(store.studySettings[props.study]?.imageZoom ?? props.ui.default_scale ?? 100)

  watch(imageZoom, newValue => {
    store.updateSettings(props.study, { imageZoom: newValue })
  })

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
            <v-list-subheader inset>Image Zoom</v-list-subheader>
            <v-slider
              v-model="imageZoom"
              append-icon="mdi-magnify-plus-outline"
              max="150"
              min="10"
              prepend-icon="mdi-magnify-minus-outline"
              step="5"
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
