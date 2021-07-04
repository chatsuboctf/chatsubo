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
              <span
                  class="headline text-h4 font-weight-bold"
              >
              Users
              </span>
            </v-layout>
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

    <v-card>
      <v-data-table
          class="row-pointer secondary"
          :headers="headers"
          :items="usersTableData"
          :loading="isLoading"
          item-key="id"
          :footer-props="{
          'items-per-page-options': [5, 10, 25, 50, 100]
        }"
          :items-per-page="50"
          :search="search"
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
        <template v-slot:item.avatar>
          <v-avatar
              class="my-2"
              color="secondaryLighter"
              size="30"
              rounded
          >
            <v-img
                :src="$store.getters.getUserProfilePicture"
            />
          </v-avatar>
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
<!--            Click the row to view the user's profile-->
<!--          </v-tooltip>-->
<!--        </template>-->
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import backend from "@/backend";

export default {
  name: "Users",
  data() {
    return {
      users: undefined,
      usersTableData: undefined,
      usersLoading: false,
      search: null,
      headers: [
        {
          text: '#',
          align: 'start',
          filterable: false,
          sortable: true,
          value: 'index',
          width: 70,
        },
        {
          text: '',
          align: 'start',
          filterable: false,
          sortable: false,
          value: 'avatar',
          width: 30,
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
          text: 'Team',
          align: 'start',
          filterable: false,
          sortable: false,
          value: 'team.name'
        },
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
      ]
    }
  },
  methods: {
    goToUser(row) {
      this.$router.push(`/profile/${row.username}`)
    },
    loadUsers(){
      this.usersLoading = true

      backend.listUsers().then((res) => {
        this.users = res.users
        console.log(this.users)
      }).catch(() => {
        this.$toast.error(`Failed to fetch users`, { duration: 10000 })
      }).finally(() => {
        this.usersLoading = false
      })
    },
  },
  computed: {
    isLoading() {
      return this.usersTableData === undefined
    },
  },
  beforeMount() {
    this.loadUsers()
  },
  watch: {
    users(val){
      for (let [idx, user] of val.entries()){
        user.index = idx+1
        user.rank = this.$mapScoreToRank(user.score).text
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
