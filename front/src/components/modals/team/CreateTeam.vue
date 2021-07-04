<template>
  <v-dialog
      v-model="show"
      transition="fade-transition"
      @keydown.ctrl.enter="createTeam"
      @click:outside="$emit('click:outside')"
      max-width="650"
  >
    <v-card
        color="secondaryLighter"
    >
      <v-container class="px-6">
        <v-layout
            fill-height
            justify-space-around
            align-center
        >
          <v-form
              @submit="createTeam"
              style="width: 100%;"
              class="fill-height">
            <v-card-title class="px-0">
              <v-layout
                  justify-space-between
                  align-start
              >
                <v-layout
                    column
                >
                  Create team
                  <v-text-field
                      v-model="team.name"
                      label="Name"
                      autofocus
                      :rules="[() => !!team.name || 'This field is required']"
                      counter="200"
                      required
                  />
                  <v-text-field
                      v-model="team.password"
                      :rules="[() => !!team.password || 'This field is required']"
                      label="Password"
                      type="password"
                  />
                  <v-text-field
                      v-model="passwordConfirmation"
                      :rules="[() => !!team.password || 'This field is required', checkPasswdConfirmation || 'Password confirmation does not match']"
                      label="Password confirmation"
                      type="password"
                  />
                </v-layout>
                <v-spacer/>
                <v-card
                    flat
                    class="ma-2"
                >
                  <team-card
                      :team="team"
                      with-stats
                      flat
                  />
                </v-card>
              </v-layout>
            </v-card-title>
            <v-row>
              <v-col md="12">
<!--                <v-text-field-->
<!--                    v-model="team.avatar"-->
<!--                    label="Background"-->
<!--                    :rules="[() => !!team.avatar || 'This field is required']"-->
<!--                />-->
<!--                <vue-dropzone-->
<!--                    :options="dropzoneOptions"-->
<!--                    id="dropzone"-->
<!--                />-->
              </v-col>
            </v-row>
            <v-card-actions class="px-0">
              <v-btn
                  color="success"
                  class="mr-4"
                  @click="createTeam"
              >
                Create
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import TeamCard from "@/components/boxes/TeamCard";
// import vue2Dropzone from 'vue2-dropzone'
// import 'vue2-dropzone/dist/vue2Dropzone.min.css'

export default {
  name: "CreateTeam",
  components:{
    TeamCard,
    // vueDropzone: vue2Dropzone
  },
  data () {
    return {
      team: undefined,
      passwordConfirmation: "",
      // dropzoneOptions: {
      //   url: '/api/teams/avatar/temp',
      //   thumbnailWidth: 150,
      //   maxFilesize: 0.5
      // }
    }
  },
  props:{
    show: Boolean
  },
  beforeMount() {
    this.clearTeam()
  },
  methods:{
    checkPasswdConfirmation(){
      return this.team.password.slice(0, this.passwordConfirmation.length) === this.passwordConfirmation
    },
    createTeam(){
      if (this.passwordConfirmation !== this.team.password){
        return
      }

      this.$emit("create", this.team)
      setTimeout(() => {
        this.clearTeam()
      }, 500)
    },
    clearTeam(){
      this.team = {
        name: "",
        password: "",
        background: "",
        users: []
      }
    }
  },
}
</script>

<style scoped>

</style>
