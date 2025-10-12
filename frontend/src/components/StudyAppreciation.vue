<script setup lang="ts">
  interface Props {
    overtime?: boolean
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
    width="auto"
  >
    <v-card
      class="mx-auto"
    >
      <v-card-title class="text-center">
        <v-icon icon="mdi-heart" />
        The End
      </v-card-title>
      <v-card-text class="ma-3 text-center">
        <p>
          Thank you for participating in this study!
        </p>

        <hr v-if="props.overtime" class="my-6">

        <p v-if="props.overtime">
          Images marked for later classification will now be shown again.
          You can skip images again and come back later by reopening the study.
        </p>
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
