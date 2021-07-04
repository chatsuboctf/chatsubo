<template>
  <span v-if="false" />
</template>

<script>
import backend from "@/backend";

export default {
  name: "Logout",
  beforeCreate() {
    backend.logout(this.$store.getters.getUser).then(() => {
      this.$router.push({name: "login"})
    }).catch((e) => {
      console.log(e)
    }).finally(() => {
      this.$store.dispatch("cleanUser")
      this.$cookies.set("CHATSUBO-SESSION", "")
    })

  }
}
</script>

<style scoped>

</style>
