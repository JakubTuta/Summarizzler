/* eslint-disable node/prefer-global/process */
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  app: {
    head: {
      title: 'SummaRizzler',
      meta: [
        { name: 'description', content: 'AI-powered tool that generates concise summaries for text, websites, files, and videos using advanced language models.' },
      ],
    },
  },

  runtimeConfig: {
    public: {
      SERVER_URL: process.env.SERVER_URL
        ? process.env.SERVER_URL
        : process.env.DOCKER === 'true'
          ? 'http://host.docker.internal:8000'
          : 'http://localhost:8000',
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
        config.plugins?.push(vuetify({ autoImport: true }))
      })
    },
  ],

  imports: {
    autoImport: true,
    dirs: [
      'stores/**',
      'constants/**',
      'components/**',
      'helpers/**',
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
    firebase: {
      gen: 2,
    },
  },

  typescript: {
    strict: true,
  },

  compatibilityDate: '2024-07-18',
})
