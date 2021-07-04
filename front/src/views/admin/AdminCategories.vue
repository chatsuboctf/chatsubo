<template>
  <v-container>
    <v-card
        color="secondary"
        class="pa-4"
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
                  @click="showNewCategoryDialog = true"
              >
                <v-icon
                    v-text="'mdi-plus'"/>
              </v-btn>
            </template>
            New track
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
                  <!--                        :width="filterCardWidth"-->
                  <card-switch
                      width="400"
                      class="pa-4"
                      no-selected-icon
                      title="Show deleted tracks"
                      subtitle="The deleted tracks will appear in red"
                      icon="mdi-delete"
                      v-model="filters.showDeletedCategories"/>
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
          :headers="categoriesHeaders"
          :loading="isLoading"
          :items="filteredCategories"
          item-key="id"
          show-select
          loading-text="Loading data..."
          :search.sync="search"
      >
        <template v-slot:top>
          <v-container>
            <v-btn
                @click="deleteSelectedCategories"
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

        <template v-slot:item.actions="{ item }">
          <v-row justify="center" align="center" v-if="!item.deleted">
            <v-tooltip transition="slide-fade-transition" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on"
                    @click.stop="beginEditCategory(item)"
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
                    @click.stop="deleteCategory(item)"
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
                    @click.stop="restoreCategory(item)"
                >
                  <v-icon
                      small
                  >
                    mdi-restore
                  </v-icon>
                </v-btn>
              </template>
              Restore
            </v-tooltip>
          </v-row>
        </template>
      </v-data-table>
    </v-card>

    <create-category
        :show.sync="showNewCategoryDialog"
        @create="createNewCategory"
        @click:outside="showNewCategoryDialog = false"
    />
    <edit-category
        :current-category="categoryToEdit"
        :show.sync="showEditCategoryDialog"
        @apply="editCategory"
        @click:outside="showEditCategoryDialog = false"
    />
  </v-container>
</template>

<script>
import backend from "@/backend";
import CardSwitch from "@/components/CardSwitch";
import CreateCategory from "@/components/admin/CreateCategory";
import EditCategory from "@/components/admin/EditCategory";

export default {
  name: "AdminCategories",
  components:{
    CardSwitch,
    CreateCategory,
    EditCategory
  },
  data () {
    return {
      selected: [],
      categories: undefined,
      search: "",
      showNewCategoryDialog: false,
      showEditCategoryDialog: false,
      showFilters: false,
      categoryToEdit: undefined,
      filters: {
        showDeletedCategories: false
      },
      loaders: {
        deleteBulk: false,
        add: false,
        restore: false,
      },
      categoriesHeaders: [
        {
          text: 'Name',
          align: 'start',
          sortable: true,
          value: 'name'
        },
        // {
        //   text: 'Description',
        //   align: 'start',
        //   sortable: true,
        //   value: 'description'
        // },
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
    deleteSelectedCategories () {
      this.loaders.bulkDelete = true
      console.log(this.selected)
      backend.deleteBulkCategories(this.selected)
          .then(() => {
            this.loadAllCategories()
          }).catch((error) => {
        this.$toast.error(`Failed to delete track : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        this.selected = []
        this.loaders.bulkDelete = false
      })
    },
    beginEditCategory (category) {
      console.log(category)
      this.showEditCategoryDialog = true
      this.categoryToEdit = JSON.parse(JSON.stringify(category))
    },
    editCategory (newCategory) {
      backend.editCategory(newCategory)
          .then(() => {
            this.loadAllCategories()
          }).catch((error) => {
        this.$toast.error(`Failed to edit track : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        this.showEditCategoryDialog = false
      })
    },
    restoreCategory (category) {
      category.loaders.restore = true
      backend.restoreCategory(category)
          .then(() => {
            this.loadAllCategories()
          }).catch((error) => {
        this.$toast.error(`Failed to restore track : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        category.loaders.restore = false
      })
    },
    deleteCategory (category) {
      console.log(category)
      category.loaders.delete = true
      backend.deleteCategory(category)
          .then(() => {
            this.loadAllCategories()
          }).catch((error) => {
        this.$toast.error(`Failed to delete track : &lt;${error.message} : ${error.response.data.error}&gt;`, { duration: 10000 })
      }).finally(() => {
        category.loaders.delete = false
      })
    },
    getFilteredCategories () {
      let categories = []
      for (let category of this.categories) {
        if (category.deleted && !this.filters.showDeletedCategories) {
          continue
        }

        categories.push(category)
      }

      return categories
    },
    createNewCategory (newCategory) {
      this.showNewCategoryDialog = false

      backend.createNewCategory(newCategory)
          .then(() => {
            this.$toast.success(`New track created : <b>${newCategory.name}</b>`, { duration: 10000 })

            this.loadAllCategories()
          }).catch((res) => {
        this.$toast.error(`Failed to create track : &lt;${res.message} : ${res.response.data.error}&gt;`, { duration: 10000 })
      })
    },
    loadAllCategories(){
      backend.listCategories().then((res) => {
        this.categories = res.categories
        for (let cat of this.categories){
          cat.loaders = JSON.parse(JSON.stringify(this.loaders))
        }

      }).catch((res) => {
        this.$toast.error(res.response.data.errors.join(" / "))
      })
    },
  },
  computed:{
    isLoading(){
      return this.categories === undefined
    },
    filteredCategories(){
      console.log(this.categories)
      if (this.categories === undefined){
        return []
      }

      let categories = []
      for (let category of this.categories) {
        if (category.deleted && !this.filters.showDeletedCategories) {
          continue
        }

        categories.push(category)
      }

      return categories
    }
  },
  beforeMount() {
    this.loadAllCategories()
  }
}
</script>

<style scoped>

</style>
