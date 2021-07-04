<template>
  <v-container fill-height grid-list-lg>
    <!--    <v-row class="mb-9" no-gutters>-->

    <v-layout fill-height align-center flex justify-center>
      <v-flex md7 lg4 xs10 sm6>
        <v-card-title
            v-text="title"
            class="overline"
            style="font-size: 18px !important;"
        />

        <v-card
            color="secondary"
            flat
        >
          <v-layout
              class="py-0"
              justify-center
              align-center
              width="220px"
          >
            <v-card
                class="pa-2 pt-8"
                flat
                color="transparent"
            >
              <v-img
                  :src="$store.getters.getSettings.logo"
                  max-height="100px"
                  :lazy-src="null"
                  contain
                  style="opacity: .95"
                  position="top"
                  class="white--text"
              />
            </v-card>
          </v-layout>
          <v-card-text>
            <v-form
                ref="form"
                action="/login"
                method="post"
                v-model="valid"
                @submit.prevent="submitForm"
            >
              <v-text-field
                  color="accent"
                  autofocus
                  v-model="username"
                  label="Username"
                  append-icon="mdi-account-box"
                  :error-messages="usernameErrors"
                  required
              />
              <v-text-field
                  color="accent"
                  label="Password"
                  v-model="password"
                  :error-messages="passwordErrors"
                  :append-icon="showPass ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
                  @click:append="() => (showPass = !showPass)"
                  :type="showPass ? 'text' : 'password'"
                  required
              />
              <v-layout
                  align-center
                  justify-center
                  v-if="!isRegister"
              >
                <v-container>
                  <v-btn
                      block
                      type="submit"
                      :disabled="!valid"
                      color="accent"
                      class="mb-4"
                  >
                    LOGIN
                  </v-btn>
                  <v-btn
                      v-if="$store.getters.getSettings.allow_registration"
                      block
                      :to="'/register'"
                      text
                  >
                    REGISTER
                  </v-btn>
                </v-container>
              </v-layout>
              <v-layout
                  v-if="isRegister && $store.getters.getSettings.allow_registration"
                  align-center
                  justify-center
              >
                <v-container>
                  <v-btn
                      block
                      :to="'/login'"
                      text
                      class="mb-4"
                  >
                    LOGIN
                  </v-btn>
                  <v-btn
                      block
                      type="submit"
                      color="accent"
                  >
                    REGISTER
                  </v-btn>
                </v-container>
              </v-layout>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <registered
        v-if="isRegister && $store.getters.getSettings.allow_registration"
        :show="showModal"
        :success.sync="registrationSuccess"
        @close="registeredModalClosed"
    />
    <logged-in
        @close="loggedInModalClosed"
        v-if="!isRegister"
        :show="showModal"
        :success.sync="loginSuccess"
    />
  </v-container>
</template>

<script>
import {validationMixin} from 'vuelidate'
import {email, maxLength, required} from 'vuelidate/lib/validators'
import backend from '../../backend'
import Registered from "@/components/modals/auth/Registered";
import LoggedIn from "@/components/modals/auth/LoggedIn";

export default {
  name: "Login",
  mixins: [validationMixin],
  components: {
    Registered,
    LoggedIn
  },
  validations: {
    username: { required, maxLength: maxLength(100) },
    password: { required, maxLength: maxLength(200) },
    email: { required, email },
  },
  data: () => ({
    valid: false,
    showPass: false,
    // username: 'admin',
    // password: 'toor',
    username: '',
    password: '',
    registrationSuccess: undefined,
    loginSuccess: undefined,
    showModal: false
  }),
  computed: {
    title(){
      return this.isRegister ? "Register" : "Login"
    },
    isRegister(){
      return this.$route.fullPath.includes("register")
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.maxLength && errors.push('Password must be at most 200 characters long')
      !this.$v.password.required && errors.push('Password is required.')
      return errors
    },
    usernameErrors () {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.maxLength && errors.push('Username must be at most 100 characters long')
      !this.$v.username.required && errors.push('Username is required.')
      return errors
    },
    emailErrors () {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('Must be valid e-mail')
      !this.$v.email.required && errors.push('E-mail is required')
      return errors
    },
  },
  methods:{
    submitForm(){
      if (this.isRegister){
        this.register()
      }else{
        this.login()
      }
    },
    loggedInModalClosed(){
      this.showModal = false
      setTimeout(() => {
        this.loginSuccess = undefined
      }, 500)
    },
    registeredModalClosed(){
      this.showModal = false
      setTimeout(() => {
        this.registrationSuccess = undefined
      }, 500)
    },
    login(){
      // TODO REPAIR VALIDATION
      // this.$v.$touch()
      // if (!this.valid){
      //   return
      // }

      this.showModal = true

      let formData = {
        username: this.username,
        password: this.password
      }

      backend.login(formData)
          .then(res => {
            if (res.data.errors.length > 0){
              this.$toast.error(`Failed to login : ${res.data.errors.join(" / ")}`)
              this.showModal = false
              // this.loginSuccess = false
              return
            }

            this.loginSuccess = true
            console.log(res.data.user.session)
            this.$cookies.set("CHATSUBO-SESSION", res.data.user.session)
            this.$store.commit("setUser", res.data.user)

            setTimeout(() => {
              this.$router.push("/home").catch(() => {})
            }, 500)

          }).catch(res => {
        console.log(res.response)
        if (res.response.status === 404){
          this.$toast.error(res.response.data.errors[0])
        }
        this.showModal = false
      })
    },
    register(){
      // this.$v.$touch()
      // if (!this.valid){
      //   return
      // }

      this.showModal = true

      let formData = {
        username: this.username,
        email: this.email,
        password: this.password
      }

      backend.register(formData)
          .then(responseData => {
            console.log(responseData)
            if (responseData.errors.length > 0){
              this.$toast.error(`Failed to register account : ${responseData.errors.join(" / ")}`)
              this.showModal = false
              // this.registrationSuccess = false
              return
            }

            this.registrationSuccess = true
            this.$cookies.set("CHATSUBO-SESSION", responseData.user.session)
            this.$store.commit("setUser", responseData.user)
            // this.$router.push("/")
          }).catch(error => {
        console.log(error)
        // this.registrationSuccess = false
        this.showModal = false
        this.$toast.error(`Failed to register account : ${error}`)
      })
    },
    goTo(where){
      this.$router.push({ path: where })
    }
  },
  mounted() {
    // this.$refs.form.validate()
  }
}
</script>

<style scoped>

.v-application--wrap{
  opacity: 1 !important;
  transition: .3s opacity ease-in-out;
}

</style>
