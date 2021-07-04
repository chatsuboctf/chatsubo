<template>
  <v-container
      id="team-container"
      style="height: 300px"
      v-if="!isLoading && noTeam"
  >
    <v-layout
        fill-height
        align-center
        justify-center
    >
      <!--      <div class="headline">-->
      <!--        User not found :'(-->
      <!--      </div>-->
      <v-row>
        <v-col md="5">
          <v-layout fill-height column align-center justify-center>
            <v-btn
                large
                color="primary"
                @click="showCreateTeamDialog = true"
            >
              <v-icon
                  class="mr-1"
                  v-text="'mdi-plus'" />
              Create team
            </v-btn>
          </v-layout>
        </v-col>
        <v-col md="1">
          <v-divider
              class="mx-4"
              vertical
          ></v-divider>
        </v-col>
        <v-col md="5">
          <v-layout
              style="height: 150px"
              column
              fill-height
              justify-space-around
              align-content-space-around
          >
            <div
                class="text-center"
            >
              <v-btn
                  large
                  color="primary"
                  @click="showJoinTeamDialog = true"
              >
                <v-icon
                    class="mr-2"
                    v-text="'mdi-account-multiple-plus'" />
                Join team
              </v-btn>
            </div>
          </v-layout>
        </v-col>
      </v-row>
    </v-layout>
    <join-team
        :show.sync="showJoinTeamDialog"
        @join="joinTeam"
        @click:outside="showJoinTeamDialog = false"
    />
    <create-team
        :show.sync="showCreateTeamDialog"
        @create="createTeam"
        @click:outside="showCreateTeamDialog = false"
    />
  </v-container>
  <v-container
      v-else-if="!isLoading && teamNotFound"
  >
    <v-layout fill-height align-center justify-center>
      <div class="headline">
        Team not found
      </div>
    </v-layout>
  </v-container>
  <v-container
      v-else-if="!isLoading"
      class="pt-16"
  >
    <v-row
        class="mb-2"
    >
      <v-layout>
        <v-col sm="12">
          <v-card
              color="secondary"
          >
            <v-row>
              <v-col sm="12" lg="3">
                <v-card
                    style="position: absolute; left: 20px; top: -25px"
                >
                  <team-card
                      :team="team"
                      :is-teammate="isTeammate"
                      with-stats
                      flat
                  />
                </v-card>

                <v-container
                    class="pa-4"
                    style="min-height: 200px"
                />
              </v-col>
              <v-col
                  lg="9"
                  sm="12"
              >
                <v-container
                    class="pa-0 px-6"
                >
                  <v-layout
                      justify-start
                  >
                    <v-icon
                        small
                        class="pr-2"
                        v-text="'mdi-account'"
                    />
                    <span
                        style="color: white !important;"
                        class="overline"
                        v-text="'Members'"
                    />
                  </v-layout>
                  <v-data-table
                      class="row-pointer secondary"
                      :headers="headers"
                      :items="team.users"
                      :loading="isLoading"
                      item-key="id"
                      :items-per-page="5"
                      :search="search"
                      loading-text="Loading data..."
                      @click:row="goToUser"
                  >
                    <template slot="top">
                      <v-text-field
                          class="pt-0"
                          v-model="search"
                          append-icon="mdi-magnify"
                          hide-details
                          label="Search"
                      ></v-text-field>
                    </template>
                    <template slot="item.actions">
                      <v-tooltip
                          transition="slide-fade-transition"
                          top
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              small
                              v-text="'mdi-chevron-right'"
                              v-bind="attrs"
                              v-on="on"
                          />
                        </template>
                        View profile
                      </v-tooltip>
                    </template>
                  </v-data-table>
                </v-container>
              </v-col>
            </v-row>
            <!--            <v-card-text>-->
            <!--              <v-row>-->
            <!--                <v-col sm="3">-->
            <!--                <safety-switch-->
            <!--                    icon="mdi-account-multiple-remove"-->
            <!--                    :outlined="!safeties.reset"-->
            <!--                    :disabled="!safeties.reset"-->
            <!--                    label="Leave"-->
            <!--                    @click="leave"-->
            <!--                />-->

            <!--                </v-col>-->
            <!--              </v-row>-->
            <!--            </v-card-text>-->

            <v-card-text
                v-if="isTeammate && !team.is_owner"
            >
              <div
                  class="pt-4"
              >
                <v-btn
                    :outlined="!safeties.reset"
                    :disabled="!safeties.reset"
                    color="error"
                    @click="leave"
                >
                  <!--                :loading="resetBoxLoader"-->
                  <v-icon
                      v-text="'mdi-account-multiple-remove'"
                      class="mr-2"
                  />
                  Leave
                </v-btn>
                <v-switch hint="You won't be prompted for confirmation"
                          color='red darken-2'
                          persistent-hint
                          v-model="safeties.reset"
                          label="Safety"/>
              </div>

            </v-card-text>
          </v-card>
        </v-col>
      </v-layout>
    </v-row>
    <v-container
        v-if="team.is_owner"
    >
      <v-layout
          justify-start
      >
        <v-icon
            small
            class="pr-2"
            v-text="'mdi-cog'"
        />
        <span
            style="color: white !important;"
            class="overline"
        >
              Administration
            </span>
      </v-layout>
      <v-row
          class="pt-2"
      >
        <v-col sm="12" md="4">
          <v-text-field
              hide-details
              required
              label="Name"
              :rules="[() => !!team.name || 'This field is required']"
              v-model="team.name"
          />
        </v-col>
        <v-col sm="12" md="4">
          <v-text-field
              hide-details
              label="Background"
              :rules="[() => !!team.avatar || 'This field is required']"
              v-model="team.avatar"
          />
        </v-col>
        <v-col sm="12" md="4">
          <v-autocomplete
              hide-details
              v-model="team.owner"
              :items="team.users"
              item-text="username"
              item-value="id"
              label="Captain"
              :rules="[() => !!team.owner || 'This field is required']"
              required
          />
        </v-col>
        <v-row>
          <v-col>
            <div
                class="pt-4"
            >
              <v-btn
                  :outlined="!safeties.reset"
                  :disabled="!safeties.reset"
                  color="error"
                  @click="disband"
              >
                <!--                :loading="resetBoxLoader"-->
                <v-icon
                    v-text="'mdi-account-multiple-remove'"
                    class="mr-2"
                />
                Disband
              </v-btn>
              <v-switch hint="You won't be prompted for confirmation"
                        color='red darken-2'
                        persistent-hint
                        v-model="safeties.reset"
                        label="Safety"/>
            </div>
          </v-col>
        </v-row>
      </v-row>
    </v-container>
    <v-container>
      <v-layout
          align-center
          justify-start
          column
      >
        <v-card-text
            class="pa-0"
            v-for="cat in team.categories"
            :key="cat.name"
        >
          <v-layout
              justify-start
          >
            <v-icon
                small
                class="pr-2"
                v-text="cat.icon"
            />
            <span
                style="color: white !important;"
                class="overline"
            >
              {{cat.name.toProperCase()}}
            </span>
          </v-layout>
          <box-card-wall
              showcase
              :boxes.sync="cat.boxes"
              @click:card="boxCardClicked"
          />
        </v-card-text>
      </v-layout>
    </v-container>
    <update-snackbar
        v-model="showBottomSaveSnackbar"
        :allow-save="showBottomSaveSnackbar"
        :loading="saveCurrentSettingsLoader"
        @save="saveCurrentSettings"
        @reset="restoreSettings"
    />
  </v-container>
  <v-container fluid style="height: 300px" v-else>
    <v-layout fill-height align-center justify-center>
      <v-progress-circular
          indeterminate
      />
    </v-layout>
  </v-container>
