<template>
  <v-dialog
      v-model="show"
      transition="fade-transition"
      @keydown.ctrl.enter="editCategory"
      @click:outside="$emit('click:outside')"
      max-width="500"
  >
    <v-card>
      <v-card-title>
        Edit
      </v-card-title>
      <v-container>
        <v-form>
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
                  >
                    <v-icon
                        v-text="newCategory.icon || 'mdi-castle'"
                    />
                  </v-layout>
                </v-card>
              </v-layout>
            </v-col>
          </v-row>
          <v-textarea
              v-model="newCategory.description"
              :rules="[() => !!newCategory.description || 'This field is required']"
              label="Description"
              counter="300"
              required
          />          <v-btn
            color="success"
            class="mr-4"
            @click="editCategory"
        >
          Apply
        </v-btn>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "EditCategory",
  data () {
    return {
      newCategory: {},
    }
  },
  props:{
    show: Boolean,
    currentCategory: Object
  },
  beforeMount() {
  },
  watch: {
    show(){
      this.newCategory = this.currentCategory
    }
  },
  methods:{
    editCategory(){
      this.$emit("apply", this.newCategory)
    }
  }
}
</script>

<style scoped>

</style>
