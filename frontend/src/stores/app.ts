// Utilities
import { defineStore } from 'pinia'

interface StudySettings {
  imageZoom: number
}

export const useAppStore = defineStore('app', {
  state: () => ({
    login: !!localStorage.getItem('login'),
    studySettings: JSON.parse(localStorage.getItem('studySettings')!) ?? {} as Record<string, StudySettings>,
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
    updateSettings (study: string, patch: Partial<StudySettings>) {
      if (!this.studySettings[study]) {
        this.studySettings[study] = {}
      }
      Object.assign(this.studySettings[study], patch)
      localStorage.setItem('studySettings', JSON.stringify(this.studySettings))
    },
  },
})
