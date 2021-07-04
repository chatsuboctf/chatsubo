<template>
  <v-container>
    <v-layout
        v-if="!isLoading"
        justify-center
        align-center
        class="pb-8"
    >
      <box-card
          allowUpload
          :box="box"
          icon="mdi-pencil"
      />
    </v-layout>
    <v-row
        v-if="!isLoading"
    >
      <v-col sm="12" md="6">
        <v-form
            @submit.prevent=""
            class="mb-6"
        >
          <v-card
              color="secondary"
          >
            <v-toolbar color="secondaryLighter" dark dense flat>
              <v-toolbar-title
                  class="d-flex justify-center align-center subtitle-1"
              >
                <v-icon
                    class="mr-1"
                    v-text="'mdi-information'"
                />
                Informations
              </v-toolbar-title>
            </v-toolbar>
            <div class="overline pa-4 pb-0 px-4 grey--text">
              General
            </div>
            <v-card-text>
              <v-form class="fill-height">
                <v-text-field
                    color="accent"
                    v-model="box.name"
                    label="Name"
                    :rules="[() => !!box.name || 'This field is required']"
                    required
                ></v-text-field>
                <v-textarea
                    color="accent"
                    v-model="box.description"
                    :rules="[() => !!box.description || 'This field is required']"
                    label="Description"
                    required
                />
                <v-autocomplete
                    color="accent"
                    item-color="accent"
                    background-color="secondary"
                    :search-input.sync="authorsSearch"
                    v-model="box.authors"
                    :items="availableAuthors"
                    :loading="authors.loading"
                    :rules="[() => !!box.authors.length || 'This field is required']"
                    placeholder="Search users"
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
              </v-form>
            </v-card-text>
          </v-card>
        </v-form>

        <v-card
            color="secondary"
        >
          <v-toolbar color="secondaryLighter" dark dense flat>
            <v-toolbar-title
                class="d-flex justify-center align-center subtitle-1"
            >
              <v-icon
                  v-text="'mdi-cog-box'"
                  class="mr-1"
              />
              Advanced
            </v-toolbar-title>
          </v-toolbar>
          <v-alert
              dense
              text
              type="error"
              class="mb-0 pa-4"
              icon="mdi-information-outline"
              tile
          >
            Every action in this section have an impact on the box availability.
          </v-alert>
          <div class="overline pa-4 pb-0 px-4 error--text">
            Danger zone
          </div>
          <v-row
              class="px-4"
              justify="space-around"
          >
            <!--            <v-col-->
            <!--                sm="6"-->
            <!--            >-->
            <!--              <v-btn-->
            <!--                  :outlined="!safeties.retireOrRelease"-->
            <!--                  :disabled="!safeties.retireOrRelease"-->
            <!--                  :color="box.released ? 'warning':'success'"-->
            <!--                  :loading="loaders.retireOrRelease"-->
            <!--                  @click="retireOrRelease"-->
            <!--              >-->
            <!--                &lt;!&ndash;                :loading="resetBoxLoader"&ndash;&gt;-->
            <!--                <v-icon-->
            <!--                    v-text="box.released ? 'mdi-human-cane':'mdi-earth'"-->
            <!--                    class="mr-2"-->
            <!--                />-->
            <!--                {{box.released ? 'Retire':'Release'}}-->
            <!--              </v-btn>-->
            <!--              <v-switch hint="You won't be prompted for confirmation"-->
            <!--                        :color="box.released ? 'warning':'success'"-->
            <!--                        persistent-hint-->
            <!--                        v-model="safeties.retireOrRelease"-->
            <!--                        label="Safety"/>-->
            <!--            </v-col>-->
            <v-col
                sm="6"
                v-if="box.released"
            >
              <safety-switch
                  label="Retire"
                  :loading.sync="loaders.retire"
                  color="warning"
                  @click="retireBox"
                  icon="mdi-human-cane"
              />
            </v-col>
            <v-col
                sm="6"
                v-if="!box.released"
            >
              <safety-switch
                  label="Release"
                  :loading.sync="loaders.release"
                  color="primary"
                  @click="releaseBox"
                  icon="mdi-earth"
              />
            </v-col>
            <!--            <v-col-->
            <!--                sm="6"-->
            <!--                v-if="!box.released"-->
            <!--            >-->
            <!--              <v-btn-->
            <!--                  :outlined="!safeties.release"-->
            <!--                  :disabled="!safeties.release"-->
            <!--                  color="success"-->
            <!--                  :loading.sync="loaders.release"-->
            <!--                  @click="releaseBox"-->
            <!--              >-->
            <!--                &lt;!&ndash;                :loading.sync="resetBoxLoader"&ndash;&gt;-->
            <!--                <v-icon-->
            <!--                    v-text="'mdi-earth'"-->
            <!--                    class="mr-2"-->
            <!--                />-->
            <!--                Release-->
            <!--              </v-btn>-->
            <!--              <v-switch hint="You won't be prompted for confirmation"-->
            <!--                        color='success'-->
            <!--                        persistent-hint-->
            <!--                        v-model="safeties.release"-->
            <!--                        label="Safety"/>-->
            <!--            </v-col>-->
            <!--            <v-col-->
            <!--                sm="6"-->
            <!--                v-if="box.released"-->
            <!--            >-->
            <!--              <v-btn-->
            <!--                  :outlined="!safeties.retire"-->
            <!--                  :disabled="!safeties.retire"-->
            <!--                  :loading.sync="loaders.retire"-->
            <!--                  color="warning"-->
            <!--                  @click="retireBox"-->
            <!--              >-->
            <!--                &lt;!&ndash;                :loading.sync="resetBoxLoader"&ndash;&gt;-->
            <!--                <v-icon-->
            <!--                    v-text="'mdi-human-cane'"-->
            <!--                    class="mr-2"-->
            <!--                />-->
            <!--                Retire-->
            <!--              </v-btn>-->
            <!--              <v-switch hint="You won't be prompted for confirmation"-->
            <!--                        color='warning'-->
            <!--                        persistent-hint-->
            <!--                        v-model="safeties.retire"-->
            <!--                        label="Safety"/>-->
            <!--            </v-col>-->

            <v-col
                sm="6"
                v-if="box.deleted"
            >
              <safety-switch
                  label="Restore"
                  :loading.sync="loaders.restore"
                  color="secondaryLighter"
                  @click="restoreBox"
                  icon="mdi-refresh"
              />
            </v-col>
            <v-col
                sm="6"
                v-if="!box.deleted"
            >
              <safety-switch
                  label="Delete"
                  :loading.sync="loaders.delete"
                  color="error"
                  @click="deleteBox"
                  icon="mdi-delete"
              />
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col sm="12" md="6">
        <v-form
            @submit.prevent=""
            class="mb-6"
        >
          <v-card
              color="secondary"
          >
            <v-toolbar color="secondaryLighter" dark dense flat>
              <v-toolbar-title
                  class="d-flex justify-center align-center subtitle-1"
              >
                <v-icon
                    class="mr-1"
                    v-text="'mdi-cog'"
                />
                Configuration
              </v-toolbar-title>
            </v-toolbar>
            <div class="overline pa-4 pb-0 px-4 grey--text">
              Preview
            </div>
            <v-card-text>
              <v-autocomplete
                  v-model="box.template"
                  :items="availableTemplates"
                  item-text="data.name"
                  item-value="data.name"
                  color="accent"
                  item-color="accent"
                  label="Template"
                  :rules="[() => !!box.template || 'This field is required']"
                  auto-select-first
                  required
              />
              <v-autocomplete
                  v-model="box.category_id"
                  :items="availableCategories"
                  item-text="name"
                  item-value="id"
                  label="Category"
                  color="accent"
                  item-color="accent"
                  :rules="[() => !!box.category || 'This field is required']"
                  auto-select-first
                  required
              />
              <v-text-field
                  color="accent"
                  :rules="[() => !!box.background || 'This field is required']"
                  v-model="box.background"
                  label="Background"
              />
              <v-text-field
                  color="accent"
                  v-if="box.kind === 'dynamic'"
                  v-model="box.duration"
                  label="Duration"
                  type="number"
              />
              <v-row
                  justify="center"
                  align="center"
              >
                <v-col cols="2">
                    <span>
                      Difficulty
                    </span>
                </v-col>
                <v-col cols="7">
                  <v-layout
                      justify-center
                      align-center
                  >
                    <v-rating
                        v-model="box.difficulty"
                        background-color="grey"
                        color="yellow darken-2"
                        dense
                        length="10"
                        hover
                    />
                  </v-layout>
                </v-col>
                <v-col cols="3">
                  <v-layout
                      justify-start
                      align-center
                  >
                    <v-icon
                        class="mr-2"
                        v-text="$mapValueToDifficulty(box.difficulty).icon"
                        :color="$mapValueToDifficulty(box.difficulty).color"
                    />
                    <span v-text="$mapValueToDifficulty(box.difficulty).text"/>
                  </v-layout>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-form>
        <v-card
            color="secondary"
        >
          <v-toolbar
              color="secondaryLighter"
              dark
              dense
              flat
              class="mb-2"
          >
            <v-toolbar-title
                class="d-flex justify-center align-center subtitle-1"
            >
              <v-icon
                  class="mr-1"
                  v-text="'mdi-flag'"
              />
              Flags
            </v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-layout
                align-start
                column
                fluid
                :key="idx" v-for="(flag, idx) in box.flags">
              <v-card
                  class="pa-4 mb-6 mx-2"
                  outlined
                  color="secondaryLighter"
              >
                <!--                style="border: 1px solid rgba(255,255,255,.4)"-->
                <v-row>
                  <v-col cols="12" class="pb-0">
                    <v-row>
                      <v-col md="6">
                        <v-text-field
                            color="accent"
                            v-model="flag.name"
                            label="Name"
                            placeholder="Step 1"
                            :rules="[() => !!flag.name || 'This field is required']"
                            required
                        ></v-text-field>
                      </v-col>
                      <v-col md="6">
                        <v-layout
                            justify-center
                            align-center
                            fill-height
                            fluid
                            class="ma-0"
                        >
                          <v-text-field
                              color="accent"
                              v-model="flag.icon"
                              label="Icon"
                              :rules="[() => !!flag.icon || 'This field is required']"
                              required
                              class="mr-3"
                          />
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <a href="https://materialdesignicons.com"
                                 target="_blank"
                                 class="caption ml-2"
                              >
                                <v-card
                                    v-bind="attrs"
                                    v-on="on"
                                    height="50"
                                    width="50"
                                    color="primary"
                                >
                                  <v-layout
                                      justify-center
                                      align-center
                                      fill-height
                                      class="ma-0"
                                  >
                                    <v-icon
                                        v-text="flag.icon"
                                    />
                                  </v-layout>
                                </v-card>
                              </a>
                            </template>
                            <span>Available icons</span>
                          </v-tooltip>

                        </v-layout>
                      </v-col>
                    </v-row>
                  </v-col>

                  <v-col cols="9" class="pb-0">
                    <v-text-field
                        color="accent"
                        :disabled="flag.dynamic"
                        v-model="flag.value"
                        label="Value"
                        placeholder="flag{...}"
                        :rules="[() => !!flag.value || 'This field is required']"
                        required
                    ></v-text-field>
                  </v-col>
                  <v-col cols="1" class="pb-0">
                    <v-layout
                        fill-height
                        justify-center
                        align-center
                        column
                    >
                      <v-btn
                          icon
                          :disabled="flag.dynamic"
                          :loading="flag.loaders.generate"
                          @click="generateFlagFor(flag)"
                      >
                        <v-icon
                            v-text="'mdi-refresh'"
                        />
                      </v-btn>
                    </v-layout>
                  </v-col>
                  <v-col cols="2" class="pb-0">
                    <v-text-field
                        color="accent"
                        label="Points"
                        v-model="flag.points"
                        type="number"
                    />
                  </v-col>
                </v-row>
                <v-row
                    no-gutters
                >
                  <!--                    <v-layout-->
                  <!--                        fill-height-->
                  <!--                        justify-start-->
                  <!--                        align-center-->
                  <!--                    >-->
                  <v-col
                      sm="6"
                  >
                    <v-checkbox
                        v-model="flag.user"
                        prepend-icon="mdi-account"
                        hide-details
                        class="mt-0 mr-4"
                        color="teal ligthen-4"
                        label="User"
                    />
                  </v-col>

                  <v-col
                      sm="6"
                  >
                    <v-checkbox
                        v-model="flag.root"
                        color="teal ligthen-4"
                        class="mt-0 mr-4"
                        prepend-icon="mdi-pound-box"
                        hide-details
                        label="Root"
                    />
                  </v-col>
                  <v-col
                      sm="6"
                  >
                    <v-checkbox
                        v-model="flag.case_insensitive"
                        color="teal ligthen-4"
                        class="mt-0 mr-4"
                        prepend-icon="mdi-format-letter-case"
                        hide-details
                        label="Case sensitive"
                    />
                  </v-col>
                  <v-col
                      sm="6"
                  >
                    <v-checkbox
                        v-model="flag.dynamic"
                        class="mt-0"
                        color="teal ligthen-4"
                        label="Dynamic"
                        prepend-icon="mdi-flash-circle"
                        hide-details
                    />
                  </v-col>
                  <!--                    </v-layout>-->
                </v-row>
                <v-row
                    no-gutters
                    class="pt-4"
                >
                  <v-col>
                    <v-layout
                        justify-center
                        align-center
                    >
                      <v-btn
                          v-if="!flag.deleted && !flag.stub"
                          outlined
                          color="error"
                          :loading="flag.loaders.delete"
                          @click="deleteFlag(flag)"
                      >
                        <v-icon
                            v-text="'mdi-delete'"
                        />
                      </v-btn>
                      <v-btn
                          v-if="!flag.deleted && flag.stub"
                          outlined
                          color="error"
                          :loading="flag.loaders.delete"
                          @click="removeFlag(idx)"
                      >
                        <v-icon
                            v-text="'mdi-minus'"
                        />
                      </v-btn>
                      <v-btn
                          v-else-if="flag.deleted"
                          outlined
                          color="grey"
                          :loading="flag.loaders.restore"
                          @click="restoreFlag(flag)"
                      >
                        <v-icon
                            v-text="'mdi-refresh'"
                        />
                      </v-btn>                    </v-layout>
                  </v-col>
                </v-row>
              </v-card>
            </v-layout>
            <v-layout
                align-center
                justify-center
                class="mb-1"
            >
              <v-btn
                  color="accent"
                  @click="addFlag"
              >
                <v-icon
                    v-text="'mdi-plus'"
                />
                Add flag
              </v-btn>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <update-snackbar
        v-model="showBottomSaveSnackbar"
        :allow-save="showBottomSaveSnackbar"
        :loading="saveCurrentSettingsLoader"
        @save="saveCurrentSettings"
        @reset="restoreSettings"
    />
  </v-container>
