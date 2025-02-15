import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  app: {
    head: {
      title: 'SummaRizzler',
    },
  },

  build: {
    transpile: ['vuetify'],
  },

  modules: [
    '@vueuse/nuxt',
    '@unocss/nuxt',
    '@pinia/nuxt',
    '@nuxtjs/color-mode',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
  ],

  imports: {
    autoImport: true,
    dirs: [
      'stores/**',
      'constants/**',
      'utils/**',
    ],
  },

  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },

  ssr: false,

  nitro: {
    preset: 'node-server',
  },

  typescript: {
    strict: true,
  },

  compatibilityDate: '2024-07-18',
})
