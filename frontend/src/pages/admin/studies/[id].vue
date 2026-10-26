<script setup lang="ts">
  import { onBeforeUnmount, ref } from 'vue';
  import DOMPurify from 'dompurify';
  import MarkdownIt from 'markdown-it';
  import { useRoute } from 'vue-router';
  import client from '@/client.ts';
  import type { StudyProgress } from '@/api.ts';
  import { type ErrorData, getError, setError } from '@/util/fetch-errors.ts';

  const route = useRoute<'/admin/studies/[id]'>()
  const progress = ref<StudyProgress | null>(null)
  const error = ref<ErrorData>(getError())

  function load () {
    client.GET('/v1/studies/{id}/progress/', { params: { path: { id: route.params.id } } })
      .then(result => {
        if (!result.response.ok) {
          setError(error.value, result.error, result.response)
          return
        }

        progress.value = result.data as StudyProgress
      })
      .catch(err => console.log(err))
  }

  load()
  // the reviewers keep working while this page is open
  const timer = setInterval(load, 30_000)
  onBeforeUnmount(() => clearInterval(timer))

  function formatDate (rawDate: string): string {
    return new Date(rawDate).toLocaleDateString('en-US', { year: 'numeric', month: 'numeric', day: 'numeric' });
  }

  function formatTime (rawDate: string | null | undefined): string {
    return rawDate ? new Date(rawDate).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }) : 'not started';
  }

  // descriptions are Markdown, as in the reviewers' view
  const md = new MarkdownIt()
  function formatMarkdown (text: string): string {
    return DOMPurify.sanitize(md.render(text))
  }

  function percent (classified: number, total: number): number {
    return total > 0 ? Math.min(100, Math.round(100 * classified / total)) : 0
  }
</script>

<template>
  <v-container max-width="900">
    <v-btn
      class="mb-2"
      prepend-icon="mdi-arrow-left"
      size="small"
      to="/admin/studies"
      variant="text"
    >All studies</v-btn>

    <v-progress-linear v-if="!progress && !error.show" indeterminate />

    <template v-if="progress">
      <h2 class="text-h5">{{ progress.title }}</h2>
      <div v-if="progress.description" class="text-medium-emphasis mt-1" v-html="formatMarkdown(progress.description)" />

      <div class="d-flex flex-wrap ga-2 my-4">
        <v-chip prepend-icon="mdi-account-group" variant="outlined">{{ progress.group ?? 'no group' }}</v-chip>
        <v-chip prepend-icon="mdi-image-multiple" variant="outlined">{{ progress.file_count }} images ({{ progress.dataset_title }})</v-chip>
        <v-chip prepend-icon="mdi-calendar" variant="outlined">{{ formatDate(progress.pub_date) }} – {{ formatDate(progress.end_date) }}</v-chip>
        <v-chip v-if="progress.anonymous" prepend-icon="mdi-incognito" variant="outlined">anonymous access</v-chip>
      </div>

      <v-card class="mb-4" title="Reviewers" variant="outlined">
        <v-list>
          <v-list-item v-for="r in progress.reviewers" :key="r.username">
            <v-list-item-title>{{ r.username }}</v-list-item-title>
            <v-list-item-subtitle>last activity: {{ formatTime(r.last_activity) }}</v-list-item-subtitle>
            <v-progress-linear
              class="mt-2"
              :color="r.complete ? 'success' : 'primary'"
              height="10"
              :model-value="percent(r.classified, progress.file_count)"
              rounded
            />
            <template #append>
              <v-chip :color="r.complete ? 'success' : undefined" size="small" variant="tonal">
                {{ r.complete ? 'finished' : `${r.classified} / ${progress.file_count}` }}
              </v-chip>
            </template>
          </v-list-item>
          <v-list-item v-if="progress.reviewers.length === 0">
            <v-list-item-title class="text-medium-emphasis">Nobody has started yet and the study has no group.</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>

      <v-card class="mb-4" title="Answers so far" variant="outlined">
        <v-card-text class="d-flex flex-wrap ga-2">
          <v-chip v-for="a in progress.answers" :key="a.choice" variant="tonal">{{ a.label ?? a.choice }}: {{ a.count }}</v-chip>
          <span v-if="progress.answers.length === 0" class="text-medium-emphasis">No answers yet.</span>
        </v-card-text>
      </v-card>

      <div class="d-flex flex-wrap ga-2">
        <v-btn :href="`/v1/export/${progress.study}/csv/`" prepend-icon="mdi-download" variant="tonal">Results (CSV)</v-btn>
        <v-btn :href="`/v1/export/${progress.study}/results/`" prepend-icon="mdi-code-json" target="_blank" variant="tonal">Results (JSON)</v-btn>
        <v-btn prepend-icon="mdi-microscope" :to="{ name: '/studies.[id].[[tag]]', params: { id: progress.study } }" variant="text">Take part</v-btn>
      </div>
      <p class="text-caption text-medium-emphasis mt-2">“Take part” opens the swipe view; it is only available to members of the study's group.</p>
    </template>
  </v-container>

  <FetchError :code="error.code" :show="error.show" :text="error.text" @close="error.show = false" />
</template>
