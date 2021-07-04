<template>
  <v-card
      :color="value ? selectedColor : unselectedColor"
      :class="{
          'unselected-tile' : !value
        }"
      @click="valueLocal = !$props.value"
      :width="width"
  >
<!--      :width="width"-->
<!--      :height="height"-->
    <v-row
        class="fill-height"
        align="center"
        justify="center"
    >
      <v-list-item
          class="justify-start"
          style="width: 100%; height: 100%"
          two-line
          dark
      >
        <v-icon
            color="white"
            class="mr-1"
            size="54"
            v-text="icon"
        />
        <v-list-item-content class="ml-2" dark>
          <v-list-item-title class="headline mb-1" dark>
            {{title}}
          </v-list-item-title>
          <v-list-item-subtitle>{{subtitle}}</v-list-item-subtitle>
        </v-list-item-content>

        <v-scroll-x-reverse-transition v-if="!noSelectedIcon">
          <v-icon
              v-if="value"
              color="white"
              size="48"
              v-text="checkedIcon"
          />
        </v-scroll-x-reverse-transition>
      </v-list-item>
    </v-row>
  </v-card></template>

<script>
export default {
  name: 'CardSwitch',
  props: {
    selectedColor: {
      default: 'accent',
      type: String
    },
    unselectedColor: {
      default: 'grey darken-3',
      type: String
    },
    icon: {
      default: 'mdi-zip-box-outline',
      type: String
    },
    checkedIcon: {
      default: 'mdi-checkbox-marked-circle-outline',
      type: String
    },
    title: String,
    subtitle: String,
    noSelectedIcon: {
      default: false,
      type: Boolean
    },
    width: {
      default: '100%',
      type: String
    },
    height: {
      default: '100%',
      type: String
    },
    value: Boolean
  },
  computed: {
    valueLocal: {
      get: function () {
        return this.value
      },
      set: function (value) {
        this.$emit('input', value)
      }
    }
  },
  data: () => {
    return {

    }
  }
}
</script>

<style scoped>

</style>
