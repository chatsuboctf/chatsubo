<template>
  <v-card
      width="100%"
      height="100%"
    color="secondary"
  >
    <v-hover
        v-slot:default="{ hover }"
    >
      <v-card
          class="d-flex"
          style="transition: .1s ease-in-out;"
          :to="team.id ? `/team/${team.id}` : null"
          :flat="flat"
          :elevation="elevation"
          @click="beginUploadAvatar"
          min-height="200"
          width="200"
      >
        <v-img
            width="100%"
            height="100%"
            style="position: absolute"
            :src="team.avatar"
            class="white--text pa-6"
            gradient="to bottom, rgba(0,0,0,.4), rgba(0,0,0,.4)"
        >
          <v-fade-transition>
            <v-overlay
                v-if="hover"
                absolute
                color="black lighten-4"
            >
              <v-icon v-if="!isTeammate" color="grey lighten-2" v-text="'mdi-account-group'"/>
              <v-icon v-else color="grey lighten-2" v-text="'mdi-pencil'"/>
            </v-overlay>
          </v-fade-transition>

          <v-layout
              fill-height
          >
            <v-row
                justify="center"
                align="end"
            >
              <v-col
                  class="pa-0 pb-1"
                  sm="11"
              >
                <v-layout
                    justify-center
                    fill-height
                    align-end
                >
                  <v-sheet
                      class="px-3 rounded overline"
                      style="z-index: 999; background-color: rgba(0,0,0,.5);"
                  >
                    <v-layout
                        justify-center
                        align-center
                    >
                      <v-tooltip
                          bottom
                      >

                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              v-if="!withStats"
                              small
                              v-bind="attrs"
                              v-on="on"
                              class="mr-2"
                              v-text="$mapScoreToRank(team.score).icon"
                              :color="$mapScoreToRank(team.score).color"
                          />
                          <span v-text="team.name"/>
                        </template>
                        <span
                            v-text="$mapScoreToRank(team.score).text"
                        />
                      </v-tooltip>
                    </v-layout>
                  </v-sheet>
                </v-layout>
              </v-col>
            </v-row>
          </v-layout>
        </v-img>
      </v-card>
    </v-hover>
    <v-card-actions
        v-if="withStats"
        class="pa-1"
    >
      <v-layout
          justify-start
          align-center
      >
        <box-card-stat
            icon="mdi-account"
            :stat="team.users ? team.users.length.toString() : '0'"
            tooltip="Members"
        />
        <box-card-stat
            icon="mdi-flag"
            :stat="team.flags ? team.flags.length.toString() : '0'"
            tooltip="Flags"
        />
<!--        <v-spacer/>-->
<!--        <box-card-stat-->
<!--            :icon="$mapScoreToRank(team.score).icon"-->
<!--            :stat="$mapScoreToRank(team.score).text"-->
<!--            :color="$mapScoreToRank(team.score).color"-->
<!--            tooltip="Rank"-->
<!--        />-->
      </v-layout>
    </v-card-actions>
    <input
        type="file"
        ref="avatarFileInput"
        v-on:change="uploadAvatar"
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
    team: Object,
    withStats: Boolean,
    flat: Boolean,
    isTeammate: Boolean,
    elevation: Number
  },
  methods:{
    beginUploadAvatar () {
      this.$refs.avatarFileInput.click()
    },
    uploadAvatar (ev) {
      let img = ev.target.files[0]
      let data = {
        "teamID": this.team.id ? this.team.id : "temp",
        "avatar": img
      }

      backend.uploadTeamAvatar(data)
          .then((res) => {
            console.log(res.data.data)
            this.team.avatar = res.data.data.path
            this.$toast.success("Updated avatar")
          }).catch((error) => {
        this.$toast.error(`Failed to upload file : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      }).finally(() => {
        // this.reloadAvatar()
      })

      this.newAvatar = null
    },
  },
  data () {
    return {
    }
  },
  computed:{
  }
}
</script>

<style scoped>
.box-card{
  border: 1px solid white;
}
</style>
