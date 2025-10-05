
import './assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'

import router from './router'

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import InputText from 'primevue/inputtext';
import Slider from 'primevue/slider';
import Button from 'primevue/button';

const app = createApp(App)

app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});

app.component('InputText', InputText);
app.component('Slider', Slider)
app.component('Button', Button);

app.mount('#app')
