<script setup lang="ts">
  import { ref } from 'vue';
  import { default as axios } from 'axios';


  const dialog = ref(false)

  const studies = ref([])

  onMounted( () => {
    console.log('LOAD studies...')

    axios.get('/v1/studies/')
      .then(function (response) {
        studies.value = response.data;
        console.log(studies)

        studies.value.forEach(function (study) {
          console.log('Studies:')
          for (const key in study) {
            console.log(key,':', study[key])
          }
        })
      })
      .catch(function (error) {
        console.log(error);
      })
  })

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
        subtitle="May 13, 2025"
        title="Histogram"
      >
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            icon="mdi-clipboard-text"
            to="swipe"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          />
        </template>

        <v-dialog
          v-model="dialog"
          width="auto"
        >
          <v-card
            max-width="400"
            prepend-icon="mdi-folder-information-outline"
            text="In this study, we investigate the different manifestations of cell division visualized on microscopic images."
            title="Study Description"
          >
            <template #actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              />
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
      <v-list-item
        subtitle="Jan 20, 2025"
        title="Atypical cells"
      >
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            icon="mdi-clipboard-text"
            to="swipe"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          />
        </template>

        <v-dialog
          v-model="dialog"
          width="auto"
        >
          <v-card
            max-width="400"
            prepend-icon="mdi-folder-information-outline"
            text="In this study, we investigate the different manifestations of cell division visualized on microscopic images."
            title="Study Description"
          >
            <template #actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              />
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>

    <v-divider />
    <v-list lines="three">
      <v-list-item
        subtitle="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
      eirmod tENDE invidunt ut labore et dolore magna aliquyam erat, sed"
        title="Long subtitle Histogram"
      >
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            icon="mdi-clipboard-text"
            to="swipe"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          />
        </template>

        <v-dialog
          v-model="dialog"
          width="auto"
        >
          <v-card
            max-width="400"
            prepend-icon="mdi-folder-information-outline"
            text="In this study, we investigate the different manifestations of cell division visualized on microscopic images."
            title="Study Description"
          >
            <template #actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              />
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
      <v-divider inset />
      <v-list-item
        subtitle="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
      eirmod tENDE"
        title="Long title Histogram-Histogram-Histogram"
      >
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            icon="mdi-clipboard-text"
            to="swipe"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          />
        </template>

        <v-dialog
          v-model="dialog"
          width="auto"
        >
          <v-card
            max-width="400"
            prepend-icon="mdi-folder-information-outline"
            text="In this study, we investigate the different manifestations of cell division visualized on microscopic images."
            title="Study Description"
          >
            <template #actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              />
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
      <v-list-item
        v-for="(study, index) in studies"
        :key="index"
      >
        <v-list-item-title>{{ study.title }}</v-list-item-title>
        <v-list-item-subtitle>{{ study.pub_date }}</v-list-item-subtitle>
        <template #prepend>
          <v-btn
            class="mr-3"
            color="blue"
            density="default"
            icon="mdi-clipboard-text"
            to="swipe"
          />
        </template>

        <template #append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          />
        </template>

        <v-dialog
          v-model="dialog"
          width="auto"
        >
          <v-card
            max-width="400"
            prepend-icon="mdi-folder-information-outline"
            text="In this study, we investigate the different manifestations of cell division visualized on microscopic images."
            title="Study Description"
          >
            <template #actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              />
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>

    </v-list>
  </v-card>

</template>

<style scoped lang="sass">

</style>
