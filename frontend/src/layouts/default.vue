<template>
  <v-navigation-drawer v-model="drawer">
    <v-list nav>
      <v-list-item title="Menü" link></v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-app-bar>
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>SWAN App</v-app-bar-title>
  </v-app-bar>

  <v-main>
    <router-view />
  </v-main>

  <AppFooter />
</template>

<script lang="ts" setup>
import {ref} from 'vue'

const drawer = ref(false)
</script>
