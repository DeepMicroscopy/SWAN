<script setup lang="ts">
  interface Props {
    show?: boolean
    text?: string
    icon?: string
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
    text: () => '',
    icon: () => '',
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
    :close-on-back="false"
    color="pink-accent-4"
    timeout="-1"
  >
    You classified:
    <v-icon>{{ icon }}</v-icon>
    {{ text }}

    <template #actions>
      <v-btn
        color="white"
        rounded="m"
        variant="outlined"
        @click="showSnackbar = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<style scoped lang="sass">

</style>
