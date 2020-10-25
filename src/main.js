import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

let next_card_id = 1
Vue.prototype.getCardId = function() {
  let id = next_card_id
  next_card_id = id + 1
  return id
}

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
