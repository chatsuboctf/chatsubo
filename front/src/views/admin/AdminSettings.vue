<template>
  <v-container
      color="transparent"
      fluid
  >
    <!--            color="primary darken-2"-->
    <v-sheet
        color="transparent"
        style="position: absolute"
        height="200px"
        width="100%"
    >
      <v-card-title
          class="headline text-h4 font-weight-bold"
      >
        Admin settings
      </v-card-title>
    </v-sheet>

    <v-container fluid style="margin-top: 80px">
      <v-tabs
          v-if="!isLoading"
          v-model="tab"
          class="py-2"
          background-color="transparent"
          dark
          color="white"
      >
        <v-tab
            v-for="item in settingsTabs"
            :key="item"
        >
          {{ item }}
        </v-tab>
      </v-tabs>

      <v-tabs-items
          v-model="tab"
          style="background: transparent"
      >
        <v-tab-item
            key="Game"
        >
          <game-admin-settings
              :loading="isLoading"
              :saving="saveCurrentSettingsLoader"
              @saved="updateGameSettings"
          />
        </v-tab-item>

        <v-tab-item
            key="Users"
        >
          <users-admin-settings/>
        </v-tab-item>

        <v-tab-item
            key="Access"
        >
          <admin-access-restriction
              :loading="isLoading"
              :saving="saveCurrentSettingsLoader"
              @saved="updateRestrictionSettings"
          />
        </v-tab-item>

        <v-tab-item
            key="Home"
        >
          <home-settings/>
        </v-tab-item>


        <v-tab-item
            key="Appearance"
        >
          <appearance/>
        </v-tab-item>
      </v-tabs-items>
      <!--      <v-row no-gutters>-->
      <!--        <v-col sm="12" md="8">-->
      <!--          <v-card-->
      <!--              color="secondary"-->
      <!--              rounded="lg"-->
      <!--              v-if="!isLoading"-->
      <!--          >-->
      <!--            &lt;!&ndash;          TODO: adapt for light theme&ndash;&gt;-->
      <!--          <v-card>-->
      <!--            <v-toolbar color="primary" dark dense flat>-->
      <!--              <v-toolbar-title class="subtitle-1">-->
      <!--                Global-->
      <!--              </v-toolbar-title>-->
      <!--            </v-toolbar>-->
      <!--            <div class="overline pa-4 pb-0 px-4 grey--text">-->
      <!--              Style-->
      <!--            </div>-->
      <!--            <v-card-text>-->

      <!--              <v-switch v-model="darkTheme" inset persistent-hint hint="Toggle the dark theme" color="primary darken-1"-->
      <!--                        class="ma-2"-->
      <!--                        label="Dark theme"></v-switch>-->
      <!--            </v-card-text>-->
      <!--          </v-card>-->
      <!--          </v-card>-->
      <!--          <v-card v-else>-->
      <!--            <v-progress-circular indeterminate />-->
      <!--          </v-card>-->
      <!--        </v-col>-->
      <!--      </v-row>-->
      <update-snackbar
          v-model="showBottomSaveSnackbar"
          :allow-save="showBottomSaveSnackbar"
          :loading="saveCurrentSettingsLoader"
          @save="saveCurrentSettings"
          @reset="restoreSettings"
      />
    </v-container>
  </v-container>
</template>

<script>
import UpdateSnackbar from "@/components/interactive/UpdateSnackbar";
import backend from "@/backend";
import Appearance from "@/components/admin/appearance/Appearance";
import HomeSettings from "@/components/admin/home/HomeSettings";
import GameAdminSettings from "@/components/admin/game/GameAdminSettings";
import AdminAccessRestriction from "@/components/admin/AccessRestriction";
import UsersAdminSettings from "@/components/admin/users/UsersAdminSettings";

