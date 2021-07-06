<template>
  <v-main>
<!--    :key="$route.fullPath" -->
    <top />
    <drawer/>
    <!--    <router-view id="main-container" @loaded="contentLoaded" style="max-width: 1185px" class="nav-fade"/>-->
    <v-container
        fluid
    >
<!--       -->
      <router-view id="main-container" :key="$route.fullPath" class="nav-fade"  style="max-width: 1185px"/>
<!--      <router-view/>-->
    </v-container>
  </v-main>
</template>

<script>
import Drawer from "@/components/nav/Drawer";
import Top from "@/components/nav/Top";
import $ from "jquery"

export default {
  name: "Container",
  components: {
    Top,
    Drawer
  },
  methods: {
    contentLoaded(){
      $("#main-container").addClass("nav-fade-show")
    }
  },
  updated() {
    setTimeout(function () {
      // next()
      $(".nav-fade").addClass("nav-fade-show")
    }, 400)
  },
  beforeMount() {
    setTimeout(function () {
      // next()
      $(".nav-fade").addClass("nav-fade-show")
    }, 400)
  },
  beforeRouteUpdate: function (to, from, next) {
    setTimeout(function () {
      next()
    }, 100)

    let fadeContainer = $(".nav-fade")

    fadeContainer.removeClass("nav-fade-show")
    fadeContainer.addClass("nav-fade-hide")
  },
}
</script>

<style>
.nav-fade{
  opacity: 0 !important;
  transition: .3s opacity ease-in-out;
}

.nav-fade-hide{
    opacity: 0 !important;
}

.nav-fade-show{
  opacity: 1 !important;
}


</style>
