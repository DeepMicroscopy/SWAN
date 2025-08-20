<template>
  <v-navigation-drawer
    v-if="store.loggedIn && drawer"
    v-model="drawer"
  >
    <v-list nav>
      <v-list-item link title="SWAN">
        <template #prepend>
          <SwanIcon class="mr-4" />
        </template>
      </v-list-item>

      <v-divider />

      <v-list-item prepend-icon="mdi-home" to="/overview">
        Home
      </v-list-item>

      <v-list-item disabled prepend-icon="mdi-account" to="/profile">
        Profile
      </v-list-item>

      <v-list-item disabled prepend-icon="mdi-cog" to="/settings">
        Settings
      </v-list-item>
    </v-list>
    <template #append>
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
    <template v-if="store.loggedIn" #prepend>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
    </template>
    <v-app-bar-title>Swipeable Annotations</v-app-bar-title>
  </v-app-bar>

  <v-main class="mt-3">
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
