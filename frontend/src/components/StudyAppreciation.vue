<script setup lang="ts">
  interface Props {
    postpone?: boolean
    show?: boolean
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
  })

  const emit = defineEmits<{
    close: [event: void]
  }>()

  const show = computed({
    get () {
      return props.show
    },
    set () {
      emit('close')
    },
  })
</script>

<template>
  <v-dialog
    v-model="show"
    width="50%"
  >
    <v-card
      class="mx-auto"
    >
      <v-card-title class="text-center">
        <v-icon icon="mdi-heart" />

        <span v-if="props.postpone">
          You have seen all images
        </span>
        <span v-else>
          You have reached the end
        </span>
      </v-card-title>
      <v-card-text class="ma-3 text-center">
        <span>
          Thank you for participating in this study!
        </span>

        <hr v-if="props.postpone" class="my-6">

        <span v-if="props.postpone">
          Images marked for later classification will now be shown again.
          You can skip images again.
        </span>
      </v-card-text>

      <template #actions>
        <v-btn
          class="ms-auto"
          text="Ok"
          @click="show = false"
        />
      </template>
    </v-card>
  </v-dialog>
</template>
