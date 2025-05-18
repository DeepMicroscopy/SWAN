<script setup lang="ts">
import {ref} from 'vue'

const visible = ref(false)
const rememberMe = ref(false)
</script>

<template>
  <v-container>
    <v-sheet class="pa-6 px-md-10 py-md-12"  max-width="450" rounded="xl" elevation="5">
      <h1 class="text-h4 font-weight-black mb-5 text-indigo-lighten-4">Login</h1>
      <v-form>
        <div class="text-subtitle-1 text-medium-emphasis">Email address</div>
        <v-text-field
          density="compact"
          placeholder="you@example.com"
          prepend-inner-icon="mdi-email-outline"
          variant="outlined"
        ></v-text-field>
        <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
          Password
          <a
            class="text-caption text-decoration-none text-blue"
            href="#"
            rel="noopener noreferrer"
            target="_blank"
          >
            Forgot login password?</a>
        </div>
        <v-text-field
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          density="compact"
          placeholder="Enter your password"
          prepend-inner-icon="mdi-lock-outline"
          variant="outlined"
          @click:append-inner="visible = !visible"
        ></v-text-field>
        <v-checkbox v-model="rememberMe" label="Remember me" color="indigo"></v-checkbox>
        <v-btn block rounded="lg" variant="elevated" color="indigo">Login</v-btn>
      </v-form>
    </v-sheet>
  </v-container>

</template>

<style scoped lang="sass">

</style>
