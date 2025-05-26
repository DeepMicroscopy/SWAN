<template>
  <v-navigation-drawer v-model="drawer">
    <v-list nav>
      <v-list-item title="SWAN" prepend-icon="mdi-duck" link></v-list-item>
      <v-divider></v-divider>
    </v-list>
    <template v-slot:append v-if="store.loggedIn">
      <v-divider/>
      <v-list-item>
        <template v-slot:append>
          <v-btn variant="plain" append-icon="mdi-logout" @click="store.logOff()" link to="login">
            Logout

            <template v-slot:append>
              <v-icon color="error"></v-icon>
            </template>
          </v-btn>
        </template>
      </v-list-item>
    </template>
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
import { useAppStore} from "@/stores/app.ts";

const store = useAppStore()
const drawer = ref(false)
</script>
