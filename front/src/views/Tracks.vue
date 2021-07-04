<template>
  <v-container fluid >
    <v-layout
        justify-center
        align-center
    >
      <box-card-wall
          :category="category"
          :loading="isLoading"
          :title="$route.params.category.toProperCase()"
          :boxes.sync="boxes"
          @click:card="boxCardClicked"
      />
    </v-layout>
  </v-container>
</template>

<script>
import BoxCardWall from "@/components/boxes/BoxCardWall";
import backend from "@/backend";

export default {
  name: "Tracks",
  components:{
    BoxCardWall
  },
  data() {
    return {
      category: undefined,
      boxes: undefined,
    }
  },
  methods:{
    boxCardClicked(box){
      this.$router.push(`/box/${box.id}`)
    }
  },
  mounted() {
    backend.loadCategory(this.$route.params.category).then((res)=>{
      this.category = res.data.data
    }).catch((res)=>{
      this.$toast.error(res.response.data.errors.join(" / "))
    })

    backend.loadBoxesOf(this.$route.params.category).then((res)=>{
      this.boxes = res.data.boxes
    }).catch((res)=>{
      this.$toast.error(res.response.data.errors.join(" / "))
    })
  },
  computed:{
    isLoading() {
      return this.boxes === undefined
    },
  }
}
</script>

<style scoped>

</style>
