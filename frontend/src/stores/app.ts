// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    login: false
  }),
  getters: {
    loggedIn(state) {
      return state.login
    }
  },
  actions: {
    logOn() {
      this.login = true
    },
    logOff() {
      this.login = false
    }
  }
})
