import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import router from './router'
import store from './store'

import './filters'

// import VueSocketIOExt from 'vue-socket.io-extended'
// import io from 'socket.io-client'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
// import colors from 'vuetify/lib/util/colors'
import dark from '@/plugins/vuetify/theme'
import 'vue-toast-notification/dist/theme-sugar.css'
import VueToast from 'vue-toast-notification'
import VueClipboard from 'vue-clipboard2'
import VueCookies from 'vue-cookies'
import auth from "@/lib/auth"
import settings from "./lib/settings";

Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(VueToast, {
  position: 'top-right'
})
Vue.use(VueClipboard)
Vue.use(VueCookies)

// let socketBackendURL = "http://localhost:5000"

// const socket = io(socketBackendURL)

// Vue.use(VueSocketIOExt, socket, { store })

// Uncomment to disable console.log in prod
// window['console']['log'] = function() {};

const vuetifyOptions = {
  theme: {
    options: {
      customProperties: true
    },
    dark: store.getters.getSettings.darkTheme,
    themes: {
      dark
      // light: {
      //   primary: colors.lightBlue.darken2, // #E53935
      //   // primary: colors.blue, // #E53935
      //   // secondary: colors.deepOrange.lighten4, // #FFCDD2
      //   // accent: colors.pink.darken1 // #3F51B5
      //   accent: colors.pink // #3F51B5
      // },
      // dark: {
      //   primary: "#16222e",
      //   // background: "#1C2B3B", // #3F51B5
      //   background: "#ffffff"
      // }
    },
  }
}

Vue.prototype.$mapProgressionToIcon = (done, max) => {
  const percentage = ((done/max) * 100).toFixed(3)
  let sliceIndex = parseInt(percentage.slice(0, -1), 10)

  if(done === max){
    sliceIndex = 80
  }else if (sliceIndex > 80 && done < max){
    sliceIndex = 70
  }else if (done === 0){
    return 'mdi-circle-outline'
  }

  return `mdi-circle-slice-${(sliceIndex - 1).toString().charAt(0)}`
}

Vue.prototype.$mapValueToDifficulty = (val) => {
  let difficulty = {
    text: "Easy",
    icon: "mdi-baby",
    color: "green",
  }

  if (val > 1 && val <= 3) {
    difficulty = {
      text: "Piece of cake",
      icon: "mdi-cupcake",
      color: "light-blue",
    }
  }else if (val > 3 && val <= 5){
    difficulty = {
      text: "Medium",
      icon: "mdi-altimeter",
      color: "yellow",
    }
  }else if (val > 5 && val <= 7){
    difficulty = {
      text: "Hard",
      icon: "mdi-sword-cross",
      color: "red",
    }
  }else if (val > 7 && val <= 9){
    difficulty = {
      text: "Epic",
      icon: "mdi-skull-scan",
      color: "purple",
    }
  }else if (val > 9) {
    difficulty = {
      text: "Legendary",
      icon: "mdi-hexagon-slice-6",
      color: "orange",
    }
  }
  return difficulty
}

Vue.prototype.$mapOSToIcon = (os) => {
  if (os === undefined){
    return ""
  }

  let icon = ""

  switch (os.toLowerCase()){
    case "windows":
      icon = "mdi-microsoft-windows"
      break
    case "linux":
      icon = "mdi-linux"
      break
    case "openbsd":
      icon = "mdi-freebsd"
      break
    default:
      icon = "mdi-laptop"
  }

  return icon
}


Vue.prototype.$mapScoreToRank = (score) => {
  let rank = {
    text: "Newbie",
    icon: "mdi-baby-carriage",
    color: "#03A9F4"
  }

  if (score > 25 && score <= 250) {
    rank = {
      text: "Student",
      icon: "mdi-baby",
      color: "#4CAF50"
    }
  }else if (score > 250 && score <= 500) {
    rank = {
      text: "Hacker",
      icon: "mdi-pirate",
      color: "#4CAF50"
    }
  }else if (score > 500 && score <= 750) {
    rank = {
      text: "1337",
      icon: "mdi-eye-circle",
      color: "#4CAF50"
    }
  }else if (score > 750 && score <= 1000) {
    rank = {
      text: "Guru",
      icon: "mdi-cat",
      color: "#4CAF50"
    }
  }

  return rank
}

Vue.prototype.$randStr = (n) => {
  let result           = [];
  let charset       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let charslen = charset.length;

  for ( let i = 0; i < n; i++ ) {
    result.push(charset.charAt(Math.floor(Math.random() * charslen)));
  }

  return result.join('');
}

Vue.prototype.$nameToSlug = (name) => {
  return name.replace(/[^àâäéèêëïîôöùûüÿça-z0-9]/gi, '_').toLowerCase();
}

String.prototype.toProperCase = function () {
  return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

Vue.config.productionTip = false

// TODO: set secure, only https
Vue.$cookies.config('7d','','',false)

router.beforeEach((to, from, next) => {
  auth.checkSession(Vue.$cookies.get("CHATSUBO-SESSION")).then((user) => {
    let is_admin = false

    if (to.meta.requireAuth){
      if (!user || !store.getters.getUser || user.email !== store.getters.getUser.email) {
        store.dispatch("cleanUser")
        Vue.$cookies.set("CHATSUBO-SESSION", "")
        next({name: 'login'})
        return
      }

      is_admin = user.admin

      if (to.meta.requireAdmin) {
        if (!user.admin){
          next({name: 'home'})
          return
        }
      }
    }

    store.commit("setUser", user)

    settings.fetchSettings().then((appSettings) => {
      if (!appSettings){
        this.$toast.error("Failed to load settings")
        // next({name: 'home'})
        return
      }

      store.commit("setSettings", appSettings)

      let allowedNotStarted = [
        "home",
        "login",
        "logout"
      ]

      if (!is_admin && appSettings.enforce_access_restriction && (!appSettings || appSettings.state !== "is_live") && !allowedNotStarted.includes(to.name)){
        // Should never show up
        let msg = "Access restricted"

        switch (appSettings.state){
          case "not_started":
            msg = "The game has not started yet"
            break
          case "has_ended":
            msg = "The game has ended"
            break
        }
        Vue.$toast.info(msg)
        next({name: 'home'})
        return
      }

      if (to.path === "/register" && !appSettings.allow_registration){
        Vue.$toast.error("Registration have been deactivated")
        next({name: 'login'})
        return
      }

      if (to.meta.requireAuth && !store.getters.getUser){
        Vue.$cookies.set("CHATSUBO-SESSION", "")
        next({name: 'login'})
        return
      }

      next()
    })
  })

})

new Vue({
  router,
  store,
  vuetify: new Vuetify(vuetifyOptions),
  render: h => h(App)
}).$mount('#app')
