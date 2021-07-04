<template>
    <v-card
        width="400"
        min-height="250"
        @click="$emit('click', $event)"
    >
      <v-img
          style="position: absolute; width: 100%; height: 100%"
          :src="background"
          class="white--text pa-6"
          gradient="to bottom, rgba(0,0,0,.4), rgba(0,0,0,.4)"
      >
        <!--    <v-overlay-->
        <!--        color="primary"-->
        <!--        class="pa-6 fill-height"-->
        <!--        style="height: 100%; width: 100%"-->
        <!--        absolute-->
        <!--    >-->
        <v-layout
            column
            fluid
            fill-height
            justify-space-between
        >
          <v-card-title
              class="text-h4"
          >
            <v-layout
              fluid
              justify-center
              align-center
            >
              {{title}}
            </v-layout>
          </v-card-title>
          <v-card-text>
            <pre style="white-space: pre-wrap">
{{description}}
            </pre>
          </v-card-text>

        </v-layout>
      </v-img>
      <!--    </v-overlay>-->
      <!--      :color="background"-->
    </v-card>
</template>

<script>
export default {
  name: "BoxCard",
  props:{
    title: String,
    description: String,
    background: String
  }
}
</script>

<style scoped>
  .box-card{
    border: 1px solid white;
  }
</style>
