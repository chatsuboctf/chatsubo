<template>
  <v-dialog
      v-model="show"
      max-width="750"
      transition="fade-transition"
      @keydown.ctrl.enter="createNewBox"
      @click:outside="$emit('click:outside')"
  >
    <v-card
        color="secondaryLighter"
    >
      <v-card-title>
        <v-list-item two-line>
          <v-list-item-content>
            <v-layout
                align-center
                column
                fill-height
                justify-center
            >
              <v-list-item-title>
                New box
              </v-list-item-title>
              <v-list-item-subtitle>
                Create a new box
              </v-list-item-subtitle>
            </v-layout>
          </v-list-item-content>
        </v-list-item>
      </v-card-title>

      <v-stepper
          v-model="stepperModel"
          class="pa-4 transparent elevation-0"
      >
        <v-stepper-header>
          <!--              :editable="step1Complete"-->
          <v-stepper-step
              :complete="step1Complete"
              editable
              edit-icon="mdi-check"
              step="1"
          >
            Box type
          </v-stepper-step>

          <v-divider/>

          <v-stepper-step
              :complete="step2Complete"
              :editable="step1Complete"
              edit-icon="mdi-check"
              step="2"
          >
            Informations
          </v-stepper-step>

          <v-divider/>

          <v-stepper-step
              :complete="step3Complete"
              :editable="step2Complete"
              edit-icon="mdi-check"
              step="3"
          >
            Configuration
          </v-stepper-step>

          <v-divider/>

          <v-stepper-step
              edit-icon="mdi-check"
              step="4"
              :editable="step3Complete"
          >
            Flags
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-content
            step="1"
        >
          <v-row class="fill-height">
            <v-col>
              <v-layout
                  column
                  justify-center
                  align-center
              >
                <v-card-title>
                  Box type
                </v-card-title>
                <v-container>
                  <v-row justify="space-around">
                    <v-col
                        md="6"
                    >
                      <card-switch
                          icon="mdi-webpack"
                          title="Classic"
                          subtitle="Single instance with fixed flags"
                          v-model="classicBox"
                          value="classic"
                      />
                    </v-col>
                    <v-col
                        md="6"
                    >
                      <card-switch
                          icon="mdi-flash-circle"
                          title="Dynamic"
                          subtitle="A new instance for each player"
                          value="classic"
                          v-model="dynamicBox"
                      />
                    </v-col>
                  </v-row>
                </v-container>
              </v-layout>
            </v-col>
          </v-row>
          <v-card-actions
              align-center
              class="pt-6"
              fill-height
              justify-space-between
          >
            <v-btn
                color="grey darken-3"
                disabled
            >
              Previous
            </v-btn>
            <v-spacer/>
            <v-btn
                :disabled="!step1Complete"
                :outlined="!step1Complete"
                color="success"
                @click="stepperModel = '2'"
            >
              Next
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-content
            step="2"
        >
          <v-autocomplete
              outlined
              v-model="newBox.template"
              :items="availableTemplates.filter(tpl => tpl.data.dynamic === dynamicBox)"
              item-value="data"
              item-text="data.name"
              :rules="[() => !!newBox.template || 'This field is required']"
              label="Template"
              @input="syncDockerfileWithTemplate"
              required
          >
            <template v-slot:item="{ item }">
              <span>{{item.data.name}} ({{item.data.provider.kind}}/{{item.data.provider.name}})</span>
            </template>
          </v-autocomplete>
          <v-textarea
              v-if="dynamicBox"
              v-model="newBox.dockerfile"
              readonly
              label="Dockerfile"
          />
          <v-autocomplete
              outlined
              v-model="newBox.category"
              :items="availableCategories"
              :rules="[() => !!newBox.category || 'This field is required']"
              auto-select-first
              label="Track"
              required
          />
          <v-autocomplete
              outlined
              v-model="newBox.os"
              :items="availableOS"
              :rules="[() => !!newBox.os || 'This field is required']"
              auto-select-first
              label="OS"
              required
          />
          <v-text-field
              v-if="dynamicBox"
              v-model="newBox.duration"
              label="Duration"
              type="number"
          />
          <v-row
              align="center"
              justify="center"
          >
            <v-col>
                  <span>
                    Difficulty :
                  </span>
            </v-col>
            <v-col>
              <v-rating
                  v-model="newBox.difficulty"
                  background-color="grey"
                  color="yellow darken-2"
                  dense
                  hover
                  large
                  length="10"
              />
              <!--                  empty-icon="mdi-water-outline"-->
              <!--                  full-icon="mdi-water"-->
            </v-col>
            <v-col>
              <span v-text="$mapValueToDifficulty(newBox.difficulty).text"/>
            </v-col>
          </v-row>
          <v-card-actions
              align-center
              class="pt-6"
              fill-height
              justify-space-between
          >
            <v-btn
                color="grey darken-3"
                @click="stepperModel = '1'"
            >
              Previous
            </v-btn>
            <v-spacer/>
            <v-btn
                :disabled="!step2Complete"
                :outlined="!step2Complete"
                color="success"
                @click="stepperModel = '3'"
            >
              Next
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-content
            step="3"
        >
          <v-row class="fill-height">
            <v-col>
              <v-form class="fill-height">
                <v-text-field
                    v-model="newBox.name"
                    :rules="[() => !!newBox.name || 'This field is required']"
                    autofocus
                    label="Name"
                    required
                />
                <v-textarea
                    v-model="newBox.description"
                    :rules="[() => !!newBox.description || 'This field is required']"
                    label="Description"
                    required
                />
                <!--                <v-text-field-->
                <!--                    v-model="newBox.background"-->
                <!--                    :rules="[() => !!newBox.background || 'This field is required']"-->
                <!--                    label="Background"-->
                <!--                />-->
                <v-autocomplete
                    v-model="newBox.authors"
                    :items="availableAuthors"
                    :loading="authors.loading"
                    :rules="[() => !!newBox.authors.length || 'This field is required']"
                    placeholder="Search users"
                    :search-input.sync="authorsSearch"
                    item-value="id"
                    item-text="username"
                    cache-items
                    chips
                    hide-details
                    hide-no-data
                    label="Author(s)"
                    multiple
                    required
                />
                <!--                <v-text-field-->
                <!--                    v-model="newBox.author"-->
                <!--                    label="Author"-->
                <!--                    :rules="[() => !!newBox.author || 'This field is required']"-->
                <!--                    required-->
                <!--                />-->
              </v-form>
            </v-col>
          </v-row>
          <v-card-actions
              align-center
              class="pt-6"
              fill-height
              justify-space-between
          >
            <v-btn
                color="grey darken-3"
                @click="stepperModel = '2'"
            >
              Previous
            </v-btn>
            <v-spacer/>
            <v-btn
                :disabled="!step3Complete"
                :outlined="!step3Complete"
                color="success"
                @click="stepperModel = '4'"
            >
              Next
            </v-btn>
          </v-card-actions>
        </v-stepper-content>

        <v-stepper-content
            step="4"
        >
          <v-list-item
              v-show="newBox.flags.length === 0"
              two-line
          >
            <v-list-item-content>
              <v-layout
                  align-center
                  column
                  fill-height
                  justify-center
              >
                <v-list-item-title>
                  Add flags
                </v-list-item-title>
                <v-list-item-subtitle>
                  You can add the flags later in the box admin page
                </v-list-item-subtitle>
              </v-layout>
            </v-list-item-content>
          </v-list-item>

          <v-layout
              v-for="(flag, idx) in newBox.flags"
              :key="idx"
              align-start
              column fluid>
            <v-card
                class="pa-4 mb-6"
                color="secondary"
                elevation="4"
            >
              <!--                style="border: 1px solid rgba(255,255,255,.4)"-->
              <v-row>
                <v-col cols="12" class="pb-0">
                  <v-row>
                    <v-col md="8">
                      <v-text-field
                          v-model="flag.name"
                          label="Name"
                          placeholder="Step 1"
                          :rules="[() => !!flag.name || 'This field is required']"
                          required
                      ></v-text-field>
                    </v-col>
                    <v-col md="4">
                      <v-layout
                          justify-center
                          align-center
                      >
                        <v-text-field
                            v-model="flag.icon"
                            label="Icon"
                            :rules="[() => !!flag.icon || 'This field is required']"
                            required
                            class="mr-3"
                        />
                        <v-card
                            height="48px"
                            width="48px"
                            color="primary"
                        >
                          <v-layout
                              justify-center
                              align-center
                              fill-height
                          >
                            <v-icon
                                v-text="flag.icon"
                            />
                          </v-layout>
                        </v-card>
                      </v-layout>
                    </v-col>
                  </v-row>
                </v-col>
                <v-col class="pb-0" cols="9">
                  <v-text-field
                      :disabled="flag.dynamic"
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
                        class="mt-0 mr-4"
                        color="teal ligthen-4"
                        label="Case sensitive"
                        prepend-icon="mdi-format-letter-case"
                    />
                    <v-checkbox
                        v-model="flag.dynamic"
                        class="mt-0"
                        color="teal ligthen-4"
                        label="Dynamic"
                        prepend-icon="mdi-flash-circle"
                    />
                    <v-spacer/>
                    <v-btn
                        color="error"
                        outlined
                        @click="removeFlag(idx)"
                    >
                      <v-icon
                          v-text="'mdi-minus'"
                      />
                    </v-btn>
                  </v-layout>
                </v-col>
              </v-row>
            </v-card>
          </v-layout>
          <v-layout
              align-center
              justify-center
          >
            <v-btn
                color="primary"
                @click="addFlag"
            >
              <v-icon
                  class="mr-1"
                  v-text="'mdi-plus'"
              />
              Add flag
            </v-btn>
          </v-layout>

          <v-card-actions
              class="mt-4"
          >
            <v-btn
                color="grey darken-3"
                @click="stepperModel = '3'"
            >
              Previous
            </v-btn>
            <v-spacer/>
            <v-btn
                class="mr-4"
                color="success"
                @click="createNewBox"
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-stepper-content>
      </v-stepper>

      <v-layout
          align-center
          class="pb-8"
          column
          fill-height
          justify-center
      >
        <box-card
            color=""
            allowUpload
            :box.sync="newBox"
            :blank="true"
            elevation="4"
            with-stats
            icon="mdi-upload"
            animate-hover
        />
      </v-layout>
    </v-card>
  </v-dialog>
