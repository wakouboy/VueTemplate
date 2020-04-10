// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'jquery'

Vue.config.productionTip = false
import api from './api/index.js'
Vue.prototype.$api = api

var buildCodes = false
import $ from 'jquery'
window.$ = $

// buildCodes = true

{
  window.CommunicateWithServer = function(type, paramsObj, url, callback) {
    if (buildCodes) {
      paramsObj = JSON.stringify(paramsObj)
      $.ajax({
        type: type,
        url: url,
        data: { 'params': paramsObj },
        dataType: "json",
        success: function(data) {
          callback(data);
        },
        error: function(err) {
          callback(err)
        }
      })
    } else {
      let formData = new URLSearchParams();
      formData.append("params", JSON.stringify(paramsObj));
      if (type == 'get') {
        api.get(url, formData, data => {
          callback(data)
        }, error => {
          callback(error)
        })
      } else if (type == 'post') {
        api.post(url, formData, data => {
          callback(data)
        }, error => {
          callback(error)
        })
      }
    }
  }
}


// import Vuetify from 'vuetify'
// import 'vuetify/dist/vuetify.min.css'
// Vue.use(Vuetify)

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)


import { library } from '@fortawesome/fontawesome-svg-core'
import { faUpload } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUpload)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
import * as d3 from "d3"
window.d3 = d3

import store from './store/index.js';
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
