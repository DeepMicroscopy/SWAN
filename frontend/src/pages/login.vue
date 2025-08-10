<script setup lang="ts">
  import { ref } from 'vue'
  import { useAppStore } from '@/stores/app.ts';
  import { default as axios } from 'axios';

  const store = useAppStore()
  const visible = ref(false)
  const rememberMe = ref(false)
  const username = ref('')
  const password = ref('')

  function login () {
    axios.post('/accounts/login/?next=/v1/studies/', { username, password }, { headers: { 'Content-Type':'application/x-www-form-urlencoded' } })
      .then(function (response) {
        console.log(response);
        store.logOn()
      })
      .catch(function (error) {
        console.log(error);
      })
  }
</script>

<template>
  <v-container>
    <v-sheet class="pa-6 px-md-10 py-md-12" elevation="5" max-width="450" rounded="xl">
      <h1 class="text-h4 font-weight-black mb-5 text-indigo-lighten-4">Login</h1>
      <v-form>
        <div class="text-subtitle-1 text-medium-emphasis">Email address</div>
        <v-text-field
          v-model="username"
          density="compact"
          placeholder="you@example.com"
          prepend-inner-icon="mdi-account"
          variant="solo-filled"
        />
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
          v-model="password"
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          density="compact"
          placeholder="Enter your password"
          prepend-inner-icon="mdi-lock"
          :type="visible ? 'text' : 'password'"
          variant="solo-filled"
          @click:append-inner="visible = !visible"
        />
        <v-checkbox v-model="rememberMe" color="indigo" label="Remember me" />
        <v-btn
          block
          color="indigo"
          :disabled="username === '' || password === ''"
          rounded="lg"
          size="x-large"
          to="/overview"
          variant="elevated"
          @click="login()"
        >Login</v-btn>
      </v-form>
    </v-sheet>
  </v-container>

</template>

<style scoped lang="sass">

</style>
