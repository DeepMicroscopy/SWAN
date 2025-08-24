import vuetifyConfig from 'eslint-config-vuetify/index.ts.mjs'
import pluginCypress from 'eslint-plugin-cypress'

export default [
  ...vuetifyConfig,
  pluginCypress.configs.recommended,
  pluginCypress.configs.globals,
  {
    rules: {
      'cypress/no-unnecessary-waiting': 'off',
    },
  },
]
