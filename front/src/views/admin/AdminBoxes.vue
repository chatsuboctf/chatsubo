<template>
  <v-container>
    <v-card
        class="pa-4"
        color="secondary"
    >
      <v-card-title class="pb-0">
        <v-row>
          <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
          />
          <v-spacer/>
          <v-tooltip transition="slide-fade-transition" bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  icon
                  dark
                  large
                  v-bind="attrs"
                  v-on="on"
                  @click="showNewBoxDialog = true"
              >
                <v-icon
                    v-text="'mdi-plus'"/>
              </v-btn>
            </template>
            New box
          </v-tooltip>

          <v-menu
              :close-on-content-click="false"
          >
            <template v-slot:activator="{ on: menu, attrs }">
              <v-tooltip transition="slide-fade-transition" bottom>
                <template v-slot:activator="{ on: tooltip }">
                  <v-btn
                      icon
                      dark
                      large
                      v-bind="attrs"
                      v-on="{ ...tooltip, ...menu }"
                      @click="showFilters = true"
                  >
                    <v-icon
                        v-text="'mdi-filter-variant'"/>
                  </v-btn>
                </template>
                Filters
              </v-tooltip>
            </template>
            <v-card>
              <v-card-text class="py-1">
                <v-layout
                    justify-center
                    align-center
                    column
                >
                  <card-switch
                      :width="filterCardWidth"
                      class="pa-4"
                      no-selected-icon
                      title="Show deleted boxes"
                      subtitle="The deleted boxes will appear in red"
                      icon="mdi-delete"
                      v-model="filters.showDeletedBoxes"/>
                </v-layout>
              </v-card-text>
            </v-card>
          </v-menu>
        </v-row>
      </v-card-title>

      <v-data-table
          class="secondary"
          @click:row="selectRow"
          v-model="selected"
          :headers="boxesHeaders"
          :loading="isLoading"
          :items="filteredBoxes"
          item-key="id"
          show-select
          loading-text="Loading data..."
          :search.sync="search"
      >
        <template v-slot:top>
          <v-container>
            <v-btn
                @click="deleteSelectedBoxes"
                color="error"
                class="mr-2"
                :loading.sync="loaders.deleteBulk"
                :disabled="selected.length === 0"
                :outlined="selected.length === 0"
            >
              <v-icon left dark>
                mdi-delete
              </v-icon>
              Delete
            </v-btn>
          </v-container>
        </template>

        <template v-slot:item.name="{ item }">
          <span
              :class="{
                    'red--text text--lighten-2': item.deleted
                    }"
              v-text="item.name"
          />
        </template>

        <template v-slot:item.description="{ item }">
          <div
              style="width: 350px"
              class="text-truncate"
              v-text="item.description"
          />
        </template>

        <template v-slot:item.released="{ item }">
          <v-chip
              small
              :color="item.released ? 'green' : 'grey'"
          >
            <v-icon
                class="mr-1"
                small
                v-text="item.released ? 'mdi-earth' : 'mdi-human-cane'"
            />
            <span
                v-text="item.released ? 'Released' : 'Retired'"
            />
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-row justify="center" align="center" v-if="!item.deleted">

            <v-tooltip transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="$router.push(`/box/${item.id}`)"
                >
                  <v-icon
                      small
                  >
                    mdi-open-in-new
                  </v-icon>
                </v-btn>
              </template>
              View
            </v-tooltip>

            <v-tooltip v-if="!item.released" transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="releaseBox(item)"
                >
                  <v-icon
                      small
                  >
                    mdi-earth
                  </v-icon>
                </v-btn>
              </template>
              Release
            </v-tooltip>

            <v-tooltip v-if="item.released" transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="retireBox(item)"
                >
                  <v-icon
                      small
                  >
                    mdi-human-cane
                  </v-icon>
                </v-btn>
              </template>
              Retire
            </v-tooltip>

            <v-tooltip transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="$router.push(`/admin/box/${item.id}`)"
                >
                  <v-icon
                      small
                  >
                    mdi-pencil
                  </v-icon>
                </v-btn>
              </template>
              Edit
            </v-tooltip>


            <v-tooltip transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    :loading.sync="item.loaders.delete"
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="deleteBox(item)"
                >
                  <v-icon
                      small
                      color="error"
                  >
                    mdi-delete
                  </v-icon>
                </v-btn>
              </template>
              Delete
            </v-tooltip>
          </v-row>
          <v-row justify="center" align="center" v-else>
            <v-tooltip transition="slide-fade-transition" bottom>

              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    :loading.sync="item.loaders.restore"
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="restoreBox(item)"
                >
                  <v-icon
                      small
                  >
                    mdi-restore
                  </v-icon>
                </v-btn>
              </template>
              restore
            </v-tooltip>
          </v-row>
        </template>
      </v-data-table>
    </v-card>

    <create-box
        :show.sync="showNewBoxDialog"
        :available-templates="availableTemplates"
        :available-categories="availableCategories.map(cat => cat.name)"
        :available-os="availableOs"
        @create="createNewBox"
        @click:outside="showNewBoxDialog = false"
    />

    <!--    <v-dialog max-width="500px" v-model="showEditBoxDialog">-->
    <!--      <v-card>-->
    <!--        <v-card-title>-->
    <!--          Edit a tag-->
    <!--        </v-card-title>-->
    <!--        <v-container>-->
    <!--          <v-form>-->
    <!--            <v-textarea-->
    <!--                autofocus-->
    <!--                v-model="newBox.description"-->
    <!--                label="Description"-->
    <!--                required-->
    <!--            ></v-textarea>-->
    <!--            &lt;!&ndash;              <v-autocomplete&ndash;&gt;-->
    <!--            &lt;!&ndash;                  v-model="newBox.tags"&ndash;&gt;-->
    <!--            &lt;!&ndash;                  :items="availableBoxs.map(tag => tag.fullname)"&ndash;&gt;-->
    <!--            &lt;!&ndash;                  label="Boxs"&ndash;&gt;-->
    <!--            &lt;!&ndash;                  autofocus&ndash;&gt;-->
    <!--            &lt;!&ndash;                  multiple&ndash;&gt;-->
    <!--            &lt;!&ndash;                  chips&ndash;&gt;-->
    <!--            &lt;!&ndash;              ></v-autocomplete>&ndash;&gt;-->
    <!--            <v-btn-->
    <!--                color="success"-->
    <!--                class="mr-4"-->
    <!--                @click="editBox"-->
    <!--            >-->
    <!--              Apply-->
    <!--            </v-btn>-->
    <!--          </v-form>-->
    <!--        </v-container>-->
    <!--      </v-card>-->
    <!--    </v-dialog>-->
  </v-container>
