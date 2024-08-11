import { createApp } from 'vue'
import naive from "naive-ui";
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App).use(store).use(router)

app.use(router)
app.use(naive)
app.mount('#app')