</template>

<script>
import backend from "@/backend";
import JoinTeam from "@/components/modals/team/JoinTeam";
import CreateTeam from "@/components/modals/team/CreateTeam";
import TeamCard from "@/components/boxes/TeamCard";
import BoxCardWall from "@/components/boxes/BoxCardWall";
import UpdateSnackbar from "@/components/interactive/UpdateSnackbar";
// import SafetySwitch from "../components/interactive/SafetySwitch";

export default {
  name: "Team",
  components:{
    JoinTeam,
    CreateTeam,
    TeamCard,
    BoxCardWall,
    UpdateSnackbar,
    // SafetySwitch
  },
  data: () => {
    return {
      team: {},
      originalTeam: {},
      search: null,
      showBottomSaveSnackbar: false,
      saveCurrentSettingsLoader: false,
      disbandLoader: false,
      leaveLoader: false,
      headers: [
        {
          text: '#',
          align: 'start',
          filterable: false,
          sortable: true,
          value: 'index'
        },
        {
          text: 'Username',
          align: 'start',
          sortable: false,
          value: 'username'
        },
        // {
        //   text: 'Rank',
        //   align: 'start',
        //   filterable: false,
        //   sortable: false,
        //   value: 'rank'
        // },
        {
          text: 'Score',
          align: 'start',
          filterable: false,
          sortable: false,
          value: 'score'
        },
        {
          text: '',
          align: 'center',
          filterable: false,
          sortable: false,
          value: 'actions'
        },
      ],
      safeties:{
        reset: false,
      },
      noTeam: undefined,
      teamNotFound: undefined,
      showJoinTeamDialog: false,
      showCreateTeamDialog: false,
      showChangeCaptainDialog: false
    }
  },
  methods:{
    disband(){
      this.disbandLoader = true

      backend.disbandTeam(this.team).then(() => {
      }).catch((res) => {
        if (res.response.status === 401){
          this.$toast.error("Unauthorized")
        }

        this.$toast.error(res.response.data.errors.join(" / "))
      }).finally(() => {
        this.disbandLoader = false
        this.loadTeam("join")
        this.$router.push("/team/join")
      })
    },
    leave(){
      this.leaveLoader = true

      backend.leaveTeam().then(() => {
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      }).finally(() => {
        this.leaveLoader = false
        this.loadTeam("join")
        this.$router.push("/team/join")
      })
    },
    restoreSettings () {
      this.showBottomSaveSnackbar = false
      this.team = JSON.parse(JSON.stringify(this.originalTeam))
    },
    saveCurrentSettings () {
      this.saveCurrentSettingsLoader = true

      backend.editTeam(this.team).then(() => {
        this.$toast.success("Team updated")
      }).catch((res) => {
        if (res.response.status === 401){
          this.$toast.error("Unauthorized")
          return
        }

        this.$toast.error(res.response.data.errors.join(" / "))
      }).finally(() => {
        this.showBottomSaveSnackbar = false
        this.saveCurrentSettingsLoader = false
        // this.originalTeam = JSON.parse(JSON.stringify(this.team))
        this.loadTeam(this.$router.currentRoute.params.who)
      })
    },
    goToUser(row) {
      this.$router.push(`/profile/${row.username}`)
    },
    boxCardClicked(box){
      this.$router.push(`/box/${box.id}`)
    },
    joinTeam(teamData){
      this.showJoinTeamDialog = false

      const data = {
        team: teamData,
        user: this.$store.getters.getUser
      }

      backend.joinTeam(data)
          .then((res) => {
            console.log(res.data.data.team_id)
            this.$toast.success(`Joined team <b>${data.team.name}</b>`, { duration: 10000 })
            this.loadTeam(res.data.data.team_id)
            this.$router.push(`/team/${res.data.data.team_id}`)

          }).catch((res) => {
            this.team = {}
            this.$toast.error(res.response.data.errors.join(" / "), { duration: 10000 })
          }
      )
    },
    createTeam(teamData){
      this.showCreateTeamDialog = false

      const data = {
        team: teamData,
        user: this.$store.getters.getUser
      }

      backend.createTeam(data)
          .then((res) => {
            console.log(res.data.data.team_id)
            this.$toast.success(`Created team <b>${data.team.name}</b>`, { duration: 10000 })
            this.loadTeam()
            this.$toast.error(res.response.data.errors.join(" / "), { duration: 10000 })
          }).catch((res) => {
            this.team = {}
            this.$toast.error(res.response.data.errors.join(" / "), { duration: 10000 })
          }
      )
    },
    loadTeam(teamID){
      this.noTeam = undefined

      backend.getTeam(teamID)
          .then((res) => {
            if (res.status === 204){
              this.noTeam = true
              this.team = {}
              return
            }

            if (res.data.errors.length > 0){
              this.noTeam = true
              this.$toast.error(`Failed to fetch team data : ${res.data.errors.join(" / ")}`)
              this.team = {}
              return
            }

            // for (let [idx, user] of res.data.team.entries()){
            //   user.index = idx+1
            //   user.rank = this.$mapScoreToRank(user.score).text
            // }

            this.team = res.data.team
            this.originalTeam = JSON.parse(JSON.stringify(this.team))
            this.noTeam = false
          }).catch((err) => {
        if (err.response.status === 404){
          this.$toast.error(err.response.data.errors.join(" / "), { duration: 10000 })
          this.team = {}
          this.teamNotFound = true
        }else if (err.response.status === 301){
          this.$router.push(`/team/${err.response.data.data.team_id}`)
        }
      }).finally(()=>{
        this.$emit("loaded")
      })

    }
  },
  computed:{
    isLoading(){
      return this.noTeam === undefined && this.teamNotFound === undefined
    },
    isTeammate(){
      if (!this.$store.getters.getUser.team){
        return false
      }

      return this.$store.getters.getUser.team.id === this.team.id
    }
  },
  watch:{
    team: {
      handler (val) {
        this.showBottomSaveSnackbar = JSON.stringify(val) !== JSON.stringify(this.originalTeam);
      },
      deep: true
    },
    "team.users": {
      handler(val){
        if (val === undefined){
          return
        }

        for (let [idx, user] of val.entries()) {
          user.index = idx + 1
          // user.rank = this.$mapScoreToRank(user.score).text
        }

        this.team.users = val
      },
      deep: true
    }
  },
  beforeMount(){
    this.loadTeam(this.$router.currentRoute.params.who)
  }
}
</script>

<style scoped>

</style>
