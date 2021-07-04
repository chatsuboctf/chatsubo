<template>
  <v-navigation-drawer
      clipped
      app
      floating
      :permanent="!$vuetify.breakpoint.xsOnly"
      color="transparent"
  >
    <!--      color="#1e1e1e"-->
    <!--      :expand-on-hover="!$vuetify.breakpoint.xs"-->
    <!--    <template slot="prepend">-->
    <!--      <v-list-item>-->
    <!--        <v-list-item-content>-->
    <!--          <v-list-item-title>-->
    <!--            <v-layout-->
    <!--                class="py-0"-->
    <!--                justify-center-->
    <!--                align-center-->
    <!--            >-->
    <!--              <h2 id="logo-title">CHATSUBO</h2>-->
    <!--            </v-layout>-->
    <!--          </v-list-item-title>-->
    <!--        </v-list-item-content>-->
    <!--      </v-list-item>-->
    <!--    </template>-->

    <!--    <v-divider/>-->

    <v-list
        dense
        nav
    >
      <span
          v-for="item in drawerItems"
          :key="item.title"
      >
        <v-list-group
            :value="true"
            :color="$store.getters.getSettings.darkTheme ? 'white' : 'rgba(0,0,0,.87)'"
            v-if="item.children"
            class="mt-1"
            no-action
        >
          <template v-slot:activator>
            <v-layout
                align-center
                justify-center
            >
              <v-list-item-icon class="mr-4">
                <v-icon v-text="item.icon"/>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-layout>
          </template>

          <v-list-item
              v-for="(subitem, i) in item.children"
              :key="i"
              class="pl-8"
              :to="subitem.to"
          >
            <v-list-item-icon class="mr-4">
              <v-icon v-text="subitem.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-title v-text="subitem.title"></v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-item
            v-else
            class="mt-1"
            :to="item.to"
            link
        >
          <v-list-item-icon class="mr-4">
            <v-icon v-text="item.icon"/>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title v-text="item.title"/>
          </v-list-item-content>
        </v-list-item>
      </span>
    </v-list>

    <template slot="append">
      <v-card-text
          class="overline text-center"
          style="color: #ccc"
      >
        {{ new Date().getFullYear() }} — <strong>Chatsubo</strong>
      </v-card-text>
    </template>
  </v-navigation-drawer>
</template>

<script>
import backend from "@/backend";

export default {
  name: 'Drawer',
  data: () => {
    return {
      categories: [],
    }
  },
  methods:{
    loadAllCategories(){
      backend.listCategories().then((res) => {
        this.categories = res.categories
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
  },
  beforeMount() {

    this.loadAllCategories()
  },
  computed:{
    drawerItems(){
      let drawerItems = [
        {
          title: 'Home',
          icon: 'mdi-home',
          to: '/home'
        },
        {
          title: 'Tracks',
          icon: 'mdi-webpack',
          children: []
        },
        {
          title: 'Scoreboard',
          icon: 'mdi-podium',
          to: '/scoreboard'
        },
        {
          title: 'Users',
          icon: 'mdi-account-group',
          to: '/users'
        }
      ]

      if (this.tracksChildren.length > 0){
        drawerItems.find(x => x.title === "Tracks").children = this.tracksChildren
      }else{
        drawerItems.find(x => x.title === "Tracks").children.push({
          title: 'Empty', icon: 'mdi-package-variant'
        })
      }


      if (this.$store.getters.getSettings.enable_teams) {
        drawerItems.push(
            {
              title: 'Teams',
              icon: 'mdi-account-supervisor-circle',
              to: '/teams'
            }
        )
      }

      if (this.$store.getters.getUser.admin){
        drawerItems.push(
            {
              title: 'Administration',
              icon: 'mdi-wrench',
              children: [
                {
                  title: 'Tracks',
                  icon: 'mdi-bookshelf',
                  to: '/admin/tracks'
                },
                {
                  title: 'Boxes',
                  icon: 'mdi-webpack',
                  to: '/admin/boxes'
                },
                {
                  title: 'Submissions',
                  icon: 'mdi-flag',
                  to: '/admin/submissions'
                },
                {
                  title: 'Settings',
                  icon: 'mdi-cog',
                  to: '/admin/settings'
                },
              ]
            }
        )
      }
      return drawerItems
    },
    tracksChildren(){
      if (this.categories === undefined){
        return []
      }

      let cats = []

      for (const cat of this.categories){
        cats.push(
            {
              title: cat.name,
              icon: cat.icon,
              to: `/tracks/${cat.slug}`
            },
        )
      }

      return cats
    }

  }
}
</script>

<style scoped>

</style>
