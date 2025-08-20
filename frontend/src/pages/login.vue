<script setup lang="ts">
  import { ref } from 'vue'
  import { useAppStore } from '@/stores/app.ts';
  import { useRouter } from 'vue-router';
  import client from '@/client.ts';

  const store = useAppStore()
  const router = useRouter()

  const visible = ref(false)
  const username = ref('')
  const password = ref('')
  const failureMessage = ref(false)

  function login () {
    client.POST('/v1/auth/login/', {
      body: {
        username: username.value,
        password: password.value,
      },
    })
      .then(() => {
        failureMessage.value = false
        store.logOn()
        router.push('/overview')
      })
      .catch(error => {
        console.log(error)
        failureMessage.value = true
      })
  }
</script>

<template>
  <v-container>
    <v-sheet class="pa-6 px-md-10 py-md-12" elevation="5" max-width="450" rounded="xl">
      <h1 class="text-h4 font-weight-black mb-5 text-indigo-lighten-4">Login</h1>

      <v-alert
        v-model="failureMessage"
        class="mb-5"
        text="We couldn’t sign you in. Please check your credentials."
        type="error"
        variant="tonal"
      />
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
        <v-btn
          block
          color="indigo"
          :disabled="username === '' || password === ''"
          rounded="lg"
          size="x-large"
          variant="elevated"
          @click="login()"
        >Login
        </v-btn>
      </v-form>
    </v-sheet>
  </v-container>

</template>

<style scoped lang="sass">

</style>
