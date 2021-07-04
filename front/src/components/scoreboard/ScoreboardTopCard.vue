<template>
  <v-card
      :width="meta.size"
      :height="meta.size"
      :elevation="meta.elevation"
  >
    <v-card
        flat
        color="transparent"
    >
      <v-layout
          align-center
          fill-height
          justify-start
          column
      >
        <v-avatar
            class="elevation-6"
            color="secondaryLighter"
            rounded="lg"
            :size="meta.size"
        >
          <v-img
              :width="meta.size"
              :height="meta.size"
              :src="user.avatar"
          />
        </v-avatar>
        <v-sheet
            class="px-3 overline top-card"
            rounded
            elevation="8"
            :style="`z-index: 999; margin-top: -40px; background-color: rgba(0,0,0,.85)`"
        >
          <v-layout
              align-center
              justify-space-around
          >
            <v-icon
                small
                :style="`color:rgb(${meta.color})`"
                v-text="meta.icon"
                class="pr-2"
            />
            <span
                :style="`color:rgb(${meta.color})`"
            >
              {{user.username}}
            </span>
          </v-layout>
        </v-sheet>
      </v-layout>
    </v-card>
  </v-card>
</template>

<script>

export default {
  props: {
    "user": Object,
    "rank": Number
  },
  data: () => ({
  }),
  methods:{
    mapRankToMeta(){

      let meta = {
        "size": 100
      }

      switch (this.rank){
        case 1:
          meta = {
            "size": 200,
            "color": "255, 215, 0",
            "elevation": 10,
            "icon": "mdi-trophy-award"
          }
          break
        case 2:
          meta = {
            "size": 150,
            "color": "192, 192, 192",
            "elevation": 6,
            "icon": "mdi-trophy"
          }
          break
        case 3:
          meta = {
            "size": 130,
            "color": "176, 141, 87",
            "elevation": 4,
            "icon": "mdi-trophy-variant"
          }
          break
      }

      return meta
    }
  },
  computed:{
    meta(){
      console.log(this.user)
      return this.mapRankToMeta()
    }
  },
  mounted () {
  }
}
</script>