</template>

<script>
import BoxCard from "@/components/boxes/BoxCard";
import backend from "@/backend";
import CardSwitch from "@/components/CardSwitch";

import {defaults} from "@/lib/defaults"

export default {
  name: "CreateBox",
  components: {
    BoxCard,
    CardSwitch
  },
  data() {
    return {
      newBox: undefined,
      stepperModel: "1",
      authors: {
        entries: [],
        loading: false,
        textLimit: 100
      },
      authorsSearch: null,
    }
  },
  props: {
    availableTemplates: Array,
    availableCategories: Array,
    availableOS: Array,
    show: Boolean,
  },
  beforeMount() {
    this.clearNewBox()
  },
  methods: {
    syncDockerfileWithTemplate(template){
      if (!this.dynamicBox){
        return
      }

      this.newBox.dockerfile = template.dockerfile
    },
    loadUsers(){
      this.authors.loading = true

      backend.listUsers().then((res) => {
        this.authors.entries = res.users
      }).catch(() => {
        this.$toast.error(`Failed to fetch authors`, { duration: 10000 })
      }).finally(() => {
        this.authors.loading = false
      })
    },
    createNewBox() {
      this.$emit("create", this.newBox)
      this.stepperModel = "1"
      this.clearNewBox()
    },
    addFlag() {
      let newFlag = defaults.flag
      newFlag.dynamic = this.dynamicBox
      this.newBox.flags.push(JSON.parse(JSON.stringify(newFlag)))
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
    clearNewBox() {
      this.newBox = JSON.parse(JSON.stringify(defaults.newBox))
    },
    makeFlags(selectedTemplate){
      // const template = this.availableTemplates.find(tpl => tpl.data.name === selectedTemplate.name)
      for (const [idx, flag] of selectedTemplate.flags.entries()){
        console.log(flag)
        this.addFlag()
        this.newBox.flags[idx].name = flag.name
        this.newBox.flags[idx].value = flag.value
        this.newBox.flags[idx].points = flag.points
        this.newBox.flags[idx].dynamic = this.dynamicBox
      }
    },
    parseLabels(selectedTemplate){
      // const template = this.availableTemplates.find(tpl => tpl.data.name === selectedTemplate.name)
      for (const label in selectedTemplate.labels){
        if (Object.prototype.hasOwnProperty.call(selectedTemplate.labels, label)){
          let key = label.replace("chatsubo.", "")
          if (!Object.keys(this.newBox).includes(key.toLowerCase())){
            continue
          }

          switch (key){
            case "difficulty":
              this.newBox[key] = parseInt(selectedTemplate.labels[label])
              break
            case "template":
              continue
            case "category":
              if (this.availableCategories.includes(key)){
                this.newBox[key] = selectedTemplate.labels[label]
              }
              break
            case "os":
              if (this.availableOS.includes(key)){
                this.newBox[key] = selectedTemplate.labels[label]
              }
              break
            default:
              this.newBox[key] = selectedTemplate.labels[label]
          }
        }
      }
    }
  },
  computed: {
    step1Complete() {
      return this.newBox.kind.length > 0
    },
    step3Complete() {
      return this.newBox.name.length > 0 && this.newBox.description.length > 0 && this.newBox.authors.length > 0
    },
    step2Complete() {
      return this.newBox.template !== undefined && this.newBox.category.length > 0 && this.newBox.os.length > 0 && this.newBox.difficulty > 0
    },
    areAuthorsLoaded(){
      return this.authors.length > 0
    },
    availableAuthors() {
      return this.authors.entries.map(entry => {
        const username = entry.username.length > this.authors.textLimit
            ? entry.username.slice(0, this.authors.textLimit) + '...'
            : entry.username

        return Object.assign({}, entry, {username})
      })
    },
    isLoading(){
      return this.newBox === undefined
    },
    selectedTemplate(){
      if (this.isLoading){
        return ""
      }

      return this.newBox.template
    },
    classicBox: {
      get(){
        return this.newBox.kind === 'classic'
      },
      set(){
        this.newBox.kind = "classic"
      }
    },
    dynamicBox: {
      get(){
        return this.newBox.kind === 'dynamic'
      },
      set(){
        this.newBox.kind = "dynamic"
      }
    },
  },
  watch: {
    authorsSearch() {
      // Items have already been loaded
      if (this.areAuthorsLoaded) return

      // Items have already been requested
      if (this.authors.loading) return

      this.loadUsers()
    },
    "flag.dynamic": {
      handler(val){
        if (val){
          this.flag.value = "dynamic"
        }
      },
      deep: true
    },
    selectedTemplate(val) {
      if (val === undefined){
        return
      }

      if (this.newBox === undefined){
        return
      }

      if (this.newBox.template === undefined){
        return
      }
      this.makeFlags(this.newBox.template)
      this.parseLabels(this.newBox.template)
    }
  }
}
</script>

<style scoped>

</style>
