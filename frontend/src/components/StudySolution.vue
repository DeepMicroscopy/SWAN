<script setup lang="ts">
  import type { Education, SolutionConfig, Study } from '@/api.ts';
  import MarkdownIt from 'markdown-it';
  import DOMPurify from 'dompurify';

  interface Props {
    config?: SolutionConfig | null
    education?: Education | null
    study?: Study | null
    show?: boolean
    current?: string
  }

  const props = withDefaults(defineProps<Props>(), {
    show: () => false,
  })

  const emit = defineEmits<{
    close: [event: void]
  }>()

  const showSolution = computed({
    get () {
      return props.show
    },
    set () {
      emit('close')
    },
  })

  function formatMarkdown (text: string|undefined|null): string|undefined {
    if (!text) return;

    const md = new MarkdownIt();
    return DOMPurify.sanitize(md.render(text));
  }
</script>

<template>
  <v-dialog
    v-model="showSolution"
    width="auto"
  >
    <v-card
      class="mx-auto"
    >
      <v-card-title>
        <v-icon icon="mdi-folder-information-outline" />
        {{ props.study?.title }}
      </v-card-title>
      <v-card-text class="ma-3 min-width-images">
        <v-row v-if="props.education?.proof" :class="props.config?.css_row ?? 'text-center text-decoration-underline font-weight-bold'">
          <v-col :class="props.config?.css_column" cols="6">{{ props.config?.label_current ?? "Current" }}</v-col>

          <v-col :class="props.config?.css_column" cols="6">{{ props.config?.label_proof ?? "Proof" }}</v-col>

          <v-col :class="props.config?.css_column" cols="6">
            <v-img
              aspect-ratio="1"
              cover
              :src="props.current"
            />
          </v-col>

          <v-col :class="props.config?.css_column" cols="6">
            <v-img
              aspect-ratio="1"
              cover
              :src="props.education.proof"
            />
          </v-col>
        </v-row>

        <v-divider class="my-6" />

        <div v-if="props.education" v-html="formatMarkdown(props.education.solution?.text)" />
      </v-card-text>

      <template #actions>
        <v-btn
          class="ms-auto"
          text="Ok"
          @click="showSolution = false"
        />
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.min-width-images {
  min-width: 350px;

  @media (max-width: 425px) {
    min-width: 300px;
  }

  @media (max-width: 375px) {
    min-width: 250px;
  }

  @media (min-width: 1200px) {
    min-width: 425px;
  }
}
</style>
