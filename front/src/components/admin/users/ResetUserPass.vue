<template>
  <v-row no-gutters>
    <v-col sm="12">
      <v-card
          color="cardBackground"
          rounded="lg"
          class="px-4"
      >
        <v-card-title
            class="text-h5 pa-0 pb-4 pt-4"
        >
          Password reset
        </v-card-title>
        <v-row>
          <v-col
              md="6"
              lg="4"
          >
<!--            <v-autocomplete-->
<!--                v-model="selectedUserID"-->
<!--                :items="availableUsers"-->
<!--                :loading="users.loading"-->
<!--                :rules="[() => !!selectedUserID || 'This field is required']"-->
<!--                placeholder="Search user"-->
<!--                :search-input.sync="usersSearch"-->
<!--                outlined-->
<!--                item-value="id"-->
<!--                item-text="username"-->
<!--                cache-items-->
<!--                hide-details-->
<!--                label="User"-->
<!--                required-->
<!--            />-->
            <safety-switch
                class="px-0"
                label="Reset"
                :disabled="!selectedUser"
                icon="mdi-refresh"
                color="warning"
                :loading="loader"
                @click="$emit('resetUser', newPass)"
            />
          </v-col>
          <v-col
              md="6"
              lg="8"
          >
            <v-row>
              <v-col cols="12" class="pb-0">
                <v-text-field
                    v-model="newPass"
                    label="New password"
                    :rules="[() => !!newPass || 'This field is required']"
                    required
                    append-icon="mdi-refresh"
                    @click:append="genNewpass"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-slider
                    v-model="newPassLen"
                    :max="40"
                    :min="1"
                    ticks
                    color="accent"
                    label="Password length"
                    class="align-center"
                >
                  <template v-slot:append>
                    <v-text-field
                        v-model="newPassLen"
                        class="mt-0 pt-0"
                        type="number"
                    />
                  </template>
                </v-slider>
              </v-col>
              <!--              <v-col class="pb-0" cols="1">-->
              <!--                <v-layout-->
              <!--                    align-center-->
              <!--                    column-->
              <!--                    fill-height-->
              <!--                    justify-center-->
              <!--                >-->
              <!--                  <v-btn-->
              <!--                      :loading="genLoader"-->
              <!--                      icon-->
              <!--                      @click="genNewpass"-->
              <!--                  >-->
              <!--                    <v-icon-->
              <!--                        v-text="'mdi-refresh'"-->
              <!--                    />-->
              <!--                  </v-btn>-->
              <!--                </v-layout>-->
              <!--              </v-col>-->
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import backend from "@/backend";
import SafetySwitch from "@/components/interactive/SafetySwitch";

export default {
  name: "ResetUserPass",
  components:{
    SafetySwitch
  },
  props: {
    selectedUser: null,
    loader: Boolean
  },
  data() {
    return {
      newPass: this.$randStr(8),
      genLoader: false,
      newPassLen: 8,
      users: {
        entries: [],
        loading: false,
        textLimit: 60
      },
      usersSearch: null,
    }
  },
  computed: {
    areUsersLoaded() {
      return this.users.length > 0
    },
    availableUsers() {
      return this.users.entries.map(entry => {
        const username = entry.username.length > this.users.textLimit
            ? entry.username.slice(0, this.users.textLimit) + '...'
            : entry.username

        return Object.assign({}, entry, {username})
      })
    },
  },
  methods: {
    genNewpass(){
      this.newPass = this.$randStr(this.newPassLen)
    },
    log(el){
      console.log(el)
    },
    loadUsers() {
      this.users.loading = true

      backend.listUsers().then((res) => {
        this.users.entries = res.users
      }).catch(() => {
        this.$toast.error(`Failed to fetch users`, {duration: 10000})
      }).finally(() => {
        this.users.loading = false
      })
    },
  },
  watch: {
    usersSearch() {
      // Items have already been loaded
      if (this.areUsersLoaded) return

      // Items have already been requested
      if (this.users.loading) return

      this.loadUsers()
    },
  }
}
</script>

<style scoped>

</style>
