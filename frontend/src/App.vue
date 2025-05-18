<template>
  <v-app class="rounded rounded-md border">
    <v-navigation-drawer v-model="drawer">
      <v-list nav>
        <v-list-item title="Menü" link></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar>
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title>Minder App</v-app-bar-title>
    </v-app-bar>

    <router-view/>
  </v-app>
</template>

<script lang="ts" setup>
import {ref} from 'vue'

const drawer = ref(false)
</script>
