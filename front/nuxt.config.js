const API_URL = "http://127.0.0.1:8000";

export default {
  /*
   ** Nuxt rendering mode
   ** See https://nuxtjs.org/api/configuration-mode
   */
  ssr: false,
  /*
   ** Nuxt target
   ** See https://nuxtjs.org/api/configuration-target
   */
  target: "server",
  server: {
    port: 3002, // default: 3000
    host: "0.0.0.0" // default: localhost
  },
  /*
   ** Headers of the page
   ** See https://nuxtjs.org/api/configuration-head
   */
  router: {
    linkActiveClass: "active-link",
    linkExactActiveClass: "exact-active-link"
  },
  loading: false,
  head: {
    title: "Testing system",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      {
        hid: "description",
        name: "description",
        content: process.env.npm_package_description || ""
      }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },
  /*
   ** Global CSS
   */
  css: ["~/static/font/stylesheet.css", "~/assets/my_style/main.scss"],
  /*
   ** Plugins to load before mounting the App
   ** https://nuxtjs.org/guide/plugins
   */
  plugins: [
    "~/plugins/vue-plyr",
    { src: "~/plugins/vue-inputmask", ssr: false },
    { src: "~/plugins/v-calendar", ssr: false },
    // { src: "~/plugins/axios-handler", ssr: false },
    { src: "~/plugins/vuejs-countdown-timer", ssr: false }
  ],
  /*
   ** Auto import components
   ** See https://nuxtjs.org/api/configuration-components
   */
  components: true,
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [],
  /*
   ** Nuxt.js modules
   */
  modules: [
    "vue-toastification/nuxt",
    // Doc: https://bootstrap-vue.js.org
    "bootstrap-vue/nuxt",
    // Doc: https://axios.nuxtjs.org/usage
    "@nuxtjs/axios",
    ["nuxt-sass-resources-loader"],
    "@nuxtjs/dayjs"
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    baseURL: `${API_URL}/api/v1`
  },

  dayjs: {
    locales: ["ru"],
    defaultLocale: "ru",
    plugins: [
      "utc" // import 'dayjs/plugin/utc'
    ] // Your Day.js plugin
  },

  /*
   ** Build configuration
   ** See https://nuxtjs.org/api/configuration-build/
   */
  build: {
    extractCSS: true,
    cssSourceMap: false
  }
};