export default {
  name: "Settings",
  components:{
    UpdateSnackbar,
    AdminAccessRestriction,
    UsersAdminSettings,
    Appearance,
    HomeSettings,
    GameAdminSettings,
    // CardSwitch
  },
  data () {
    return {
      tabMapping: {
        "game": 0,
        "users": 1,
        "access": 2,
        "home": 3,
        "appearance": 4
      },
      tab: null,
      settingsTabs:[
        "Game",
        "Users",
        "Access",
        "Home",
        "Appearance"
      ],
      availability: {
        start: this.$store.state.settings.not_before ? this.$store.state.settings.not_before : "",
        end: this.$store.state.settings.not_after ? this.$store.state.settings.not_after : ""
      },
      enableCalendars: false,
      showMenuOpenStart: false,
      showMenuOpenEnd: false,
      showBottomSaveSnackbar: false,
      saveCurrentSettingsLoader: false,
    }
  },
  methods:{
    updateGameSettings(gameSettings){
      let data = {
        "enable_teams": gameSettings.enable_teams,
        "freeze_scoreboard": gameSettings.freeze_scoreboard,
        "allow_registration": gameSettings.allow_registration
      }

      this.saveCurrentSettingsLoader = true

      backend.editGameSettings(data)
          .then(() => {
            this.$toast.success("Settings saved successfully")
            this.$store.commit("setSettings", data)
          }).catch(() => {
        this.$toast.error(`Failed to save settings`, {duration: 10000})
      }).finally(() => {
        this.saveCurrentSettingsLoader = false
      })
    },
    updateRestrictionSettings(restrictionSettings){
      let data = {
        "not_before": restrictionSettings["notBefore"],
        "not_after": restrictionSettings["notAfter"],
        "enforce_access_restriction": restrictionSettings["enforce"]
      }

      this.saveCurrentSettingsLoader = true

      backend.editAccessSettings(data)
          .then(() => {
            this.$toast.success("Settings saved successfully")
            this.$store.commit("setSettings", data)
          }).catch(() => {
        this.$toast.error(`Failed to save settings`, {duration: 10000})
      }).finally(() => {
        this.saveCurrentSettingsLoader = false
      })
    },
    checkNewPasswdConfirmation(){
      return this.user.newPassword.slice(0, this.user.newPasswordConfirmation.length) === this.user.newPasswordConfirmation
    },
    restoreSettings () {
      this.showBottomSaveSnackbar = false
      this.user = JSON.parse(JSON.stringify(this.originalUser))
    },
    saveCurrentSettings () {
      this.saveCurrentSettingsLoader = true
      console.log(this.user)

      backend.editUserSelf(this.user).then((res) => {
        if (res.data.errors.length > 0){
          this.$toast.error(res.data.errors.join(" / "))
          return
        }

        this.$toast.success("Settings updated")
        this.$store.commit("setUser", this.user)
      }).catch((res) => {
        if (res.data){
          this.$toast.error(res.data.errors.join(" / "))
        }else if(res.response.status === 401){
          this.$toast.error("Unauthorized")
        }else{
          this.$toast.error(res.response.data.message)
        }
      }).finally(() => {
        this.showBottomSaveSnackbar = false
        this.saveCurrentSettingsLoader = false
        this.originalUser = JSON.parse(JSON.stringify(this.user))
      })
    },
  },
  computed:{
    isLoading(){
      return this.user === null
    },
    darkTheme: {
      get () {
        return this.$store.state.settings.darkTheme
      },
      set (value) {
        this.$vuetify.theme.dark = !this.$vuetify.theme.dark
        this.$store.commit('toggleDarkTheme', value)
      }
    },
  },
  watch: {
    user: {
      handler (val) {
        if (this.user.newPassword.length > 0 || this.user.password.length > 0){
          if (this.user.newPassword.length === 0 || this.user.newPasswordConfirmation !== this.user.newPassword){
            this.showBottomSaveSnackbar = false
            return
          }
        }

        this.showBottomSaveSnackbar = JSON.stringify(val) !== JSON.stringify(this.originalUser)
      },
      deep: true
    },

  },
  beforeMount() {
    if (this.$route.params.tab === undefined){
      this.tab = 0
      return
    }

    this.tab = this.tabMapping[this.$route.params.tab.toLowerCase()]
  },
  mounted() {
    let base = this.$store.getters.getUser
    base.newPasswordConfirmation = ""
    base.newPassword = ""
    this.originalUser = JSON.parse(JSON.stringify(base))

    this.user = JSON.parse(JSON.stringify(base))
  }
}
</script>

<style scoped>

</style>
