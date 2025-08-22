<script setup lang="ts">
  interface Props {
    show?: boolean
    text?: string
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
    text: () => '',
  })

  const emit = defineEmits<{
    close: [event: void]
  }>()

  const showSnackbar = computed({
    get () {
      return props.show
    },
    set () {
      emit('close')
    },
  })
</script>

<template>
  <v-snackbar
    v-model="showSnackbar"
    color="green"
  >
    {{ text }}

    <template #actions>
      <v-btn
        color="white"
        variant="text"
        @click="showSnackbar = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<style scoped lang="sass">

</style>
