<script setup lang="ts">
  import { ref } from 'vue';
  import client from '@/client.ts';
  import type { StudyList } from '@/api.ts';
  import StudyDescription from '@/components/StudyDescription.vue';
  import { type ErrorData, getError, setError } from '@/util/fetch-errors.ts';


  const studies = ref<StudyList[]>([])
  const current = ref<StudyList | null>(null)
  const showStudy = ref(false)
  const error = ref<ErrorData>(getError())

  onMounted(() => {
    client.GET('/v1/studies/')
      .then(result => {
        if (!result.response.ok) {
          setError(error.value, result.error, result.response)
          return
        }

        studies.value = result.data as StudyList[];
      })
      .catch(err => console.log(err))
  })

  function formatDate (rawDate: string): string {
    return new Date(rawDate).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
    });
  }

  function setStudy (s: StudyList) {
    current.value = s
    showStudy.value = true
  }

</script>

<template>
  <v-card
    class="mx-auto"
    max-width="375"
  >
    <v-img
      class="text-white align-end"
      cover
      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
      height="250px"
      src="@/assets/image-title.jpg"
    >
      <v-card-title class="text-white">Your Studies</v-card-title>
    </v-img>

    <v-list lines="two">
      <v-list-item
        v-for="(study, index) in studies"
        :key="index"
      >
        <v-list-item-title>{{ study.title }}</v-list-item-title>
        <v-list-item-subtitle>{{ formatDate(study.pub_date) }} - {{ formatDate(study.end_date) }}</v-list-item-subtitle>
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            :icon="study.educational ? 'mdi-clipboard-text' : 'mdi-microscope'"
            :to="{ name: '/studies.[id].[[tag]]', params: { id: study.id } }"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="setStudy(study)"
          />
        </template>


      </v-list-item>

    </v-list>
  </v-card>

  <StudyDescription :show="showStudy" :study="current" @close="showStudy = false" />

  <FetchError :code="error.code" :show="error.show" :text="error.text" @close="error.show = false" />
</template>

<style scoped lang="sass">

</style>
