<template>
  <v-row no-gutters>
    <v-col>
      <v-card
          color="secondary"
          rounded="lg"
          v-if="!loading"
      >
        <!--          TODO: adapt for light theme-->
        <!--          <v-card>-->
        <!--            <v-toolbar color="primary" dark dense flat>-->
        <!--              <v-toolbar-title class="subtitle-1">-->
        <!--                Global-->
        <!--              </v-toolbar-title>-->
        <!--            </v-toolbar>-->
        <!--            <div class="overline pa-4 pb-0 px-4 grey&#45;&#45;text">-->
        <!--              Style-->
        <!--            </div>-->
        <!--            <v-card-text>-->

        <!--              <v-switch v-model="darkTheme" inset persistent-hint hint="Toggle the dark theme" color="primary darken-1"-->
        <!--                        class="ma-2"-->
        <!--                        label="Dark theme"></v-switch>-->
        <!--            </v-card-text>-->
        <!--          </v-card>-->
        <v-card-title
            class="text-h5"
        >
          Game settings
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col sm="12" md="6" >
              <card-switch
                  selected-color="primary"
                  class="pa-4"
                  title="Enable teams"
                  subtitle="Allow the players to form teams"
                  icon="mdi-account-supervisor-circle"
                  v-model="enableTeams"
              />
            </v-col>
            <v-col sm="12" md="6" >
              <card-switch
                  selected-color="orange"
                  class="pa-4"
                  title="Freeze scoreboard"
                  subtitle="Prevent any new submissions"
                  icon="mdi-snowflake-alert"
                  v-model="freezeScoreboard"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col sm="12" md="6" >
              <card-switch
                  selected-color="primary"
                  class="pa-4"
                  title="Allow registration"
                  subtitle="Allow anyone to create an account from the login page"
                  icon="mdi-account-multiple-plus"
                  v-model="allowRegistration"
              />
            </v-col>
          </v-row>
        </v-card-text>

        <v-layout
            class="pa-4"
            justify-end
        >
          <v-btn
              :color="allowSave ? 'success' : ''"
              :disabled="!allowSave"
              :outlined="!allowSave"
              :loading="saving"
              @click="emitSaveSettings"
          >
            <v-icon
                v-text="'mdi-content-save'"
                class="mr-2"
            />
            Save
          </v-btn>

        </v-layout>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import CardSwitch from "../../CardSwitch";

export default {
  components: {
    CardSwitch
  },
  name: "GameAdminSettings",
  data() {
    return {
      enableTeams: this.$store.getters.getSettings.enable_teams,
      freezeScoreboard: this.$store.getters.getSettings.freeze_scoreboard,
      allowRegistration: this.$store.getters.getSettings.allow_registration,
      originalSettings: null,
      localSettings: null,
      allowSave: false,
      allowSubmissions: false,
      showBottomSaveSnackbar: false,
    }
  },
  computed: {},
  methods: {
    loadAccessSettings(settings) {
      this.originalSettings = JSON.parse(JSON.stringify(settings))
      this.localSettings = JSON.parse(JSON.stringify(settings))
      this.settings = JSON.parse(JSON.stringify(settings))
    },
    emitSaveSettings() {
      this.$emit('saved', {
        enable_teams: this.enableTeams,
        freeze_scoreboard: this.freezeScoreboard,
        allow_registration: this.allowRegistration
      })
      this.loadAccessSettings(this.localSettings)
    },
  },
  beforeMount() {
    this.loadAccessSettings(this.$store.getters.getSettings)
  },
  watch: {
    localSettings: {
      handler(val) {
        this.allowSave = JSON.stringify(val) !== JSON.stringify(this.originalSettings)
      },
      deep: true
    },
    enableTeams(val) {
      this.localSettings.enable_teams = val
    },
    freezeScoreboard(val) {
      this.localSettings.freeze_scoreboard = val
    },
    allowRegistration(val) {
      this.localSettings.allow_registration = val
    },
  },
  props: {
    loading: Boolean,
    saving: Boolean,
  }
}
</script>

<style scoped>

</style>
