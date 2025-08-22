<script setup lang="ts">
  import { useAppStore } from '@/stores/app.ts';
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';
  import SwiperHelp from '@/components/SwiperHelp.vue';
  import type { UiLabel } from '@/api.ts';


  const router = useRouter()
  const store = useAppStore()

  interface Props {
    title?: string
    index?: number
    total?: number
    labels?: UiLabel
  }

  const props = withDefaults(defineProps<Props>(), {
    title: () => 'n/a',
    index: () => 0,
    total: () => 0,
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
    back: [event: void]
  }>()

  const showHelp = ref(false)

  const progress = computed(() => {
    return 100 * (props.index / props.total)
  })

  const backward = () => {
    emit('back')
  }

  const close = () => {
    router.back()
  }
</script>

<template>
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
        :disabled="props.index === 0"
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

    <SwiperHelp :labels="props.labels" :show="showHelp" @close="showHelp = false" />
  </v-container>
</template>

<style scoped lang="sass">

</style>
