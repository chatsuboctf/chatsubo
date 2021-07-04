<template>
  <v-app
      :style="{background: $vuetify.theme.themes.dark.background}"
  >
    <!--    <top :key="$route.fullPath" />-->
    <!--    <drawer/>-->
    <router-view/>
    <socket-handler/>
  </v-app>
</template>

<script>
// import Drawer from '@/components/nav/Drawer'
// import Top from '@/components/nav/Top'
import SocketHandler from '@/components/SocketHandler'

export default {
  components: {
    SocketHandler,
    // Top,
    // Drawer
  },
  sockets: {
    connect () {
      this.$store.dispatch('connected')
    },
    disconnect () {
      this.$store.dispatch('disconnected')
    },
    connecting () {
      this.$store.dispatch('connecting')
    },
    reconnecting () {
      this.$store.dispatch('connecting')
    }
  },
}
</script>

<style>
#logo-title{
  font-family: 'Righteous', cursive;
  font-size: 2em;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}

.notices .toast-success {
  background-color: #4caf50 !important;
}

.bottom-spacer{
  width: 100%;
  height: 50vh;
}

</style>
