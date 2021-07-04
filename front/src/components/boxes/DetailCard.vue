<template>
  <v-card
      :color="color"
      v-if="extended"
      :loading="loading"
      :flat="flat"
      :outlined="outlined"
  >
    <v-list-item>
      <v-list-item-content>
        <slot name="title">
          <div
              class="overline mb-1"
              v-text="title"
          />
        </slot>
        <slot name="text">
          <v-list-item-title
              class="headline mb-1"
              v-text="text"
          />
        </slot>
      </v-list-item-content>

      <slot name="icon" v-if="!noIcon">
        <v-list-item-avatar
            size="70"
        >
          <v-icon
              :color="iconColor"
              size="50"
              v-text="icon"
          />
        </v-list-item-avatar>
      </slot>
    </v-list-item>
  </v-card>
  <v-card
      v-else
      :color="color"
      :flat="flat"
      :loading="loading"
      class="px-5 py-3"
  >
    <v-layout
        justify-center
        align-center
        column
    >
      <slot v-if="!noIcon" name="icon">
        <v-icon
            :color="iconColor"
            v-text="icon"/>
      </slot>
      <slot name="text">
        <div class="headline">
          {{text}}
        </div>
      </slot>
      <slot name="title">
        <div class="overline">
          {{title}}
        </div>
      </slot>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  name: "DetailCard",
  props:{
    color: String,
    loading: Boolean,
    noIcon: Boolean,
    extended: Boolean,
    outlined: Boolean,
    flat: Boolean,
    iconColor: {
      type: String,
      default: () => null
    },
    icon: String,
    text: String,
    title: String,
  }
}
</script>

<style scoped>

</style>
