<template>
  <v-container>
    <v-layout
        justify-space-between
        fill-height
        align-center
    >
        <span
            class="headline text-h4 font-weight-bold"
        >
        Scoreboard
        </span>
    </v-layout>

    <v-tabs
        v-if="!isLoading"
        v-model="tab"
        class="py-2"
        background-color="transparent"
        dark
        color="white"
    >
      <v-tab
          v-for="item in categories"
          :key="item.id"
      >
        {{ item.name }}
      </v-tab>
    </v-tabs>
    <scoreboard-sheet
        :loading="isLoading"
        :category="currentCategory"
    />
  </v-container>
</template>

<script>
import backend from "@/backend"
import ScoreboardSheet from "@/components/scoreboard/ScoreboardSheet";

export default {
  name: "Scoreboard",
  components:{
    ScoreboardSheet
  },
  data() {
    return {
      tab: null,
      categories: null,
    }
  },
  methods: {
    loadAllCategories(){
      backend.listCategories().then((res) => {
        let allTotalFlags = 0

        for (let cat of res.categories){
          cat.totalFlags = 0
          for (let box of cat.boxes) {
            cat.totalFlags += box.flags.length
            console.log(cat.totalFlags)
          }
          allTotalFlags += cat.totalFlags
        }

        res.categories.unshift({
          id: "all",
          name  : "All",
          totalFlags: allTotalFlags
        })

        this.categories = res.categories

      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
  },
  computed:{
    isLoading() {
      return this.categories === null
    },
    currentCategory(){
      if (this.isLoading){
        return {}
      }

      return this.categories[this.tab]
    }
  },
  beforeMount() {
    this.loadAllCategories()
  },
  watch: {
  }
}
</script>

<style scoped>
.row-pointer >>> tbody tr :hover {
  /*cursor: pointer;*/
}
</style>
