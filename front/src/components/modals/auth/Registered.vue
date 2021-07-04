<template>
  <v-dialog
      overlay-color="background"
      v-model="show"
      :persistent="isLoading"
      max-width="300"
      @click:outside="closeModal"
  >
    <v-card
        style="transition: .3s ease-in-out"
        :color="cardColor"
    >
      <v-card-title class="headline" v-text="loadingCardTitle" />
      <v-card-text v-text="loadingCardText" />
      <v-layout fill-height justify-center align-center>
        <v-progress-linear
            v-show="isLoading"
            style="width: 40px"
            indeterminate
            color="yellow darken-2"
        />
      </v-layout>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
            v-if="!isLoading"
            text
            @click="closeModal"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Registered",
  props:{
    success: {
      type: Boolean,
      default: () => undefined
    },
    show: {
      type: Boolean,
      default: () => false
    }
  },
  data: () => ({
  }),
  methods:{
    closeModal(){
      this.$emit("close")
    }
  },
  computed: {
    loadingCardTitle(){
      let text = "Waiting for server..."
      if (!this.isLoading){
        switch (this.success){
          case true:
            text = "Success"
            break
        }
      }

      return text
    },
    loadingCardText(){
      let text = ""

      switch (this.success){
        case true:
          text = "Account registered"
          break
      }

      return text
    },
    isLoading(){
      return this.success === undefined
    },
    cardColor(){
      let color = "default"

      switch (this.success){
        case true:
          color = "green darken-1"
          break
        case false:
          color = "error"
          break
      }

      return color
    }
  }
}
</script>

<style scoped>

</style>
