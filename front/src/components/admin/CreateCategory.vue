<template>
  <v-dialog
      v-model="show"
      transition="fade-transition"
      @keydown.ctrl.enter="createNewCategory"
      @click:outside="$emit('click:outside')"
      max-width="700"
  >
    <v-card
      color="secondaryLighter"
    >
      <v-container class="px-6">

        <v-layout
            fill-height
            justify-space-around
            align-center
        >
          <v-form class="fill-height">
            <v-card-title class="px-0">
              Create track
            </v-card-title>
            <v-row>
              <v-col>
                <v-text-field
                    v-model="newCategory.name"
                    label="Name"
                    autofocus
                    :rules="[() => !!newCategory.name || 'This field is required']"
                    counter="200"
                    required
                />
              </v-col>
              <v-col>
                <v-layout
                    justify-center
                    align-center
                >
                  <v-text-field
                      v-model="newCategory.icon"
                      label="Icon"
                      :rules="[() => !!newCategory.icon || 'This field is required']"
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
                        style="width: 48px; height: 48px"
                    >
                      <v-icon
                          v-text="newCategory.icon || 'mdi-castle'"
                      />
                    </v-layout>
                  </v-card>
                </v-layout>
              </v-col>
            </v-row>
<!--            <v-textarea-->
<!--                v-model="newCategory.description"-->
<!--                :rules="[() => !!newCategory.description || 'This field is required']"-->
<!--                label="Description"-->
<!--                counter="300"-->
<!--                required-->
<!--            />-->
            <v-card-actions class="px-0">
              <v-btn
                  color="success"
                  class="mr-4"
                  @click="createNewCategory"
              >
                Create
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-layout>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "CreateCategory",
  components:{
  },
  data () {
    return {
      newCategory: undefined,
    }
  },
  props:{
    show: Boolean
  },
  beforeMount() {
    this.clearNewCategory()
  },
  methods:{
    createNewCategory(){
      this.newCategory.slug = this.$nameToSlug(this.newCategory.name)
      this.$emit("create", this.newCategory)
      this.clearNewCategory()
    },
    clearNewCategory(){
      this.newCategory = {
        name: "",
        slug: "",
        description: "",
        icon: "mdi-castle",
      }
    }
  },
}
</script>

<style scoped>

</style>
