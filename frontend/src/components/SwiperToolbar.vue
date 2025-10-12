<script setup lang="ts">
  import { useAppStore } from '@/stores/app.ts';
  import { computed } from 'vue';
  import { useRouter } from 'vue-router';
  import SwiperHelp from '@/components/SwiperHelp.vue';
  import type { UiLabel } from '@/api.ts';
  import 'driver.js/dist/driver.css';


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
    } as UiLabel),
  })

  const emit = defineEmits<{
    back: [event: void]
  }>()

  const showHelp = ref(false)

  const titleStudy = useTemplateRef('title-study')
  const buttonHelp = useTemplateRef('button-help')
  const buttonBack = useTemplateRef('button-back')
  const progressBar = useTemplateRef('progress-bar')
  const buttonExit = useTemplateRef('button-exit')

  defineExpose({
    titleStudy,
    buttonHelp,
    buttonBack,
    progressBar,
    buttonExit,
  });

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
      ref="progress-bar"
      class="progress-bar"
      :color="props.index > props.total ? 'blue' : 'green'"
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
        ref="button-back"
        color="white"
        :disabled="props.index === 0"
        icon="mdi-arrow-left"
        @click="backward"
      />

      <v-spacer />

      <p ref="title-study">{{ props.title }}</p>

      <v-btn
        ref="button-help"
        class="ml-2"
        color="white"
        icon="mdi-help-circle"
        @click="showHelp = true"
      />

      <v-spacer />

      <v-btn
        ref="button-exit"
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
