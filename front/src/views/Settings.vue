<template>
  <v-layout>
    <!--        color="primary darken-2"-->
    <v-sheet
        color="transparent"
        style="position: absolute"
        height="200px"
        width="100%"
    >

      <v-card-title
          class="headline text-h4 font-weight-bold"
      >
        Settings
      </v-card-title>
    </v-sheet>

    <v-container fluid style="margin-top: 80px">
      <v-row no-gutters>
        <v-col sm="12" md="8">
          <v-card
              rounded="lg"
              v-if="!isLoading"
              color="secondary"
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
              <v-card
                  flat
                  color="transparent"
                  style="position: absolute; width: calc(100% - 15px); left: 15px; top: -15px"
              >
                <v-layout
                    align-center
                    fill-height
                    justify-center
                >
                  <v-hover>
                    <template v-slot:default="{ hover }">
                      <v-avatar
                          class="elevation-6"
                          color="secondaryLighter"
                          rounded="lg"
                          size="100"
                          style="cursor:pointer;"
                          @click="beginUploadAvatar"
                      >
                        <!--                        <v-icon-->
                        <!--                            v-if="!userAvatar"-->
                        <!--                            dark-->
                        <!--                            size="70"-->
                        <!--                            v-text="'mdi-account-circle'"-->
                        <!--                        />-->
                        <v-img
                            ref="settingsAvatar"
                            width="100"
                            height="100"
                            :src="avatarImgPath"
                        />
                        <v-fade-transition>
                          <v-overlay
                              v-if="hover"
                              absolute
                              color=primary
                          >
                            <v-icon
                                v-text="'mdi-pencil'"
                            />
                          </v-overlay>
                        </v-fade-transition>
                      </v-avatar>
                    </template>
                  </v-hover>
                  <v-layout
                      fill-height
                  >
                    <!--                        v-model="user.avatar"-->
                    <!--                    <v-text-field-->
                    <!--                    color=accent-->
                    <!--                        v-model="userBackground"-->
                    <!--                        class="mt-6 px-4"-->
                    <!--                        append-icon="mdi-image-size-select-actual"-->
                    <!--                        placeholder="https://..."-->
                    <!--                        label="Profile"-->
                    <!--                    />-->
                  </v-layout>
                </v-layout>
              </v-card>
              <v-container style="height: 70px" />

            </v-card-title>

            <v-form
                @submit.prevent=""
            >
              <v-card-text>
                <v-row>
                  <v-col sm="12" md="6">
                    <v-text-field
                        color="accent"
                        disabled
                        v-model="user.username"
                        label="Name"
                        :rules="[() => !!user.username || 'This field is required']"
                    />
                  </v-col>
                  <v-col sm="12" md="6">
                    <v-text-field
                        color="accent"
                        v-model="user.password"
                        :rules="[() => !!user.password || 'This field is required']"
                        label="Current password"
                        type="password"
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col sm="12" md="6">
                    <v-text-field
                        color="accent"
                        v-model="user.newPassword"
                        :rules="[() => !!user.newPassword || 'This field is required']"
                        label="New password"
                        type="password"
                    />
                  </v-col>
                  <v-col sm="12" md="6">
                    <v-text-field
                        color="accent"
                        v-model="user.newPasswordConfirmation"
                        :rules="[() => !!user.password || 'This field is required', checkNewPasswdConfirmation || 'New password confirmation does not match']"
                        label="Password confirmation"
                        type="password"
                    />
                  </v-col>
                </v-row>
                <!--              <v-text-field-->
                <!--                color=accent-->
                <!--                  disabled-->
                <!--                  v-model="user.email"-->
                <!--                  label="Email"-->
                <!--                  :rules="[() => !!user.email || 'This field is required']"-->
                <!--                  required-->
                <!--              />-->

              </v-card-text>
            </v-form>
          </v-card>
          <v-card v-else>
            <v-progress-circular indeterminate />
          </v-card>
        </v-col>
      </v-row>
      <update-snackbar
          v-model="showBottomSaveSnackbar"
          :loading="saveCurrentSettingsLoader"
          :allow-save.sync="allowSave"
          @save="saveCurrentSettings"
          @reset="restoreSettings"
      />

    </v-container>
    <!--    <v-dialog max-width="500px" v-model="showUploadAvatarDialog">-->
    <!--      <v-card>-->
    <!--        <v-card-title>-->
    <!--          Change avatar-->
    <!--        </v-card-title>-->
    <!--        <v-card-text>-->
    <!--          <v-file-input-->
    <!--              accept="image/png,image/jpeg"-->
    <!--              label="Avatar"-->
    <!--              show-size-->
    <!--              ref="avatarFileInput"-->
    <!--              v-model="newAvatar"-->
    <!--          />-->
    <!--        </v-card-text>-->
    <!--        <v-card-actions>-->
    <!--          <v-btn @click="uploadAvatar" color="primary" text>Upload</v-btn>-->
    <!--        </v-card-actions>-->
    <!--      </v-card>-->
    <!--    </v-dialog>-->
    <!--    <v-file-input-->
    <!--        accept="image/png,image/jpeg"-->
    <!--        label="Avatar"-->
    <!--        show-size-->
    <!--        ref="avatarFileInput"-->
    <!--        v-model="newAvatar"-->
    <!--        style="display: none"-->
    <!--    />-->
    <input
        type="file"
        ref="avatarFileInput"
        v-on:change="uploadAvatar"
        style="display: none"
    />

  </v-layout>

</template>

<script>
import UpdateSnackbar from "@/components/interactive/UpdateSnackbar";
import backend from "@/backend";

export default {
  name: "Settings",
  components:{
    UpdateSnackbar,
  },
  data () {
    return {
      slug: Date.now().toString(),
      user: null,
      allowSave: false,
      originalUser: null,
      showBottomSaveSnackbar: false,
      saveCurrentSettingsLoader: false,
      newAvatar: null,
      showUploadAvatarDialog: false
    }
  },
  methods:{
    beginUploadAvatar () {
      this.$refs.avatarFileInput.click()
    },
    uploadAvatar (ev) {
      let img = ev.target.files[0]
      let data = {
        "userID": this.user.id,
        "avatar": img
      }

      backend.uploadAvatar(data)
          .then(() => {
            this.slug = Date.now()
            this.$toast.success("Updated avatar")
          }).catch((error) => {
        this.$toast.error(`Failed to upload file : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      }).finally(() => {
        // this.reloadAvatar()
      })

      this.newAvatar = null
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
    avatarImgPath(){
      return `${this.$store.getters.getUserProfilePicture}?r=${this.slug}`
    },
    // userAvatar(){
    //   if (this.user.avatar){
    //     return this.user.avatar
    //   }
    //
    //   return this.$store.getters.getSettings.defaultAvatar
    // },
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
            this.allowSave = false
          }
          else{
            this.allowSave = true
          }
        }

        this.showBottomSaveSnackbar = JSON.stringify(val) !== JSON.stringify(this.originalUser)
      },
      deep: true
    },

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
