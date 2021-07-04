<template>
  <v-snackbar
      color="secondaryLighter"
      class="pb-4"
      v-model="value"
      :timeout="-1"
  >
    {{text}}
    <template v-slot:action="{ attrs }">
      <v-btn
          class="ml-2"
          text
          v-bind="attrs"
          @click="$emit('reset')"
      >
        {{resetLabel}}
      </v-btn>
      <v-btn
          :disabled="!allowSave"
          :outlined="!allowSave"
          class="ml-2"
          :color="saveColor"
          v-bind="attrs"
          :loading="loading"
          @click="$emit('save')"
      >
        {{saveLabel}}
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: "UpdateSnackbar",
  props:{
    text:{
      type: String,
      default: () => "You have unsaved changes"
    },
    resetLabel:{
      type: String,
      default: () => "reset"
    },
    saveLabel:{
      type: String,
      default: () => "save"
    },
    saveColor:{
      type: String,
      default: () => "success"
    },
    loading: Boolean,
    value: Boolean,
    allowSave: Boolean
  },
  data(){
    return {
    }
  }
}
</script>

<style scoped>

</style>
