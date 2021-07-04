<template>
  <v-dialog
      v-model="show"
      :persistent="isLoading"
      max-width="300"
      @click:outside="closeModal"
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
      <v-slide-x-transition>
        <v-card-text
            v-show="!isLoading"
            class="pt-4"
            style="height: 150px"
        >
          <v-layout fill-height column justify-space-around align-center>
            <slot v-if="success !== undefined && success" name="success">
              <div
                  style="font-size: 1rem !important; color: rgba(255,255,255,.9)"
                  class="text-overline"
                  v-text="successText"
              />
            </slot>
            <slot v-else-if="success !== undefined" name="failure">
              <div
                  style="font-size: 1rem !important; color: rgba(255,255,255,.9)"
                  class="text-overline"
                  v-text="failureText"
              />
            </slot>
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
  name: "CheckFlagLoading",
  props:{
    success: {
      type: Boolean,
      default: () => undefined
    },
    duration: {
      type: Number,
      default: () => 5000
    },
    loadingText: {
      type: String,
      default: () => "Please wait..."
    },
    loadingTitle: {
      type: String,
      default: () => "Login"
    },
    successText: {
      type: String,
      default: () => "Success"
    },
    successTitle: {
      type: String,
      default: () => "Success"
    },
    failureText: {
      type: String,
      default: () => "Failed"
    },
    failureTitle: {
      type: String,
      default: () => "Failed"
    },
    show: {
      type: Boolean,
      default: () => false
    }
  },
  data: () => ({
    timeout: null
  }),
  watch: {
    show(val){
      if (val){
        this.timeout = setTimeout(() => {
          this.$emit("close")
        }, this.duration)
      }
    }
  },
  methods:{
    closeModal(){
      if (this.timeout !== null){
        clearTimeout(this.timeout)
      }

      this.$emit("close")
    }
  },
  computed: {
    loadingCardTitle(){
      let text = this.loadingTitle
      if (!this.isLoading){
        switch (this.success){
          case true:
            text = this.successTitle
            break
          case false:
            text = this.failureTitle
            break
        }
      }

      return text
    },
    loadingCardText(){
      let text = this.loadingText

      switch (this.success){
        case true:
          text = this.successText
          break
        case false:
          text = this.failureText
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
