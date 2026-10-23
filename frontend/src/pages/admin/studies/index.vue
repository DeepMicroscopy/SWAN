<script setup lang="ts">
  import { ref } from 'vue';
  import client from '@/client.ts';
  import type { StudyProgress } from '@/api.ts';
  import { type ErrorData, getError, setError } from '@/util/fetch-errors.ts';

  const studies = ref<StudyProgress[]>([])
  const loading = ref(true)
  const error = ref<ErrorData>(getError())

  onMounted(() => {
    client.GET('/v1/studies/all/')
      .then(result => {
        if (!result.response.ok) {
          setError(error.value, result.error, result.response)
          return
        }

        studies.value = result.data as StudyProgress[];
      })
      .catch(err => console.log(err))
      .finally(() => { loading.value = false })
  })

  function formatDate (rawDate: string): string {
    return new Date(rawDate).toLocaleDateString('en-US', { year: 'numeric', month: 'numeric', day: 'numeric' });
  }

  function percent (study: StudyProgress): number {
    if (study.reviewers.length === 0 || study.file_count === 0) {
      return 0
    }
    const done = study.reviewers.reduce((sum, r) => sum + Math.min(r.classified, study.file_count), 0)
    return Math.round(100 * done / (study.reviewers.length * study.file_count))
  }
</script>

<template>
  <v-container max-width="1000">
    <h2 class="text-h5 mb-4">Study overview</h2>

    <v-progress-linear v-if="loading" indeterminate />

    <v-table v-else-if="studies.length > 0" hover>
      <thead>
        <tr>
          <th>Study</th>
          <th>Group</th>
          <th class="text-right">Images</th>
          <th>Reviewers</th>
          <th style="min-width: 160px">Progress</th>
          <th>Period</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="study in studies" :key="study.study">
          <td>
            <router-link :to="{ name: '/admin/studies/[id]', params: { id: study.study } }">{{ study.title }}</router-link>
          </td>
          <td>{{ study.group ?? '–' }}</td>
          <td class="text-right">{{ study.file_count }}</td>
          <td>{{ study.complete_reviewers }} / {{ study.reviewers.length }} finished</td>
          <td>
            <v-progress-linear
              :color="study.complete_reviewers === study.reviewers.length && study.reviewers.length > 0 ? 'success' : 'primary'"
              height="10"
              :model-value="percent(study)"
              rounded
            />
          </td>
          <td>{{ formatDate(study.pub_date) }} – {{ formatDate(study.end_date) }}</td>
        </tr>
      </tbody>
    </v-table>

    <p v-else-if="!error.show" class="text-medium-emphasis">There are no studies yet.</p>
  </v-container>

  <FetchError :code="error.code" :show="error.show" :text="error.text" @close="error.show = false" />
</template>
