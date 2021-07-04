<template>
  <v-card
      :width="width"
      :height="height"
      @click="$emit('click')"
  >
    <v-layout
        justify-center
        align-center
        fill-height
    >
      <v-icon
          size="50"
          v-text="icon"
      />
    </v-layout>
  </v-card>
</template>

<script>
export default {
  name: "ButtonCard",
  props: {
    icon: {
      type: String,
      default: () => "mdi-download"
    },
    width: {
      type: String,
      default: () => "100"
    },
    height: {
      type: String,
      default: () => "100"
    }
  }
}
</script>

<style scoped>

</style>
