<template>
  <v-card :loading="loading">
    <v-list-item>
      <v-list-item-content>
        <div class="overline mb-1">
          {{ title }}
        </div>
        <v-list-item-title class="headline mb-1">
          {{ description }}
          <slot/>
        </v-list-item-title>
      </v-list-item-content>

      <v-list-item-avatar
          size="70"
      >
        <v-icon
            size="50"
            v-text="icon"
        />
      </v-list-item-avatar>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  name: "BaseCard",
  props:{
    title: String,
    description: String,
    icon: String,
    loading: Boolean
  }

}
</script>

<style scoped>

</style>
