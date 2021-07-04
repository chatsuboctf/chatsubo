<template>
  <!--  <v-row-->
  <!--      class="column"-->
  <!--      no-gutters-->
  <!--  >-->
  <!--    <v-col-->
  <!--        class="pt-2 flex-column"-->
  <!--        sm="12"-->
  <!--    >-->
  <!--      <v-container fill-height fluid class="pa-0 cover-fill">-->
  <v-app-bar
      clipped-left
      app
      style="opacity: 1 !important;"
      color="secondary"
      elevation="0"
  >
    <v-app-bar-title
    >
      <v-layout
          class="py-0"
          justify-center
          align-center
          :width=$store.getters.getSettings.logo_width
      >
        <v-card
            class="pa-2"
            elevation="6"
            :width=$store.getters.getSettings.logo_width
            color="transparent"
            to="/"
            :ripple="false"
        >
          <v-img
              :src=$store.getters.getSettings.logo
              :max-height=$store.getters.getSettings.logo_height
              :lazy-src="null"
              contain
              style="opacity: .95"
              position="top"
              class="white--text pa-0 ma-0"
          />
        </v-card>
      </v-layout>
    </v-app-bar-title>
    <v-spacer />
    <v-chip-group>
      <v-chip
          v-if="$store.getters.getSettings.freeze_scoreboard"
          color="orange"
      >
        <v-icon
            class="mr-1"
            v-text="'mdi-snowflake-alert'"
        />
        Frozen scoreboard
      </v-chip>
      <v-chip
          v-if="$store.getters.getSettings.enforce_access_restriction && $store.getters.getSettings.state !== 'is_live'"
          color="secondaryLighter"
      >
        <v-icon
            class="mr-1"
            v-text="'mdi-calendar'"
        />
        The game has not started yet
      </v-chip>
    </v-chip-group>
    <v-menu
        transition="slide-y-transition"
        bottom
        offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-card
            v-bind="attrs"
            v-on="on"
            elevation="0"
            class="px-4 py-1"
            rounded="lg"
            color="transparent"
        >
          <v-layout
              justify-center
              align-center
          >
            <div class="pr-4">
              <v-layout
                  align-end
                  justify-center
                  column
              >
                <span class="float-right" v-text="$store.getters.getUser.username"/>
                <span
                    class="text-caption"
                    :style="`color: ${$store.getters.getSettings.darkTheme ? 'rgba(255, 255, 255,.7)' : 'rgba(0,0,0,.87)'}`"
                    v-text="`${$store.getters.getUser.score} pts`"
                />

              </v-layout>
              <!--            <div class="text-caption" style="color: rgba(255, 255, 255,.7)" v-text="$mapScoreToRank($store.getters.getUser.score).text"/>-->
            </div>
            <v-avatar
                rounded="lg"
            >
              <!--                <v-tooltip-->
              <!--                    transition="slide-fade-transition"-->
              <!--                    left-->
              <!--                >-->
              <!--                  <template v-slot:activator="{ on, attrs }">-->
              <!--                    <div-->
              <!--                        style="position:absolute; bottom: -10px; right: 0;"-->
              <!--                        v-bind="attrs"-->
              <!--                        v-on="on"-->
              <!--                    >-->

              <!--                      <status-indicator-->
              <!--                          :negative="isDisconnected"-->
              <!--                          :positive="isConnected"-->
              <!--                          :intermediary="isConnecting"-->
              <!--                          :pulse="isConnecting"/>-->
              <!--                    </div>-->
              <!--                  </template>-->
              <!--                  <span>{{ connStateText }}</span>-->
              <!--                </v-tooltip>-->
              <!--          <v-icon v-if="!$store.getters.getUserProfilePicture" dark v-text="'mdi-account-circle'"/>-->
              <v-img
                  :src="$store.getters.getUserProfilePicture"
              />
            </v-avatar>
          </v-layout>
        </v-card>

      </template>
      <v-list
          color="secondary"
      >
        <v-list-item
            v-for="item in profileMenuItems"
            :key="item.title"
            :to="item.to"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="item.title"></v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
// import {StatusIndicator} from 'vue-status-indicator'

export default {
  name: 'Top',
  components: {
    // StatusIndicator
  },
  data() {
    return {
    }
  },
  computed: {
    profileMenuItems(){
      let items = [
        // {title: 'Profile', icon: 'mdi-account-circle', to: `/profile/${this.$store.getters.getUser.username}`},
        {title: 'Settings', icon: 'mdi-cog', to: '/settings'},
        {title: 'Logout', icon: 'mdi-logout-variant', to: '/logout'},
      ]

      if (this.$store.getters.getSettings.enable_teams) {
        items.unshift({
          title: 'Team',
          icon: 'mdi-account-multiple',
          to: `/team/${this.$store.getters.getUser.team ? this.$store.getters.getUser.team.id : 'join'}`
        })
      }

      return items
    },
    isConnected() {
      return this.$store.getters.getConnectionState === 'connected'
    },
    isConnecting() {
      return this.$store.getters.getConnectionState === 'connecting'
    },
    isDisconnected() {
      return this.$store.getters.getConnectionState === 'disconnected'
    },
    connStateText() {
      let state = 'Disconnected'
      switch (this.$store.getters.getConnectionState) {
        case 'connected':
          state = 'Connected'
          break
        case 'disconnected':
          state = 'Disconnected'
          break
        case 'connecting':
          state = 'Connecting...'
          break
      }
      return state
    },
    crumbs() {
      let crumbs = []
      for (const match of this.$router.currentRoute.matched) {
        if (Object.keys(match.meta).length) {
          crumbs.push({
            text: match.meta.title || match.name,
            disabled: false,
            href: match.meta.crumbLink || match.matchAs,
            large: true
          })
        }
      }
      return crumbs
    }
  }
}
</script>

<style scoped>
.connected-color {
  color: green;
}

.disconnected-color {
  color: crimson;
}

.connecting-color {
  color: orange;
}

</style>
