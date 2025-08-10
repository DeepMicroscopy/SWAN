/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')

// Axios
import axios from 'axios'

function getCookie (name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop()?.split(';').shift() : null;
}

axios.interceptors.request.use(config => {
  const token = getCookie('csrftoken')

  if (!config.headers['X-CSRFToken'] && token) {
    config.headers['X-CSRFToken'] = token
  }

  return config
})
