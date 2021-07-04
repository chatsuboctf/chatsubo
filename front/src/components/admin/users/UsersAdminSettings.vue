<template>
  <v-row>
    <v-col sm="12" md="4">
      <v-row style="flex-direction: column">
        <v-col sm="12">
          <v-autocomplete
              v-model="selectedUserID"
              :items="availableUsers"
              :loading="users.loading"
              :rules="[() => !!selectedUser || 'This field is required']"
              placeholder="Search user"
              :search-input.sync="usersSearch"
              outlined
              item-value="id"
              item-text="username"
              cache-items
              hide-details
              label="User"
              required
          />
        </v-col>
        <v-col sm="12">
          <promote-user
              @setAdmin="setAdmin"
              :loader="setAdminLoader"
              :selected-user.sync="selectedUser"
          />
        </v-col>
      </v-row>
    </v-col>
    <v-col sm="12" md="8">
      <reset-user-pass
          @resetUser="resetUserPassword"
          :loader="resetUserLoader"
          :selected-user.sync="selectedUser"
      />
    </v-col>
    <v-row>
      <v-col>

      </v-col>
    </v-row>
  </v-row>
</template>

<script>
import ResetUserPass from "@/components/admin/users/ResetUserPass";
import PromoteUser from "@/components/admin/users/PromoteUser";
import backend from "@/backend";

export default {
  components:{
    ResetUserPass,
    PromoteUser
  },
  name: "UserAdminSettings",
  data () {
    return {
      users: {
        entries: [],
        loading: false,
        textLimit: 60
      },
      usersSearch: null,
      selectedUserID: null,
      selectedUser: null,
      resetUserLoader: false,
      setAdminLoader: false,
      enableCalendars: false,
      showMenuOpenStart: false,
      showMenuOpenEnd: false,
      showBottomSaveSnackbar: false,
      saveCurrentSettingsLoader: false,
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
    setAdmin(newState){
      let data = {"userID": this.selectedUserID, "state": newState}

      backend.setAdmin(data)
          .then(() => {
            this.$toast.success('Admin status updated')
          }).catch((err) => {
        this.$toast.error(err.response.data.errors.join(" / "))
      }).finally(() => {
        this.resetUserLoader = false
      })
    },
    resetUserPassword(newPass){
      this.setAdminLoader = true
      let data = {
        "userID": this.selectedUserID,
        "newPass": newPass
      }

      backend.resetUserPassword(data)
          .then(() => {
            this.$toast.success('Password has been reset')
          }).catch(() => {
        this.$toast.error(`Failed to reset password`, {duration: 10000})
      }).finally(() => {
        this.setAdminLoader = false
      })
    },
  },
  watch: {
    selectedUserID(newSelectedUserID){
      console.log(this.users.entries.find(user => user.id === newSelectedUserID))
      this.selectedUser = this.users.entries.find(user => user.id === newSelectedUserID)
    },
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
