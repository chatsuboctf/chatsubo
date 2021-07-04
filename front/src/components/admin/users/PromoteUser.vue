<template>
  <v-row no-gutters>
    <v-col sm="12" md="12">
      <v-card
          color="cardBackground"
          rounded="lg"
          class="px-4"
      >
        <v-card-title
            class="text-h5 pa-0 pb-4 pt-4"
        >
          Administrator status
        </v-card-title>
        <v-row>
          <v-col
            md="12"
            class="pb-0"
          >
            <v-layout
              justify-space-around
              align-center
            >
              <v-btn
                  :color="newState !== null && newState === true ? 'success': null"
                  @click="newState = true"
                  :disabled="newState === null"
                  :outlined="newState === null"
              >
                <v-icon
                    class="mr-1"
                  v-text="'mdi-check'"
                />
                True
              </v-btn>
              <v-btn
                  :color="newState !== null && newState === false ? 'red': null"
                  @click="newState = false"
                  :disabled="newState === null"
                  :outlined="newState === null"
              >
                <v-icon
                    class="mr-1"
                  v-text="'mdi-close'"
                />
                False
              </v-btn>
            </v-layout>
          </v-col>
          <v-col
            md="12"
            class="pt-0"
          >
            <safety-switch
                class="px-0"
                label="Update"
                :disabled="!selectedUser"
                icon="mdi-account-cog"
                color="warning"
                :loading="loader"
                @click="$emit('setAdmin', newState)"
            />
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
  name: "PromoteUser",
  components: {
    SafetySwitch
  },
  props: {
    loader: Boolean,
    selectedUser: null
  },
  data() {
    return {
      newState: null,
      users: {
        entries: [],
        loading: false,
        textLimit: 60
      },
      usersSearch: null,
    }
  },
  methods: {
    genNewpass() {
      this.newPass = this.$randStr(this.newPassLen)
    },
    log(el) {
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
  watch:{
    selectedUser(newUser){
      console.log(newUser)
      if (newUser){
        this.newState = newUser.admin
        console.log(this.newState)
      }else{
        this.newState = null
      }
    }
  }
}

</script>

<style scoped>

</style>
