<script setup lang="ts">
  interface Props {
    show?: boolean
    text?: string
    code?: number
    timeout?: number
    closable?: boolean
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
    text: () => '',
    timeout: () => 10000,
    closable: () => true,
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
    color="error"
    :timeout="props.timeout"
  >
    <p :class="props.closable ? '' : 'text-center'">
      <span v-if="code">{{ code }}: </span>{{ text }}
    </p>

    <template v-if="props.closable" #actions>
      <v-btn variant="text" @click="showSnackbar = false">Close</v-btn>
    </template>
  </v-snackbar>
</template>

<style scoped lang="sass">

</style>
