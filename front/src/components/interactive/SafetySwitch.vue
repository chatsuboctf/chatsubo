<template>
  <v-card-text>
    <v-layout
      justify-center
      align-center
    >
    <v-btn
        class="mr-2"
        :loading="loading"
        :outlined="!safety"
        :disabled="!safety"
        :color="color"
        @click="clicked"
    >
      <v-icon
          v-text="icon"
          class="mr-2"
      />
      {{ label }}
    </v-btn>
      <!--        :hint="hint"-->
<!--        :append-icon=""-->
    <v-switch
        class="mt-0"
        dense
        :disabled="disabled"
        hide-details
        :color='color'
        persistent-hint
        v-model="safety"
        :label="safetyLabel"
    />
    </v-layout>
    <v-layout
      justify-center
      align-center
    >
    <span
        class="small-caption pt-2"
        style="font-size: 13px !important;"
    >
      {{hint}}
    </span>
    </v-layout>
  </v-card-text>
</template>

<script>
export default {
  name: "SafetySwitch",
  props:{
    color: String,
    icon: String,
    label: String,
    disabled: Boolean,
    loading: Boolean,
    safetyLabel: {
      type: String,
      default: () => "Safety"
    },
    hint: {
      type: String,
      default: () => "You won't be prompted for confirmation"
    }
  },
  data () {
    return {
      safety: false,
    }
  },
  methods:{
    clicked(){
      this.safety = false
      this.$emit('click')
    }
  }
}
</script>

<style scoped>

</style>
