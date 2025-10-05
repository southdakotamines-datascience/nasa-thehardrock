import './assets/main.css'
import 'leaflet/dist/leaflet.css'
import Primevue from 'primevue/config'

import { createApp } from 'vue'

import App from './App.vue'

import router from './router'

const app = createApp(App)

app.use(Primevue)
app.use(router)

app.mount('#app')
