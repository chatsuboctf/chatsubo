<template>
  <v-card
      color="transparent"
      flat
      height="300px"
  >
    <v-row
        v-if="!loading"
        style="height: 100%"
        justify="center"
        align="center"
    >
      <v-col
          md="4"
          order="2"
      >
        <v-layout
            fill-height
            justify-center
            align-center
        >
          <scoreboard-top-card
              :rank="1"
              :user="usersData[0]"
          />
        </v-layout>
      </v-col>
      <v-col
          md="4"
          order="1"
      >
        <v-layout
            v-if="usersData.length > 1"
            justify-center
            align-center
        >
          <scoreboard-top-card
              :rank="2"
              :user="usersData[1]"
          />
        </v-layout>
      </v-col>
      <v-col
          md="4"
          order="3"
      >
        <v-layout
            justify-center
            v-if="usersData.length > 2"
            align-center
        >
          <scoreboard-top-card
              :rank="3"
              :user="usersData[2]"
          />
        </v-layout>
      </v-col>
    </v-row>
    <v-row
        v-else
        style="height: 100%"
        justify="center"
        align="center"
    >
      <v-col
          md="4"
          order="2"
      >
        <v-layout
            fill-height
            justify-center
            align-center
        >
          <v-skeleton-loader
              height="200"
              width="200"
              type="card"
          />
        </v-layout>
      </v-col>
      <v-col
          md="4"
          order="1"
      >
        <v-layout
            justify-center
            align-center
        >
          <v-skeleton-loader
              height="150"
              width="150"
              type="card"
          />
        </v-layout>
      </v-col>
      <v-col
          md="4"
          order="3"
      >
        <v-layout
            justify-center
            align-center
        >
          <v-skeleton-loader
              height="130"
              width="130"
              type="card"
          />
        </v-layout>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>

import ScoreboardTopCard from "@/components/scoreboard/ScoreboardTopCard";

export default {
  components:{
    ScoreboardTopCard
  },
  props: {
    "users": Array,
    "loading": Boolean
  },
  data: () => ({
  }),
  computed:{
    usersData(){
      return this.users !== undefined && this.users.length > 0 ? this.users : []
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
</style>