</template>

<script>
import backend from "@/backend";
import BoxCard from "@/components/boxes/BoxCard";
import {defaults} from "@/lib/defaults";
import SafetySwitch from "@/components/interactive/SafetySwitch";
import UpdateSnackbar from "@/components/interactive/UpdateSnackbar";

export default {
  name: "AdminBoxProfile",
  components:{
    BoxCard,
    SafetySwitch,
    UpdateSnackbar
  },
  data () {
    return {
      showSnackbar: false,
      safeties: {
        retireOrRelease: false,
        restore: false,
        delete: false,
        release: false,
        retire: false
      },
      authors: {
        entries: [],
        loading: false,
        textLimit: 60
      },
      authorsSearch: null,
      availableTemplates: [],
      availableCategories: [],
      box: undefined,
      originalBox: undefined,
      showBottomSaveSnackbar: false,
      saveCurrentSettingsLoader: false,
      // resetBoxLoader: false,
      flagLoaders: {
        restore: false,
        delete: false,
        generate: false,
      },
      loaders: {
        retireOrRelease: false,
        release: false,
        retire: false,
        restore: false,
        delete: false,
      },
      // flagDefault: {
      //   name: "",
      //   icon: "mdi-flag",
      //   value: "",
      //   user: false,
      //   root: false,
      //   case_insensitive: false,
      //   points: 0,
      //   loaders: {
      //     generate: false
      //   }
      // }
    }
  },
  methods:{
    addFlag() {
      this.box.flags.push(JSON.parse(JSON.stringify(defaults.flag)))
    },
    loadUsers(){
      this.authors.loading = true

      backend.listUsers().then((res) => {
        this.authors.entries = res.users
        console.log(this.authors)
      }).catch(() => {
        this.$toast.error(`Failed to fetch authors`, { duration: 10000 })
      }).finally(() => {
        this.authors.loading = false
      })
    },
    removeFlag(idx){
      this.box.flags.splice(idx, 1)
    },
    deleteFlag(flag){
      flag.loaders.delete = true
      backend.deleteFlag(flag.id).then(() => {
        this.$toast.success(`Flag deleted`, { duration: 10000 })
        this.loadBox()
      }).catch(() => {
        this.$toast.error(`Failed to delete flag`, { duration: 10000 })
      }).finally(() => {
        flag.loaders.delete = false
      })
    },
    restoreFlag(flag){
      flag.loaders.restore = true
      backend.restoreFlag(flag.id).then(() => {
        this.$toast.success(`Flag restored`, { duration: 10000 })
        this.loadBox()
      }).catch(() => {
        this.$toast.error(`Failed to restore flag`, { duration: 10000 })
      }).finally(() => {
        flag.loaders.restore = false
      })
    },
    generateFlagFor(flag) {
      flag.loaders.generate = true
      backend.generateFlag().then((res) => {
        flag.value = `flag{${res.flag}}`
      }).catch(() => {
        this.$toast.error(`Failed to generate flag`, { duration: 10000 })
      }).finally(() => {
        flag.loaders.generate = false
      })
    },
    restoreBox () {
      this.loaders.restore = true
      backend.restoreBox(this.box).then(() => {
        this.loadBox()
        this.$toast.success("Box restored")
      }).catch((res) => {
        if (res.data){
          this.$toast.error(res.data.errors.join(" / "))
        }else{
          this.$toast.error(res.error)
        }
      }).finally(() => {
        this.safeties.restore = false
        this.loaders.restore = false
      })
    },
    deleteBox () {
      this.loaders.delete = true
      backend.deleteBox(this.box.id).then(() => {
        this.loadBox()
        this.$toast.success("Box deleted")
      }).catch((res) => {
        if (res.data){
          this.$toast.error(res.data.errors.join(" / "))
        }else{
          this.$toast.error(res.error)
        }
      }).finally(() => {
        this.safeties.delete = false
        this.loaders.delete = false
      })
    },
    retireOrRelease(){
      if(this.box.released){
        this.retireBox()
      } else{
        this.releaseBox()
      }
    },
    releaseBox(){
      this.loaders.release = true
      backend.releaseBox(this.box).then(() => {
        this.loadBox()
        this.$toast.success("Box released")
      }).catch((res) => {
        if (res.data){
          this.$toast.error(res.data.errors.join(" / "))
        }else{
          this.$toast.error(res.error)
        }
      }).finally(() => {
        this.safeties.release = false
        this.loaders.release = false
      })
    },
    retireBox(){
      this.loaders.retire = true
      backend.retireBox(this.box).then(() => {
        this.loadBox()
        this.$toast.success("Box retired")
      }).catch((res) => {
        if (res.data){
          this.$toast.error(res.data.errors.join(" / "))
        }else{
          this.$toast.error(res.error)
        }
      }).finally(() => {
        this.safeties.retire = false
        this.loaders.retire = false
      })
    },
    loadAllTemplates(){
      backend.listAvailableTemplates().then((res) => {
        this.availableTemplates = res.data.templates
        console.log(res)
      }).catch((res) => {
        console.log(res)
        this.$toast.error(res.data.errors.join(" / "))
      })
    },
    loadAllCategories(){
      backend.listCategories().then((res) => {
        this.availableCategories = res.categories
        console.log(res)
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
    restoreSettings () {
      this.showBottomSaveSnackbar = false
      this.box = JSON.parse(JSON.stringify(this.originalBox))
    },
    saveCurrentSettings () {
      for (const flag of this.box.flags){
        if (flag.name === "" || flag.icon.length <= "mdi-".length){
          if (!flag.dynamic && flag.value === ""){
            this.$toast.error("Incomplete flag")
            this.showBottomSaveSnackbar = false

            return
          }
        }
      }

      this.saveCurrentSettingsLoader = true

      if (this.box.authors.length > 0 && this.box.authors[0] instanceof Object){
        this.box.authors = this.box.authors.map(author => author.id)
      }

      backend.editBox(this.box).then(() => {
        this.$toast.success("Settings updated")
      }).catch((res) => {
        this.$toast.error(res.data.errors.join(" / "))
      }).finally(() => {
        this.showBottomSaveSnackbar = false
        this.saveCurrentSettingsLoader = false
        this.originalBox = JSON.parse(JSON.stringify(this.box))
      })
    },
    loadBox(){
      backend.getBox(this.$route.params.id).then((res) => {
        for (let idx in res.data.boxes[0].flags){
          res.data.boxes[0].flags[idx].loaders = JSON.parse(JSON.stringify(this.flagLoaders))
        }

        this.box = res.data.boxes[0]
        this.originalBox = JSON.parse(JSON.stringify(this.box))
      }).catch((error) => {
        this.$toast.error(`Failed to fetch box : &lt;${error.message} : ${error.response.data.errors}&gt;`, { duration: 10000 })
      })
    }
  },
  computed: {
    isLoading() {
      return this.box === undefined
    },
    isAuthorsLoaded(){
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
  },
  watch: {
    box: {
      handler (val) {
        this.showBottomSaveSnackbar = JSON.stringify(val) !== JSON.stringify(this.originalBox);
      },
      deep: true
    },
    authorsSearch() {
      // Items have already been loaded
      if (this.isAuthorsLoaded) return

      // Items have already been requested
      if (this.authors.loading) return

      this.loadUsers()
    }
  },
  mounted() {
    this.loadUsers()
    this.loadBox()
    this.loadAllCategories()
    this.loadAllTemplates()
  }
}
</script>

<style scoped>

</style>
