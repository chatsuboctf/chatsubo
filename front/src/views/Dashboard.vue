<template>
  <v-container>
    <v-layout
        align-center
        justify-start
        column
    >
      <v-card-text
          v-for="cat in categories"
          :key="cat.name"
      >
        <v-layout
            justify-start
            class="pb-2"
        >
          <v-icon
              small
              class="pr-2"
              v-text="cat.icon"
          />
          <span
              :style="`color: ${$store.getters.getSettings.darkTheme ? 'white' : 'rgba(0,0,0,.87)'} !important;`"
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
</template>

<script>
import BoxCardWall from "@/components/boxes/BoxCardWall";
import backend from "@/backend";

export default {
  name: "Dashboard",
  components:{
    BoxCardWall
  },
  data () {
    return {
      categories: undefined
    }
  },
  methods:{
    boxCardClicked(box){
      this.$router.push(`/box/${box.id}`)
    },
    loadAllCategories(){
      backend.listCategories().then((res) => {
        this.categories = res.categories

      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
  },
  beforeMount() {
    this.loadAllCategories()
    // backend.loadBoxesOf(this.$route.params.category).then((res)=>{
    //   this.boxes = res.data.boxes
    // }).catch((res)=>{
    //   this.$toast.error(res.response.data.errors.join(" / "))
    // })
  },
  computed:{
    isLoading() {
      return this.categories === undefined
    },
  }

}
</script>

<style scoped>

</style>
