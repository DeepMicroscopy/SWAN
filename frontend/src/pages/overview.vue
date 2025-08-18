<script setup lang="ts">
  import { ref } from 'vue';
  import { default as axios } from 'axios';
  import type { StudyList } from '@/api.ts';
  import MarkdownIt from 'markdown-it';
  import DOMPurify from 'dompurify';

  const showDialog = ref(false)
  const dialog = ref<StudyList | null>(null)

  const studies = ref<StudyList[]>([])

  onMounted(() => {
    console.log('LOAD studies...')

    axios.get('/v1/studies/')
      .then(function (response) {
        studies.value = response.data;

        console.log('Studies:')
        studies.value.forEach((study: StudyList) => {
          console.group(`id: ${study.id}`)

          const entries = Object.entries(study)

          for (const key in entries) {
            console.log(key + ':', entries[key])
          }

          console.groupEnd()
        })
      })
      .catch(function (error) {
        console.log(error);
      })
  })

  function formatDate (rawDate: string): string {
    return new Date(rawDate).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric',
    });
  }

  function formatMarkdown (description: string|undefined): string|undefined {
    if (!description) return;

    const md = new MarkdownIt();
    console.group('des')
    console.log(md.render(description))
    console.log(DOMPurify.sanitize(md.render(description)))
    console.groupEnd()
    return DOMPurify.sanitize(md.render(description));
  }

  function setDialog (study: StudyList) {
    showDialog.value = true
    dialog.value = study
  }

</script>

<template>
  <v-card
    class="mx-auto"
    max-width="375"
  >
    <v-img
      class="text-white"
      cover
      height="250px"
      src="@/assets/malignant-spindle-cell-neoplasm.jpg"
    >
      <div class="d-flex flex-column h-100">
        <v-card-title class="d-flex ga-2 px-2">
          <v-btn color="indigo-darken-2" icon="mdi-chevron-left" variant="text" />
          <v-spacer />
          <v-btn color="indigo-darken-2" icon="mdi-pencil" variant="text" />
          <v-btn color="indigo-darken-2" icon="mdi-dots-vertical" variant="text" />
        </v-card-title>

        <v-card-title class="pb-6 text-center text-indigo-darken-2">
          <div class="text-h3 font-weight-black mt-5">Your Studies</div>
        </v-card-title>
      </div>
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
            icon="mdi-clipboard-text"
            :to="{ name: '/studies.[id].[[tag]]', params: { id: study.id } }"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="setDialog(study)"
          />
        </template>


      </v-list-item>

    </v-list>
  </v-card>

  <v-dialog
    v-model="showDialog"
    width="auto"
  >
    <v-card
      class="mx-auto"
    >
      <v-img
        cover
        :src="dialog?.image"
      />
      <v-card-title>
        <v-icon icon="mdi-folder-information-outline" />
        Study Description
      </v-card-title>
      <v-card-text class="ma-3">
        <div v-html="formatMarkdown(dialog?.description)" />
      </v-card-text>

      <template #actions>
        <v-btn
          class="ms-auto"
          text="Ok"
          @click="showDialog = false"
        />
      </template>
    </v-card>
  </v-dialog>

</template>

<style scoped lang="sass">

</style>
