import { createApp } from 'vue'

//import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';

import BootstrapVue3 from 'bootstrap-vue-3';
import { BootstrapIconsPlugin } from 'bootstrap-icons-vue';
import Maska from 'maska';

import router from './router/router';
import store from './store/store';
import helpers from './utils/helpers';

import App from './App.vue'

const app = createApp(App);
app.use(BootstrapVue3);
app.use(BootstrapIconsPlugin);
app.use(store);
app.use(router);
app.use(helpers);
app.use(Maska);

app.directive('visible', function(el, binding) {
	el.style.visibility = binding.value ? 'visible' : 'hidden';
});
app.mount('#app');
