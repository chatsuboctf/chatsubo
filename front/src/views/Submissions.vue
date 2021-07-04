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
                    Submissions
                    </span>
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

    <v-card>
      <v-data-table
          class="row-pointer secondary"
          :headers="headers"
          :items="submissions"
          :loading="isLoading"
          item-key="id"
          :footer-props="{
          'items-per-page-options': [5, 10, 25, 50, 100]
        }"
          :items-per-page="50"
          :search="search"
          loading-text="Loading data..."
      >
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
        <template v-slot:item.avatar="{ item }">
          <v-avatar
              class="my-2"
              color="secondaryLighter"
              size="30"
              rounded
          >
            <v-img
                :src="item.user.avatar"
            />
          </v-avatar>
        </template>
        <template v-slot:item.submission.valid="{ item }">
          <v-chip
              small
              :color="item.submission.valid ? 'green' : 'grey'"
          >
            <v-icon
                class="mr-1"
                small
                v-text="item.submission.valid ? 'mdi-check' : 'mdi-close'"
            />
            <span
                v-text="item.submission.valid ? 'Valid' : 'Invalid'"
            />
          </v-chip>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import backend from "@/backend";

export default {
  name: "Submissions",
  data() {
    return {
      submissions: undefined,
      submissionsLoading: false,
      loopID: null,
      search: null,
      headers: [
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
          value: 'user.username'
        },
        {
          text: 'Box',
          align: 'start',
          value: 'box.name'
        },
        {
          text: 'Value',
          align: 'start',
          value: 'submission.value'
        },
        {
          text: 'Valid',
          align: 'start',
          value: 'submission.valid'
        },
        {
          text: 'Timestamp',
          align: 'start',
          value: 'submission.flagged_at'
        }
      ]
    }
  },
  methods: {
    loadSubmissions(){
      this.submissionsLoading = true

      backend.listSubmissions().then((res) => {
        if (res.data.data === undefined){
          this.submissions = []
        }else{
          this.submissions = res.data.data
        }
      }).catch(() => {
        this.$toast.error(`Failed to fetch submissions`, { duration: 10000 })
      }).finally(() => {
        this.submissionsLoading = false
      })
    },
  },
  computed: {
    isLoading() {
      return this.submissions === undefined
    },
  },
  beforeRouteLeave(to, from, next){
    clearInterval(this.loopID)
    next()
  },
  beforeMount() {
    this.loadSubmissions()
    this.loopID = setInterval(() => {
      this.loadSubmissions()
    }, 5000)
  },
}
</script>

<style scoped>
.row-pointer >>> tbody tr :hover {
  /*cursor: pointer;*/
}
</style>
