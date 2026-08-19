import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import axios from 'axios'
// import bootstrap from 'bootstrap/dist/css/bootstrap.css'

const app = createApp(App)

app.use(router)
// app.use(axios)
// app.use(bootstrap)

app.mount('#app')
