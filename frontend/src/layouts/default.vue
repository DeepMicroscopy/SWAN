<template>
  <v-navigation-drawer v-model="drawer">
    <v-list nav>
      <v-list-item link prepend-icon="mdi-duck" title="SWAN" />
      <v-divider />
    </v-list>
    <template v-if="store.loggedIn" #append>
      <v-divider />
      <v-list-item>
        <template #append>
          <v-btn
            append-icon="mdi-logout"
            link
            to="login"
            variant="plain"
            @click="logoff()"
          >
            Logout

            <template #append>
              <v-icon color="error" />
            </template>
          </v-btn>
        </template>
      </v-list-item>
    </template>
  </v-navigation-drawer>

  <v-app-bar>
    <template #prepend>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
    </template>
    <v-app-bar-title>SWAN App</v-app-bar-title>
  </v-app-bar>

  <v-main>
    <router-view />
  </v-main>

  <AppFooter />
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
  import { useAppStore } from '@/stores/app.ts';
  import { useRouter } from 'vue-router';
  import client from '@/client.ts';

  const store = useAppStore()
  const router = useRouter()
  const drawer = ref(false)

  function logoff () {
    client.POST('/v1/auth/logout/')
      .catch(error => console.log(error))
      .finally( () => {
        store.logOff()
        router.push('/login')
      })
  }
</script>
