// Utilities
import { defineStore } from 'pinia'
import { DEFAULTS } from '@/const.ts';

interface AppState {
  login: boolean
  studySettings: Record<string, StudySettings>
}

interface StudySettings {
  imageZoom: number
  thresholdSwipe: number
  thresholdDoubleTap: number
}

export const useAppStore = defineStore('app', {
  state: (): AppState => ({
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
        this.studySettings[study] = { imageZoom: DEFAULTS.IMAGE_ZOOM, thresholdDoubleTap: DEFAULTS.DOUBLE_TAP_THRESHOLD, thresholdSwipe: DEFAULTS.SWIPE_THRESHOLD }
      }
      Object.assign(this.studySettings[study], patch)
      localStorage.setItem('studySettings', JSON.stringify(this.studySettings))
    },
  },
})
