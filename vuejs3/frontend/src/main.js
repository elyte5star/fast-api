import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

//Global options
const options = {
    confirmButtonColor: '#41b882',
    cancelButtonColor: '#ff7674',
};



const app = createApp(App);
app.use(VueSweetalert2,options);
app.use(createPinia());
app.use(router);
app.mount('#app');
//createApp(App).use(router).mount('#app')
