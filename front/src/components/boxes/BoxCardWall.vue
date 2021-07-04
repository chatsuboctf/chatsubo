<template>
  <v-container
      v-if="!loading"
      class="pa-0 pb-4"
  >
<!--    <v-card-->
<!--        class="mb-4"-->
<!--    >-->
<!--      <v-app-bar-->
<!--          src="https://picsum.photos/1920/1080?random"-->
<!--          color="#fcb69f"-->
<!--      >-->
<!--        <template v-slot:img="{ props }">-->
<!--          <v-img-->
<!--              v-bind="props"-->
<!--              gradient="to top right, rgba(19,84,122,.5), rgba(128,208,199,.8)"-->
<!--          />-->
<!--        </template>-->
<!--        <v-app-bar-nav-icon></v-app-bar-nav-icon>-->
<!--        <v-app-bar-title>{{ title }}</v-app-bar-title>-->
<!--        <v-spacer></v-spacer>-->

<!--        <v-btn icon>-->
<!--          <v-icon>mdi-magnify</v-icon>-->
<!--        </v-btn>-->
<!--      </v-app-bar>-->
<!--    </v-card>-->
    <h3 v-if="title" class="headline text-h4 font-weight-bold pb-4">{{ category.name }}</h3>
    <v-container
        fluid
        class="pa-0"
    >
      <v-row justify="start">
        <v-col
            md="4"
            class="pa-2"
            v-for="box in boxes" :key="box.name"
        >
          <v-layout
              justify-center
              align-center
          >
            <box-card
                :no-status="showcase"
                :center-label="showcase"
                :disabled="showcase && !box.completed"
                :box="box"
            />
          </v-layout>
        </v-col>
        <v-col
            md="12"
            v-show="boxes.length === 0"
            class="pa-2"
        >
          <v-layout
              justify-center
              align-center
          >
            <box-card
                no-label-icon
                no-status
                :animateHover="false"
                center-label
                disabled
                :box="emptyBox"
            />
          </v-layout>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
  <v-container
      v-else
  >
    <v-overlay
        absolute
        opacity="0"
    >
      <v-progress-circular
          color="white"
          indeterminate
      />
    </v-overlay>

  </v-container>
</template>

<script>
import BoxCard from "@/components/boxes/BoxCard";

export default {
  name: "BoxCardWall",
  components:{
    BoxCard
  },
  props: {
    title: String,
    category: {
      type: Object,
      default: () => {}
    },
    loading: Boolean,
    boxes: {
      type: Array,
      default: () => []
    },
    showcase: Boolean
  },
  methods:{
  },
  data () {
    return {
      emptyBox: {
        name: "Empty"
      }
    }
  }
}
</script>

<style scoped>

</style>
