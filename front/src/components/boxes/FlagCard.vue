<template>
  <v-layout
      align-start
      column fluid>
    <v-card
        class="pa-4 mb-6"
        color="#303030"
    >
      <!--                style="border: 1px solid rgba(255,255,255,.4)"-->
      <v-row>
        <v-col cols="12" class="pb-0">
          <v-text-field
              v-model="flag.name"
              label="Name"
              placeholder="Step 1"
              :rules="[() => !!flag.name || 'This field is required']"
              required
          />
        </v-col>
        <v-col class="pb-0" cols="9">
          <v-text-field
              v-model="flag.value"
              :rules="[() => !!flag.value || 'This field is required']"
              autofocus
              label="Value"
              placeholder="flag{...}"
              required
          />
        </v-col>
        <v-col class="pb-0" cols="1">
          <v-layout
              align-center
              column
              fill-height
              justify-center
          >
            <v-btn
                :loading="flag.loaders.generate"
                icon
                @click="generateFlagFor(flag)"
            >
              <v-icon
                  v-text="'mdi-refresh'"
              />
            </v-btn>
          </v-layout>
        </v-col>
        <v-col class="pb-0" cols="2">
          <v-text-field
              v-model="flag.points"
              label="Points"
              type="number"
          />
        </v-col>
        <v-col class="pb-0">
          <v-layout
              align-center
              fill-height
              justify-start
          >
            <v-checkbox
                v-model="flag.user"
                class="mt-0 mr-4"
                color="teal ligthen-4"
                label="User"
                prepend-icon="mdi-account"
            />
            <v-checkbox
                v-model="flag.root"
                class="mt-0 mr-4"
                color="teal ligthen-4"
                label="Root"
                prepend-icon="mdi-pound-box"
            />
            <v-checkbox
                v-model="flag.case_insensitive"
                class="mt-0"
                color="teal ligthen-4"
                label="Case sensitive"
                prepend-icon="mdi-format-letter-case"
            />
            <v-spacer/>
            <slot name="action-bottom"/>
          </v-layout>
        </v-col>
      </v-row>
    </v-card>
  </v-layout>
</template>

<script>
import backend from "@/backend";
import {defaults} from "@/lib/defaults";

export default {
  name: "FlagCard",
  data() {
    return {}
  },
  methods:{
    addFlag() {
      this.newBox.flags.push(JSON.parse(JSON.stringify(defaults.flag)))
    },
    generateFlagFor(flag) {
      flag.loaders.generate = true
      backend.generateFlag()
          .then((res) => {
            flag.value = `flag{${res.flag}}`
          }).catch(() => {
        this.$toast.error(`Failed to generate flag`, {duration: 10000})
      }).finally(() => {
        flag.loaders.generate = false
      })
    },
    removeFlag(idx) {
      this.newBox.flags.splice(idx, 1)
    },
  }
}
</script>

<style scoped>

</style>
