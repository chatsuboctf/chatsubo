<template>
  <v-card
      :color="color"
      flat
  >
    <v-hover
        v-slot:default="{ hover }"
        :disabled="!animateHover"
    >
      <v-card
          :outlined="disabled"
          class="d-flex"
          :class="{'box-card-hover' : hover}"
          style="transition: .1s ease-in-out; border-style: dashed; overflow: hidden"
          :style="disabled ? 'border-color: grey !important;' : ''"
          :to="!allowUpload && box.id ? `/box/${box.id}` : null"
          rounded
          :flat="flat || disabled"
          :elevation="elevation"
          min-height="105"
          width="400"
          color="secondary"
          v-on="allowUpload ? {click: beginUploadBackground} : {}"
      >
        <!--            v-show="imgLoaded"-->
        <v-img
            @load="imgLoaded = true"
            width="100%"
            height="100%"
            :src="!disabled || (disabled && box.completed) ? box.background : null"
            style="position: absolute"
            :lazy-src="null"
            class="white--text pa-6"
            gradient="to bottom, rgba(0,0,0,.15), rgba(0,0,0,.15)"
        >
          <v-fade-transition>
            <v-overlay
                v-if="hover"
                absolute
                color="black lighten-4"
            >
              <v-icon
                  style="top: -15px"
                  color="grey lighten-2"
                  v-text="icon ? icon : box.category.icon"
              />
            </v-overlay>
          </v-fade-transition>

          <v-layout
              fill-height
          >
            <v-row
                justify="end"
                align="end"
            >
              <v-col
                  class="pa-0 pb-1"
                  :class="{'pl-3': !centerLabel}"
                  :sm="centerLabel ? '12':'11'"
              >
                <v-layout
                    :justify-start="!centerLabel"
                    :justify-center="centerLabel"
                    fill-height
                    align-end
                >
                  <v-sheet
                      class="px-3 overline"
                      rounded
                      style="z-index: 3; background-color: rgba(0,0,0,.5);"
                  >
                    <v-layout
                        align-center
                    >
                      <v-tooltip
                          bottom
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              v-if="!noLabelIcon"
                              small
                              v-bind="attrs"
                              v-on="on"
                              class="mr-2"
                              v-text="$mapValueToDifficulty(box.difficulty).icon"
                              :color="$mapValueToDifficulty(box.difficulty).color"
                          />
                          <span v-text="box.name"/>
                        </template>
                        <span
                            v-text="$mapValueToDifficulty(box.difficulty).text"
                        />
                      </v-tooltip>
                    </v-layout>
                  </v-sheet>
                </v-layout>
              </v-col>
              <v-col
                  v-if="!noStatus"

                  class="pa-0 pl-3 pb-1"
                  sm="1"
                  align-self="start"
              >
                <span
                >
                <v-icon
                    v-if="box.completed"
                    small
                    color="green"
                    v-text="'mdi-check-circle'"
                />
                <v-icon
                    v-else
                    small
                    v-text="$mapProgressionToIcon(box.validated_flags.length, box.flags.length)"
                />
                </span>
              </v-col>
            </v-row>
          </v-layout>
        </v-img>
        <v-container
            fluid
            v-if="!disabled || (disabled && box.completed)"
        >
          <v-layout
              fill-height
              justify-center
              align-center
          >
            <v-progress-linear
                v-if="!blank"
                v-show="!imgLoaded"
                indeterminate
                color="white"
                style="width: 24px; top: -15px"
            />
            <v-icon
                v-if="blank && !box.background"
                color="white"
                v-text="'mdi-upload'"
            />
          </v-layout>
        </v-container>
      </v-card>
    </v-hover>
    <v-card-actions
        v-if="withStats"
        class="pa-1"
    >
      <v-layout
          justify-start
          align-center
          class="pl-2"
      >
        <box-card-stat
            :icon="$mapOSToIcon(box.os)"
            :stat="box.os"
            tooltip="OS"
        />
        <box-card-stat
            icon="mdi-flag"
            :stat="`${box.validated_flags.length}/${box.flags.length}`"
            tooltip="Flags"
        />
        <v-spacer/>
        <box-card-stat
            :icon="$mapValueToDifficulty(box.difficulty).icon"
            :stat="$mapValueToDifficulty(box.difficulty).text"
            :color="$mapValueToDifficulty(box.difficulty).color"
            tooltip="Difficulty"
        />
      </v-layout>
    </v-card-actions>

    <input
        type="file"
        ref="backgroundFileInput"
        v-on:change="uploadBackground"
        style="display: none"
    />
  </v-card>
</template>

<script>
import BoxCardStat from "@/components/boxes/BoxCardStat";
import backend from "../../backend";

export default {
  name: "BoxCard",
  components:{
    BoxCardStat
  },
  props:{
    box: Object,
    withStats: Boolean,
    flat: Boolean,
    elevation: String,
    icon: {
      type: String,
      default: () => ""
    },
    color: {
      type: String,
      default: () => "secondary"
    },
    disabled: Boolean,
    centerLabel: Boolean,
    noStatus: Boolean,
    noLabelIcon: Boolean,
    allowUpload: Boolean,
    animateHover: {
      type: Boolean,
      default: () => true
    },
    blank: Boolean
  },
  data () {
    return {
      imgLoaded: false
    }
  },
  methods:{
    beginUploadBackground () {
      this.$refs.backgroundFileInput.click()
    },
    uploadBackground (ev) {
      let img = ev.target.files[0]
      let boxID = this.$router.currentRoute.params.box ? this.$router.currentRoute.params.box : "temp"
      let data = {
        boxID:  boxID,
        background: img
      }

      backend.uploadBoxBackground(data)
          .then((res) => {
            this.box.background = res.data.data.path
            this.$toast.success("Updated background")
            console.log(res.data.data.background)
          }).catch((error) => {
        this.$toast.error(`Failed to upload file : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      }).finally(() => {
        // this.reloadBackground()
      })

      this.newBackground = null
    },

  }
}
</script>

<style scoped>
.box-card-hover{
  transform: scale(.98);
}
</style>
