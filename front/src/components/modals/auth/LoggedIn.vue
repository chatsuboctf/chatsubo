<template>
  <v-dialog
      v-model="show"
      :persistent="isLoading"
      max-width="300"
      @click:outside="closeModal"
      overlay-color="background"
  >
    <v-card
        style="transition: .3s ease-in-out"
        :color="cardColor"
    >
      <!--      <v-card-title class="headline" v-text="loadingCardTitle" />-->
      <v-slide-x-reverse-transition leave-absolute hide-on-leave>
        <v-card-text
            v-show="isLoading"
            class="pt-4"
            style="height: 150px"
        >
          <v-layout fill-height column justify-space-around align-center>
            <v-progress-circular
                indeterminate
                color="white"
            />
<!--                color="yellow darken-2"-->
            <div v-text="loadingCardText" />
            <!--          <div>-->
            <!--            Please wait...-->
            <!--          </div>-->

          </v-layout>
        </v-card-text>
      </v-slide-x-reverse-transition>
      <v-slide-x-transition >
        <v-card-text
            v-show="!isLoading"
            class="pt-4"
            style="height: 150px"
        >
          <v-layout fill-height column justify-space-around align-center>
            <div style="font-size: 1rem !important; color: rgba(255,255,255,.9)" class="text-overline">
              Welcome
            </div>
          </v-layout>
        </v-card-text>
      </v-slide-x-transition>
      <!--      <v-card-actions>-->
      <!--        <v-spacer></v-spacer>-->
      <!--        <v-btn-->
      <!--            v-if="!isLoading"-->
      <!--            text-->
      <!--            @click="closeModal"-->
      <!--        >-->
      <!--          Close-->
      <!--        </v-btn>-->
      <!--      </v-card-actions>-->
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "LogginIn",
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
      let text = "Please wait..."
      if (!this.isLoading){
        switch (this.success){
          case true:
            text = "Login successful"
            break
            // case false:
            //   text = "Error"
            //   break
        }
      }

      return text
    },
    loadingCardText(){
      let text = "Signin in..."

      switch (this.success){
        case true:
          text = "Welcome"
          break
      }

      return text
    },
    isLoading(){
      return this.success === undefined
    },
    cardColor(){
      let color = "secondary"

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
