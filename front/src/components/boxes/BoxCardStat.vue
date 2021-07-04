<template>
  <div
    class="mr-2"
  >
    <v-tooltip
        bottom
    >
      <template v-slot:activator="{ on, attrs }">
        <v-layout
            justify-start
            align-center
            v-bind="attrs"
            v-on="on"
        >
          <v-icon
              :color="color"
              small v-text="icon"
              class="mr-1"
          />
          <div
              v-text="stat"
              class="overline"
              :style="`line-height: 1.3rem; color: ${color} !important; font-size: 14px`"
          />
        </v-layout>
      </template>
      <span>{{ tooltip }}</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "BoxCardStat",
  props:{
    color: String,
    icon: String,
    stat: String,
    tooltip: String
  }
}
</script>

<style scoped>

</style>
