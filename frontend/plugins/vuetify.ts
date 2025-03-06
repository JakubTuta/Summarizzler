import '@mdi/font/css/materialdesignicons.css'

import { createVuetify } from 'vuetify'
import 'vuetify/styles'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    ssr: false,
    theme: {
      defaultTheme: 'dark',
      themes: {
        light: {
          dark: false,
          colors: {
            'primary': 'rgba(142, 147, 108, 1)',
            'secondary': 'rgba(113, 108, 147, 1)',
            'primary-transparent': 'rgba(142, 147, 108, 0.25)',
            'secondary-transparent': 'rgba(113, 108, 147, 0.25)',
          },
        },
        dark: {
          dark: true,
          colors: {
            'primary': 'rgba(142, 147, 108, 1)',
            'secondary': 'rgba(113, 108, 147, 1)',
            'primary-transparent': 'rgba(142, 147, 108, 0.25)',
            'secondary-transparent': 'rgba(113, 108, 147, 0.25)',
          },
        },
      },
    },
    defaults: {
      VTextarea: {
        variant: 'outlined',
      },
      VTextField: {
        variant: 'outlined',
      },
      VAutocomplete: {
        variant: 'outlined',
      },
      VSelect: {
        variant: 'outlined',
      },
      VBtn: {
        variant: 'outlined',
        rounded: 'lg',
      },
      VContainer: {
        style: 'max-width: 1400px',
      },
      VCard: {
        rounded: 'xl',
        width: '100%',
      },
      VTab: {
        rounded: 'xl',
      },
      VListItem: {
        rounded: 'lg',
      },
    },
    display: {
      mobileBreakpoint: 'sm',
    },
  })
  app.vueApp.use(vuetify)
})
