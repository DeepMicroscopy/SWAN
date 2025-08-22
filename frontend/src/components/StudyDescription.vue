<script setup lang="ts">
  import type { StudyList } from '@/api.ts';
  import MarkdownIt from 'markdown-it';
  import DOMPurify from 'dompurify';

  interface Props {
    study?: StudyList | null
    show?: boolean
  }

  const props = withDefaults(defineProps<Props>(), {
    study: () => ({} as StudyList),
    show: () => false,
  })

  const emit = defineEmits<{
    close: [event: void]
  }>()

  const showStudy = computed({
    get () {
      return props.show
    },
    set () {
      emit('close')
    },
  })

  function formatMarkdown (description: string|undefined|null): string|undefined {
    if (!description) return;

    const md = new MarkdownIt();
    console.group('des')
    console.log(md.render(description))
    console.log(DOMPurify.sanitize(md.render(description)))
    console.groupEnd()
    return DOMPurify.sanitize(md.render(description));
  }
</script>

<template>
  <v-dialog
    v-model="showStudy"
    width="auto"
  >
    <v-card
      class="mx-auto"
    >
      <v-img
        v-if="props.study?.image"
        cover
        :src="props.study.image"
      />
      <v-card-title>
        <v-icon icon="mdi-folder-information-outline" />
        {{ props.study?.title }}
      </v-card-title>
      <v-card-text class="ma-3">
        <div v-html="formatMarkdown(props.study?.description)" />
      </v-card-text>

      <template #actions>
        <v-btn
          class="ms-auto"
          text="Ok"
          @click="showStudy = false"
        />
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="sass">

</style>
