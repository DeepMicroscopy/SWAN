<script setup lang="ts">
  import type { UiLabel } from '@/api.ts';

  interface Props {
    show?: boolean
    labels?: UiLabel
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
    labels: () => ({
      'left': {
        'text': 'n/a',
      },
      'right': {
        'text': 'n/a',
      },
    } as UiLabel),
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
