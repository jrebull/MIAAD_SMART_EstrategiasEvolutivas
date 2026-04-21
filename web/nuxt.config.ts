// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2026-04-21',
  devtools: { enabled: true },
  ssr: true,

  modules: ['@nuxtjs/tailwindcss'],

  css: ['~/assets/css/main.css', 'katex/dist/katex.min.css'],

  app: {
    // baseURL: '/MIAAD_SMART_EstrategiasEvolutivas/', // descomentar si se despliega en GitHub Pages
    head: {
      htmlAttrs: { lang: 'es' },
      title: 'EE: Isotropía vs Anisotropía — MIAAD UACJ',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Resultados interactivos de la práctica de Estrategias Evolutivas: Isotropía vs Anisotropía — Optimización Inteligente, MIAAD, UACJ.'
        },
        { property: 'og:title', content: 'EE: Isotropía vs Anisotropía — MIAAD UACJ' },
        { property: 'og:type', content: 'website' }
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }
      ]
    }
  },

  nitro: {
    prerender: {
      routes: ['/', '/problem', '/results', '/convergence', '/sigma', '/conclusions']
    }
  },

  typescript: {
    strict: true
  }
})
