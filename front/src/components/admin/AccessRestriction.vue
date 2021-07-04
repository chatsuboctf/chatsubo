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
          <v-row
              justify-center
              align-center
          >
            <v-col sm="12" md="4" >
              Plateform availability
            </v-col>
            <v-col sm="12" md="8" >
              <card-switch
                  selected-color="primary"
                  class="pa-4"
                  title="Restrict access to challenges"
                  subtitle="Only the home page will be accessible"
                  icon="mdi-calendar"
                  v-model="enforce"
              />
            </v-col>
          </v-row>
        </v-card-title>
        <v-form
            @submit.prevent=""
        >
          <v-card-text>
            <v-row>
              <v-layout
                  justify-center
                  align-center
              >
                <v-col sm="12" md="5">
                  <v-layout
                      column
                      justify-center
                      align-center
                  >
                    <!--                        :disabled="!settings.enforce_access_restriction"-->
                    <v-date-picker
                        elevation="6"
                        v-model="notBeforeDate"
                        @input="showMenuOpenStart = false"
                        color="secondaryLighter"
                        class="mb-6"
                    />
                    <!--                        :disabled="!settings.enforce_access_restriction"-->
                    <v-time-picker
                        format="24hr"
                        elevation="6"
                        scrollable
                        color="secondaryLighter"
                        v-model="notBeforeTime"
                    />
                  </v-layout>
                </v-col>
                <v-col md="1">
                  <v-layout
                      fill-height
                      justify-center
                      align-center
                  >
                    <v-icon
                        v-text="'mdi-chevron-double-right'"
                    />
                  </v-layout>
                </v-col>
                <v-col sm="12" md="5">
                  <v-layout
                      justify-center
                      align-center
                      column
                  >
                    <!--                        :disabled="!settings.enforce_access_restriction"-->
                    <v-date-picker
                        color="secondaryLighter"
                        elevation="6"
                        v-model="notAfterDate"
                        @input="showMenuOpenStart = false"
                        class="mb-6"
                    />
                    <!--                        :disabled="!settings.enforce_access_restriction"-->
                    <v-time-picker
                        format="24hr"
                        elevation="6"
                        scrollable
                        color="secondaryLighter"
                        v-model="notAfterTime"
                    />
                  </v-layout>
                </v-col>
              </v-layout>
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
        </v-form>
      </v-card>
      <v-card v-else>
        <v-progress-circular indeterminate />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import CardSwitch from "../../components/CardSwitch";

export default {
  name: "AdminAccessRestriction",
  components:{
    CardSwitch,
  },
  data () {
    return {
      allowSave: false,
      enforce: this.$store.getters.getSettings.enforce_access_restriction,
      originalSettings: null,
      settings: null,
      localSettings: null,
      notBeforeTime: this.$store.getters.getSettings.not_before ? new Date(this.$store.getters.getSettings.not_before+"Z") : new Date(0),
      notAfterTime: this.$store.getters.getSettings.not_after ? new Date(this.$store.getters.getSettings.not_after+"Z") : new Date(0),
      notBeforeDate: this.makeNotBeforeDate(),
      notAfterDate: this.makeNotAfterDate(),
    }
  },
  methods:{
    makeNotBeforeDate(){
      let defaultDate = new Date()
      let date = this.$store.getters.getSettings.not_before ? new Date(this.$store.getters.getSettings.not_before) : defaultDate
      return date.toISOString().substr(0, 10)
    },
    makeNotAfterDate(){
      let defaultDate = new Date()
      let date = this.$store.getters.getSettings.not_after ? new Date(this.$store.getters.getSettings.not_after) : defaultDate
      return date.toISOString().substr(0, 10)
    },
    emitSaveSettings(){
      if (this.notBefore > this.notAfter){
        this.$toast.error("Start date cannot be greater then end date")
        return
      }
      this.$emit('saved', {notBefore: this.notBefore, notAfter: this.notAfter, enforce: this.enforce})
      this.loadAccessSettings(this.localSettings)
    },
    loadAccessSettings(settings){
      this.originalSettings = JSON.parse(JSON.stringify(settings))
      this.localSettings = JSON.parse(JSON.stringify(settings))
      this.settings = JSON.parse(JSON.stringify(settings))
    }
  },
  beforeMount() {
    this.loadAccessSettings(this.$store.getters.getSettings)
  },
  computed:{
    notBefore(){
      if (Object.prototype.toString.call(this.notBeforeTime) === '[object String]'){
        return new Date(this.notBeforeDate +" "+ this.notBeforeTime)
      }else{
        let date = new Date(this.notBeforeDate)
        let hours = this.notBeforeTime.getHours()
        let minutes = this.notBeforeTime.getMinutes()
        date.setMinutes(minutes)
        date.setHours(hours)
        return date
      }
    },
    notAfter(){
      if (Object.prototype.toString.call(this.notAfterTime) === '[object String]'){
        return new Date(this.notAfterDate +" "+ this.notAfterTime)
      }else{
        let date = new Date(this.notAfterDate)
        let hours = this.notAfterTime.getHours()
        let minutes = this.notAfterTime.getMinutes()
        date.setMinutes(minutes)
        date.setHours(hours)
        return date
      }
    },
  },
  watch:{
    localSettings: {
      handler (val) {
        this.allowSave = JSON.stringify(val) !== JSON.stringify(this.originalSettings)
      },
      deep: true
    },
    enforce(val){
      this.localSettings.enforce_access_restriction = val
    },
    notBeforeDate(val){
      let newDate = new Date(val)
      let year = newDate.getFullYear()
      let month = newDate.getMonth()
      let day = newDate.getDate()
      let date = new Date(this.localSettings.not_before)
      date.setFullYear(year)
      date.setMonth(month)
      date.setDate(day)
      this.localSettings.not_before = date.toISOString()
    },
    notAfterDate(val){
      let newDate = new Date(val)
      let year = newDate.getFullYear()
      let month = newDate.getMonth()
      let day = newDate.getDate()
      let date = new Date(this.localSettings.not_after)
      date.setFullYear(year)
      date.setMonth(month)
      date.setDate(day)
      this.localSettings.not_after = date.toISOString()
    },
    notBeforeTime(val){
      let chunks = val.split(":")
      let hours = chunks[0]
      let minutes = chunks[1]
      let date = new Date(this.localSettings.not_before)
      date.setMinutes(minutes)
      date.setHours(hours)
      this.localSettings.not_before = date.toISOString()
    },
    notAfterTime(val){
      let chunks = val.split(":")
      let hours = chunks[0]
      let minutes = chunks[1]
      let date = new Date(this.localSettings.not_after)
      date.setMinutes(minutes)
      date.setHours(hours)
      this.localSettings.not_after = date.toISOString()
    }
  },
  props:{
    loading: Boolean,
    saving: Boolean,
  },
}
</script>

<style scoped>

</style>
