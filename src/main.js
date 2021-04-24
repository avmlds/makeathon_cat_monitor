import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

import * as VueGoogleMaps from "vue2-google-maps";

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyDE3JFZhub_2bn11RgujwGPP5z_mjRR4hE",
    libraries: "places", // necessary for places input
    region: "ru"
  }
});

Vue.use(Buefy)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