</template>

<script>
import backend from "@/backend";
import CardSwitch from "@/components/CardSwitch";
import CreateBox from "@/components/admin/CreateBox";

export default {
  name: "AdminBoxes",
  components:{
    CardSwitch,
    CreateBox
  },
  data () {
    return {
      availableTemplates: [],
      availableCategories: [],
      availableOs: ['Linux', 'Windows', 'FreeBSD', 'Other'],
      selected: [],
      boxes: undefined,
      search: "",
      showNewBoxDialog: false,
      showEditBoxDialog: false,
      showFilters: false,
      filters: {
        showDeletedBoxes: false
      },
      loaders: {
        deleteBulk: false,
        add: false,
        release: false,
        restore: false,
      },
      boxesHeaders: [
        {
          text: 'Name',
          align: 'start',
          sortable: true,
          value: 'name'
        },
        {
          text: 'Description',
          align: 'start',
          sortable: true,
          value: 'description'
        },
        {
          text: 'Category',
          align: 'start',
          sortable: true,
          value: 'category.name'
        },
        {
          text: 'Availability',
          align: 'start',
          sortable: true,
          value: 'released'
        },
        {
          text: 'Actions',
          align: 'center',
          sortable: false,
          value: 'actions'
        }
      ],
      filterCardWidth: '300'
    }
  },
  methods: {
    selectRow (row) {
      const idx = this.selected.indexOf(row)
      if (idx === -1) {
        this.selected.push(row)
      } else {
        this.selected.splice(idx, 1)
      }
    },
    deleteSelectedBoxes () {
      this.loaders.bulkDelete = true
      backend.deleteBulkBoxes(this.selected)
          .then(() => {
            this.loadAllBoxes()
          }).catch((error) => {
        this.$toast.error(`Failed to delete box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        this.loaders.bulkDelete = false
      })
    },
    releaseBox(box){
      this.loaders.release = true
      backend.releaseBox(box)
          .then(() => {
            this.loadAllBoxes()
          }).catch((error) => {
        this.$toast.error(`Failed to release box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        this.loaders.release = false
      })
    },
    retireBox(box){
      this.loaders.retire = true
      backend.retireBox(box)
          .then(() => {
            this.loadAllBoxes()
          }).catch((error) => {
        this.$toast.error(`Failed to retire box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        this.loaders.retire = false
      })
    },
    beginEditBox (box) {
      console.log(box)
      //   this.showEditBoxDialog = true
      //   this.newBox = JSON.parse(JSON.stringify(box))
    },
    editBox () {
      //   backend.editBox(this.newBox)
      //     .then(() => {
      //       this.loadAllBoxes()
      //     }).catch((error) => {
      //       this.$toast.error(`Failed to edit box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      //     }).finally(() => {
      //       this.showEditBoxDialog = false
      //       this.newBox.description = ''
      //     })
    },
    restoreBox (box) {
      box.loaders.restore = true
      backend.restoreBox(box)
          .then(() => {
            this.loadAllBoxes()
          }).catch((error) => {
        this.$toast.error(`Failed to restore box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        box.loaders.restore = false
      })
    },
    deleteBox (box) {
      box.loaders.delete = true
      backend.deleteBox(box.id)
      .then(() => {
        this.loadAllBoxes()
      }).catch((error) => {
        this.$toast.error(`Failed to delete box : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        box.loaders.delete = false
      })
    },
    createNewBox (newBox) {
      this.showNewBoxDialog = false
      newBox.category = this.availableCategories.find(cat => cat.name === newBox.category)

      backend.createNewBox(newBox)
          .then(() => {
            this.$toast.success(`New box created : <b>${newBox.name}</b>`, { duration: 10000 })

            this.loadAllBoxes()
          }).catch((err) => {
        this.$toast.error(`Failed to create the box : &lt;${err.message} : ${err.response.data.error}&gt;`, { duration: 10000 })
      })
    },
    loadAllBoxes(){
      backend.listBoxes().then((res) => {
        this.boxes = res.boxes
        for (let box of this.boxes){
          box.category = this.availableCategories.find(cat => cat.id === box.category_id)
        }
        for (let box of this.boxes){
          box.loaders = JSON.parse(JSON.stringify(this.loaders))
        }
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
    loadAllTemplates(){
      backend.listAvailableTemplates().then((res) => {
        this.availableTemplates = res.data.templates
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
    loadAllCategories(){
      backend.listCategories().then((res) => {
        this.availableCategories = res.categories
      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    }
  },
  computed: {
    isLoading(){
      return this.boxes === undefined
    },
    filteredBoxes(){
      if (this.boxes === undefined){
        return []
      }

      let boxes = []
      for (let box of this.boxes) {
        if (box.deleted && !this.filters.showDeletedBoxes) {
          continue
        }

        boxes.push(box)
      }

      return boxes
    }
  },
  watch:{
    availableCategories(){
      // loadAllBoxes needs the categories to be loaded before
      // so we watch the categories to load the boxes only when the categories are loaded
      this.loadAllBoxes()
    }
  },
  beforeMount() {
    this.loadAllCategories()
    this.loadAllTemplates()
  }
}
</script>

<style scoped>

</style>
