<script setup lang="ts">
import {ref} from "vue";

const dialog = ref(false)
</script>

<template>
  <v-card
    class="mx-auto"
    max-width="375"
  >
    <v-img
      class="text-white"
      height="250px"
      src="@/assets/malignant-spindle-cell-neoplasm.jpg"
      cover
    >
      <div class="d-flex flex-column h-100">
        <v-card-title class="d-flex ga-2 px-2">
          <v-btn icon="mdi-chevron-left" variant="text" color="indigo-darken-2"></v-btn>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-pencil" variant="text" color="indigo-darken-2"></v-btn>
          <v-btn icon="mdi-dots-vertical" variant="text" color="indigo-darken-2"></v-btn>
        </v-card-title>

        <v-card-title class="pb-6 text-center text-indigo-darken-2">
          <div class="text-h3 font-weight-black mt-5">Your Studies</div>
        </v-card-title>
      </div>
    </v-img>

    <v-list lines="two">
      <v-list-item
        title="Histogram"
        subtitle="May 13, 2025"
      >
        <template v-slot:prepend>
          <v-btn density="default" color="blue" icon="mdi-clipboard-text" class="mr-3" to="swipe"></v-btn>
        </template>

        <template v-slot:append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          ></v-btn>
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
            <template v-slot:actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              ></v-btn>
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
      <v-list-item
        title="Atypical cells"
        subtitle="Jan 20, 2025"
      >
        <template v-slot:prepend>
          <v-btn density="default" color="blue" icon="mdi-clipboard-text" class="mr-3" to="swipe"></v-btn>
        </template>

        <template v-slot:append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          ></v-btn>
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
            <template v-slot:actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              ></v-btn>
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>
    <v-list lines="three">
      <v-list-item
        title="Long subtitle Histogram"
        subtitle="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
      eirmod tENDE invidunt ut labore et dolore magna aliquyam erat, sed"
      >
        <template v-slot:prepend>
          <v-btn density="default" color="blue" icon="mdi-clipboard-text" class="mr-3" to="swipe"></v-btn>
        </template>

        <template v-slot:append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          ></v-btn>
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
            <template v-slot:actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              ></v-btn>
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
      <v-divider inset></v-divider>
      <v-list-item
        title="Long title Histogram-Histogram-Histogram"
        subtitle="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy
      eirmod tENDE"
      >
        <template v-slot:prepend>
          <v-btn density="default" color="blue" icon="mdi-clipboard-text" class="mr-3" to="swipe"></v-btn>
        </template>

        <template v-slot:append>
          <v-btn
            color="grey-lighten-1"
            icon="mdi-information"
            variant="text"
            @click="dialog = true"
          ></v-btn>
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
            <template v-slot:actions>
              <v-btn
                class="ms-auto"
                text="Ok"
                @click="dialog = false"
              ></v-btn>
            </template>
          </v-card>
        </v-dialog>
      </v-list-item>
    </v-list>
  </v-card>

</template>

<style scoped lang="sass">

</style>
