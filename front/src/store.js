import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist'

Vue.use(Vuex)

const vuexLocalStorage = new VuexPersist({
  key: 'vuex', // The key to store the state on in the storage provider.
  storage: window.localStorage, // or window.sessionStorage or localForage
  reducer: state => ({
    settings: state.settings,
    user: state.user,
    realm: null,
  })
})

export default new Vuex.Store({
  plugins: [vuexLocalStorage.plugin],
  state: {
    settings: {
      darkTheme: true,
    },
    user: null,
    realm: null,
    connected: 'disconnected'
  },
  getters: {
    getSettings: state => state.settings,
    getUser: state => state.user,
    getUserProfilePicture: state => {
      if (!state.user || !state.user.avatar){
        return state.settings.default_avatar
      }

      return state.user.avatar
    },
    getConnectionState: state => state.connected,
    getRealm: state => state.realm
  },
  mutations: {
    toggleDarkTheme (state, val) {
      state.settings.darkTheme = val
    },
    setConnState (state, newState) {
      state.connected = newState
    },
    updateUserProfilePicture(state, newProfilePicture){
      state.user.avatar = newProfilePicture
    },
    setUser (state, user) {
      state.user = user
    },
    setSettings (state, settings) {
      state.settings = {...state.settings, ...settings}
    },
    setRealm (state, realm) {
      state.realm = realm
    }
  },
  actions: {
    cleanUser(ctx){
      ctx.commit('setUser', null)
    },
    disconnected (ctx) {
      ctx.commit('setConnState', 'disconnected')
    },
    connecting (ctx) {
      ctx.commit('setConnState', 'connecting')
    },
    connected (ctx) {
      ctx.commit('setConnState', 'connected')
    }
  }
})
