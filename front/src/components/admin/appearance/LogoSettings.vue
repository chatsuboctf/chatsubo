<template>
  <v-row no-gutters>
    <v-col sm="12">
      <v-card
          color="cardBackground"
          rounded="lg"
          class="px-4 pb-6"
      >
        <v-card-title>
          Logo
        </v-card-title>
        <v-layout
            align-center
            fill-height
            justify-center
        >
          <v-sheet
              width="80%"
              color="transparent"
          >
            <v-hover>
              <template v-slot:default="{ hover }">
                <v-card
                    class="elevation-6"
                    rounded="lg"
                    color="secondaryLighter"
                    style="cursor:pointer;"
                    @click="beginUploadAvatar"
                >
                  <v-img
                      contain
                      class="pa-8 mx-6"
                      ref="settingsLogo"
                      max-height="60%"
                      :src="logoImgPath"
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
                </v-card>
              </template>
            </v-hover>
          </v-sheet>
        </v-layout>

        <v-card-title
            class="pt-6"
        >
          Sizing
        </v-card-title>
        <v-layout
            fill-height
            justify-center
        >
          <v-sheet
              width="80%"
              color="transparent"
          >
            <v-row>
              <v-col>
                <v-app-bar
                    color="secondary"
                >

                  <v-app-bar-title
                      width="100%"
                  >
                    <v-layout
                        class="py-0"
                        justify-center
                        align-center
                        :width=logoWidth
                    >
                      <v-card
                          class="pa-2"
                          elevation="6"
                          :width=logoWidth
                          color="transparent"
                      >
                        <v-img
                            :src=$store.getters.getSettings.logo
                            :max-height=logoHeight
                            :lazy-src="null"
                            contain
                            style="opacity: .95"
                            position="top"
                            class="white--text"
                        />
                      </v-card>
                    </v-layout>
                  </v-app-bar-title>

                  <v-spacer/>
                  <v-card
                      class="px-4 py-1"
                      elevation="0"
                      color="transparent"
                  >
                    <v-layout
                        justify-center
                        align-center
                    >
                      <div class="pr-4">
                        <v-layout
                            align-end
                            justify-center
                            column
                        >
                          <span class="float-right" v-text="$store.getters.getUser.username"/>
                          <span
                              class="text-caption"
                              :style="`color: ${$store.getters.getSettings.darkTheme ? 'rgba(255, 255, 255,.7)' : 'rgba(0,0,0,.87)'}`"
                              v-text="`${$store.getters.getUser.score} pts`"
                          />

                        </v-layout>
                      </div>
                      <v-avatar
                          color="secondaryLighter"
                          rounded
                      >
                        <v-img
                            :src="$store.getters.getUserProfilePicture"
                        />
                      </v-avatar>

                    </v-layout>
                  </v-card>
                </v-app-bar>
              </v-col>

            </v-row>
            <v-row>
              <v-col
                  class="fill-height"
              >
                <v-card
                    color="secondaryLighter"
                    rounded="lg"
                    class="px-4"
                >
                  <v-layout
                      justify-center
                      align-center
                      fill-height
                  >
                    <v-slider
                        v-model="logoWidth"
                        hide-details
                        :max="500"
                        :min="1"
                        ticks
                        label="Width"
                        class="align-center"
                    >
                      <template v-slot:append>
                        <v-text-field
                            @input="updateLogoWidth"
                            :value="logoWidth"
                            type="number"
                        />
                      </template>
                    </v-slider>
                  </v-layout>
                </v-card>
              </v-col>
              <v-col
                  class="fill-height"
              >
                <v-card
                    color="secondaryLighter"
                    rounded="lg"
                    class="px-4"
                >

                  <v-layout
                      justify-center
                      align-center
                      fill-height
                  >
                    <v-slider
                        hide-details="auto"
                        v-model="logoHeight"
                        :max="500"
                        :min="1"
                        ticks
                        label="Height"
                        class="align-center"
                    >
                      <template v-slot:append>
<!--                            v-model="logoHeight"-->
                        <v-text-field
                            @input="updateLogoHeight"
                            :value="logoHeight"
                            type="number"
                        />
                      </template>
                    </v-slider>
                  </v-layout>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-layout
                    justify-end
                    align-end
                >
                  <v-btn
                      color="green"
                      @click="saveLogoSizing"
                  >
                    <v-icon
                        class="mr-2"
                        v-text="'mdi-content-save'"
                    />
                    Save
                  </v-btn>
                </v-layout>
              </v-col>
            </v-row>
          </v-sheet>
        </v-layout>
      </v-card>
    </v-col>
    <input
        type="file"
        ref="logoFileInput"
        v-on:change="uploadLogo"
        style="display: none"
    />
  </v-row>
</template>

<script>
import backend from "@/backend";
import {debounce} from "lodash";
// import SafetySwitch from "@/components/interactive/SafetySwitch";


export default {
  name: "LogoSettings",
  components: {
    // SafetySwitch
  },
  props: {
    loader: Boolean,
    selectedUser: null
  },
  data() {
    return {
      logoHeight: this.$store.getters.getSettings.logo_height,
      logoWidth: this.$store.getters.getSettings.logo_width,
      slug: Date.now().toString()
    }
  },
  methods: {
    updateLogoHeight: debounce(function (val) {
      this.logoHeight = val;
    }, 300),
    updateLogoWidth: debounce(function (val) {
      this.logoWidth = val;
    }, 300),
    saveLogoSizing(){
      let data = {
        "height": this.logoHeight,
        "width": this.logoWidth
      }

      backend.saveLogoSizing(data)
          .then(() => {
            this.$toast.success("Settings updated")
          }).catch((error) => {
        this.$toast.error(`Failed to save logo sizing : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      })

    },
    beginUploadAvatar () {
      this.$refs.logoFileInput.click()
    },
    uploadLogo (ev) {
      let img = ev.target.files[0]

      backend.uploadLogo(img)
          .then(() => {
            this.slug = Date.now()
            this.$toast.success("Updated logo")
          }).catch((error) => {
        this.$toast.error(`Failed to upload logo : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      })
    },
  },
  computed:{
    logoImgPath(){
      return `${this.$store.getters.getSettings.logo}?r=${this.slug}`
    }
  },
  watch:{
  }
}

</script>

<style scoped>

</style>
