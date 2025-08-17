// Utilities
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    login: !!localStorage.getItem('login'),
  }),
  getters: {
    loggedIn (state) {
      return state.login
    },
  },
  actions: {
    logOn () {
      this.login = true
      localStorage.setItem('login', 'true')
    },
    logOff () {
      this.login = false
      localStorage.removeItem('login')
    },
  },
})
