/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHashHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import { useAppStore } from '@/stores/app.ts';
import client from '@/client.ts';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')

  const store = useAppStore()

  if (store.loggedIn) {
    client.GET('/v1/auth/status/')
      .then(res => {
        if (!res.data?.authenticated) {
          router.push('/login')
        } else if (router.currentRoute.value.name === '/') {
          router.push('/overview')
        }
      })
      .catch(error => console.log(error))
  }
})

router.beforeEach(to => {
  //Avoid access to the app if not logged in
  const store = useAppStore()

  if (!store.loggedIn && to.name !== '/login') {
    if (to.name === '/studies.[id].[[tag]]' && (to.params.tag?.length ?? 0) > 0) {
      return
    }

    return { name: '/login' }
  }
})

export default router
