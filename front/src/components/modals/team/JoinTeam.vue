<template>
  <v-dialog
      v-model="show"
      transition="fade-transition"
      @keydown.ctrl.enter="joinTeam"
      @click:outside="$emit('click:outside')"
      max-width="350"
  >
    <v-card>
      <v-container class="px-6">

        <v-layout
            fill-height
            justify-space-around
            align-center
        >
          <v-form
              @submit="joinTeam"
              class="fluid fill-height"
          >
            <v-card-title class="px-0">
              Join team
            </v-card-title>
            <v-row>
              <v-col md="12">
                <v-text-field
                    v-model="team.name"
                    label="Name"
                    autofocus
                    class="container--fluid"
                    :rules="[() => !!team.name || 'This field is required']"
                    counter="200"
                    required
                />
              </v-col>
              <v-col md="12">
                <v-text-field
                    v-model="team.password"
                    :rules="[() => !!team.password || 'This field is required']"
                    label="Password"
                    type="password"
                />
              </v-col>
            </v-row>
            <v-card-actions class="px-0">
              <v-btn
                  color="success"
                  class="mr-4"
                  @click="joinTeam"
              >
                Join
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  name: "JoinTeam",
  components:{
  },
  data () {
    return {
      team: undefined,
    }
  },
  props:{
    show: Boolean
  },
  beforeMount() {
    this.clearTeam()
  },
  methods:{
    joinTeam(){
      this.$emit("join", this.team)
      this.clearTeam()
    },
    clearTeam(){
      this.team = {
        name: "",
        password: "",
      }
    }
  },
}
</script>

<style scoped>

</style>
