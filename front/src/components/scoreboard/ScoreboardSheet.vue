<template>
  <v-container
      v-if="!loading"
  >
    <scoreboard-top
        :loading="isLoading"
        :users="users"
    />
    <v-card
        color="transparent"
        flat
    >
      <v-card-title class="pb-0 pl-0">
        <v-row>
          <v-col md="3" sm="12">
            <!--            <v-layout-->
            <!--                justify-space-between-->
            <!--                fill-height-->
            <!--                align-center-->
            <!--            >-->
            <!--                    <span-->
            <!--                        class="headline text-h4 font-weight-bold"-->
            <!--                    >-->
            <!--                    Scoreboard-->
            <!--                    </span>-->
            <!--            </v-layout>-->
          </v-col>
          <v-spacer/>
          <v-col md="6" sm="12">
            <v-text-field
                color="accent"
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-title>
    </v-card>

    <v-sheet
        rounded
        class="pa-4"
        color="secondary"
    >
      <v-data-table
          class="row-pointer secondary"
          :loading="isLoading"
          :headers="headers"
          :footer-props="{
          'items-per-page-options': [5, 10, 25, 50, 100]
        }"
          :search="search"
          :items="usersTableData"
          item-key="id"
          :items-per-page="50"
          loading-text="Loading data..."
      >
        <!--          @click:row="goToUser"-->
        <template slot="progress">
          <v-layout
              class="pt-10"
              justify-center
              align-center
              fill-height
          >
            <v-progress-circular
                color="white"
                indeterminate
            />
          </v-layout>
        </template>
        <template v-slot:item.flags="{ item }">
          <v-layout
              justify-center
              align-center
              class="overline"
          >
            <span>
<!--              {{item.flags.length}} / {{category.totalFlags}}-->
<!--              {{category.id === 'all' ? item.flags.length : item.flagged}} / {{category.totalFlags}}-->
              {{item.flagged}} / {{category.totalFlags}}

            </span>
            <v-icon
                small
                class="pl-1"
                v-text="'mdi-flag'"
            />
          </v-layout>
        </template>
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
        <template v-slot:item.username="{ item }">

          <v-layout
              justify-start
              align-center
              v-if="item.username === $store.getters.getUser.username"
          >
            <span style="font-weight: bold">
              {{item.username}}
            </span>
            <v-icon
                class="pl-2"
                small
                v-text="'mdi-account-circle'"
            />
          </v-layout>
          <span
              v-else
          >
            {{item.username}}
          </span>
        </template>
        <!--        <template slot="item.actions">-->
        <!--          <v-tooltip-->
        <!--              transition="slide-fade-transition"-->
        <!--              top-->
        <!--          >-->
        <!--            <template v-slot:activator="{ on, attrs }">-->
        <!--              <v-icon-->
        <!--                  small-->
        <!--                  v-text="'mdi-chevron-right'"-->
        <!--                  v-bind="attrs"-->
        <!--                  v-on="on"-->
        <!--              />-->
        <!--            </template>-->
        <!--            View profile-->
        <!--          </v-tooltip>-->
        <!--        </template>-->
      </v-data-table>
    </v-sheet>
  </v-container>
</template>

<script>
import backend from "@/backend"
// import ScoreboardChart from "@/components/charts/ScoreboardChart";
import ScoreboardTop from "@/components/scoreboard/ScoreboardTop";

export default {
  name: "Scoreboard",
  components:{
    ScoreboardTop
    // ScoreboardChart
  },
  props: {
    category: {
      type: Object,
      default: null
    },
    loading: Boolean
  },
  data() {
    return {
      users: undefined,
      search: null,
      usersTableData: undefined,
      // usersLoading: false,
      // chartOptions: {
      //   series: {
      //     name: 'line',
      //     type: 'line',
      //     showSymbol: false,
      //     data: [1,2,3]
      //   }
      // },
      headers: [
        {
          text: '#',
          align: 'start',
          sortable: true,
          filterable: false,
          value: 'index',
          width: 70
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
        //   value: 'rank.text'
        // },
        {
          text: 'Team',
          align: 'start',
          filterable: false,
          sortable: false,
          value: 'team.name'
        },
        {
          text: 'Score',
          align: 'start',
          sortable: true,
          filterable: false,
          value: 'score'
        },
        {
          text: 'Flags',
          align: 'center',
          sortable: true,
          filterable: false,
          value: 'flags'
        },
      ]
    }
  },
  methods: {
    goToUser(row) {
      this.$router.push(`/profile/${row.username}`)
    },
    loadAllUsers(){
      // this.usersLoading = true

      backend.listAllTopUsers(500).then((res) => {
        this.users = res.users
        // this.chartOptions.series.data =
      }).catch(() => {
        this.$toast.error(`Failed to fetch users`, { duration: 10000 })
      }).finally(() => {
        // this.usersLoading = false
      })
    },
    loadUsers(){
      // this.usersLoading = true
      // this.usersTableData = undefined

      const data = {
        n: 500,
        category_id: this.category.id
      }

      backend.listTopUsers(data).then((res) => {
        this.users = res.users
        // this.chartOptions.series.data =
      }).catch(() => {
        this.$toast.error(`Failed to fetch users`, { duration: 10000 })
      }).finally(() => {
        // this.usersLoading = false
      })
    }
  },
  computed: {
    isLoading() {
      return this.usersTableData === undefined
    },
  },
  mounted() {
    if (this.category.id === "all"){
      this.loadAllUsers()
    }else{
      this.loadUsers()
    }
  },
  watch: {
    category(){
      this.usersTableData = undefined
      if (this.category.id === "all"){
        this.loadAllUsers()
      }else{
        this.loadUsers()
      }
    },
    users(val){
      for (let [idx, user] of val.entries()){
        user.index = idx+1
        // user.rank = this.$mapScoreToRank(user.score)
        // user.team = user.team.name ? user.team : "/"
      }

      this.usersTableData = val
    }
  }
}
</script>

<style scoped>
.row-pointer >>> tbody tr :hover {
  /*cursor: pointer;*/
}
</style>
