<template>
  <v-app class="rounded rounded-md">
    <router-view/>
  </v-app>
</template>

<script lang="ts" setup>
import {ref} from 'vue'

const drawer = ref(false)
</script>
