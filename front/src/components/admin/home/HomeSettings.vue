<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn-toggle
            v-model="selectedViewMode"
        >
          <v-btn>
            <v-icon>mdi-pencil</v-icon>
          </v-btn>

          <v-btn>
            <v-icon>mdi-arrow-split-vertical</v-icon>
          </v-btn>

          <v-btn>
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </v-btn-toggle>
      </v-col>
      <v-col>
        <v-layout
            justify-end
            align-center
            fill-height
        >
          <v-btn
              color="green"
              @click="saveHomePage"
          >
            <v-icon
                class="mr-2"
                v-text="'mdi-content-save'"
            />
            Save
          </v-btn>
        </v-layout>
      </v-col>
    </v-row>
    <v-row
      style="height: 100%"
    >
      <v-col
          v-if="selectedViewMode !== viewModes.view"
      style="height: 100%"
      >
        <v-textarea
            hide-details
            auto-grow
            style="resize: vertical"
            height="100%"
            filled
            :value="input"
            @input="update"
        />
      </v-col>
      <v-col
          v-if="selectedViewMode !== viewModes.edit"
      >
        <v-layout
            justify-center
            fill-height
        >
          <v-card
              elevation="4"
              width="100%"
              color="secondary"
          >
            <v-card-text
                class="px-8"
                style="line-height: 28px"
                v-html="compiledMd"
            />
          </v-card>
        </v-layout>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-layout
            justify-end
            align-end
        >
          <v-btn
              color="green"
              @click="saveHomePage"
          >
            <v-icon
                class="mr-2"
                v-text="'mdi-content-save'"
            />
            Save
          </v-btn>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import marked from "marked"
import {debounce} from "lodash"
import backend from "@/backend";

export default {
  name: "HomeSettings",
  data() {
    return {
      input: this.$store.getters.getSettings.homepage,
      selectedViewMode: 1,
      viewModes: {
        "edit": 0,
        "split": 1,
        "view": 2
      }
    }
  },
  computed: {
    compiledMd: function() {
      return marked(this.input, { breaks: true });
    }
  },
  methods: {
    saveHomePage(){
      backend.saveHomePage(this.input)
          .then(() => {
            this.$toast.success("Home page updated")
          }).catch((error) => {
        this.$toast.error(`Failed to save home page : &lt${error.message} : ${error.response.data.error}&gt`, { duration: 10000 })
      })

    },
    update: debounce(function(content) {
      this.input = content;
    }, 300)
  }
}
</script>

<style scoped>

</style>
