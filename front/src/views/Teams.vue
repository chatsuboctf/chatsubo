<template>
  <v-container>
    <v-card color="transparent" flat >
      <v-card-title class="pb-0 pl-0">
        <v-row>
          <v-col md="3" sm="12">
            <v-layout
                justify-space-between
                fill-height
                align-center
            >
              Teams
            </v-layout>
          </v-col>
          <v-spacer/>
          <v-col md="6" sm="12">
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-title>
    </v-card>

    <v-data-table
        class="row-pointer secondary"
        :headers="headers"
        :items="teamsTableData"
        :loading="isLoading"
        item-key="id"
        :search="search"
        :items-per-page="50"
        loading-text="Loading data..."
        @click:row="goToTeam"
    >
        <template v-slot:item.avatar="{ item }">
          <v-avatar
              size="30"
              class="my-2"
              color="secondaryLighter"
              rounded
          >
            <v-img
                :src="item.avatar"
            />
          </v-avatar>
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
          Click the row to view the team's profile
        </v-tooltip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import backend from "@/backend";

export default {
  name: "Teams",
  data() {
    return {
      teams: undefined,
      teamsTableData: undefined,
      teamsLoading: false,
      search: "",
      headers: [
        {
          text: '#',
          align: 'start',
          filterable: false,
          sortable: false,
          value: 'index',
          width: 40
        },
        {
          text: '',
          align: 'start',
          sortable: false,
          filterable: false,
          value: 'avatar',
          width: 30
        },
        {
          text: 'Name',
          align: 'start',
          sortable: false,
          value: 'name'
        },
        // {
        //   text: 'Rank',
        //   align: 'start',
        //   filterable: false,
        //   sortable: false,
        //   value: 'rank.text'
        // },
        {
          text: 'Score',
          align: 'start',
          filterable: false,
          sortable: true,
          value: 'score'
        },
        {
          text: '',
          align: 'center',
          filterable: false,
          sortable: false,
          value: 'actions'
        },
      ]
    }
  },
  methods: {
    goToTeam(row) {
      this.$router.push(`/team/${row.id}`)
    },
    loadTeams(){
      this.teamsLoading = true

      backend.listTeams().then((res) => {

        if (res.data.teams){
          this.teams = res.data.teams
        }else{
          this.teams = []
        }
      }).catch((res) => {
        if (res.response.status !== 404){
          this.$toast.error(res.response.data.errors.join(" / "), { duration: 10000 })
        }

        this.teams = []
      }).finally(() => {
        this.teamsLoading = false
      })
    },
  },
  computed: {
    isLoading() {
      return this.teamsTableData === undefined
    },
  },
  beforeMount() {
    this.loadTeams()
  },
  watch: {
    teams(val){
      for (let [idx, user] of val.entries()){
        user.index = idx+1
        // user.rank = this.$mapScoreToRank(user.score)
      }

      console.log(val)
      this.teamsTableData = val
    }
  }
}
</script>

<style scoped>
.row-pointer >>> tbody tr :hover {
  cursor: pointer;
}
</style>
