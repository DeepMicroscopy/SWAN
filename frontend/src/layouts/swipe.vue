<template>
  <v-main>
    <Suspense>
      <router-view />

      <template #fallback>
        Loading
      </template>
    </Suspense>
  </v-main>
</template>

<script lang="ts" setup>
  //
</script>
