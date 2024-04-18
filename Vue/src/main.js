import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router/index.js'
import ElementPlus from 'element-plus'
import Tmap from '@map-component/vue-tmap'
import { createPinia } from 'pinia'

import 'element-plus/dist/index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Tmap)
app.use(ElementPlus)

app.mount('#app')
