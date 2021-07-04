<template>
  <v-container fluid v-if="user !== undefined">
    <v-row align="center" class="ma-0 pt-8" justify="center" style="width: 100%; height: 200px">
      <v-col sm="6">
        <v-layout align-center column fill-height justify-center>
          <v-avatar
              color="secondaryLighter"
              rounded
              size="100"
          >
            <v-icon dark size="70" v-text="'mdi-account-circle'"/>
          </v-avatar>
          <div v-text="user.username"/>
          <div class="text-caption" style="color: rgba(255, 255, 255,.7)"
               v-text="$mapScoreToRank(user.score).text"/>
        </v-layout>
      </v-col>
    </v-row>
<!--    <v-row align="center" class="ma-0 pt-8" justify="center" style="width: 100%;height: 200px">-->
<!--      <v-col sm="6" md="3">-->
<!--        <v-card :loading="isLoading">-->
<!--          <v-list-item>-->
<!--            <v-list-item-content>-->
<!--              <div class="overline mb-1">-->
<!--                Score-->
<!--              </div>-->
<!--              <v-list-item-title class="headline mb-1">-->
<!--                {{ user.score }}-->
<!--              </v-list-item-title>-->
<!--            </v-list-item-content>-->

<!--            <v-list-item-avatar-->
<!--                size="70"-->
<!--            >-->
<!--              <v-icon-->
<!--                  size="50"-->
<!--                  v-text="'mdi-podium'"-->
<!--              />-->
<!--            </v-list-item-avatar>-->
<!--          </v-list-item>-->
<!--        </v-card>-->
<!--      </v-col>-->
<!--      <v-col sm="6" md="3">-->
<!--        <v-card :loading="isLoading">-->
<!--          <v-list-item>-->
<!--            <v-list-item-content>-->
<!--              <div class="overline mb-1">-->
<!--                Machines-->
<!--              </div>-->
<!--              <v-list-item-title class="headline mb-1">-->
<!--                {{ user.score }}-->
<!--              </v-list-item-title>-->
<!--            </v-list-item-content>-->

<!--            <v-list-item-avatar-->
<!--                size="70"-->
<!--            >-->
<!--              <v-icon-->
<!--                  size="50"-->
<!--                  v-text="'mdi-webpack'"-->
<!--              />-->
<!--            </v-list-item-avatar>-->
<!--          </v-list-item>-->
<!--        </v-card>-->
<!--      </v-col>-->
<!--      <v-col sm="6" md="3">-->
<!--        <v-card :loading="isLoading">-->
<!--          <v-list-item>-->
<!--            <v-list-item-content>-->
<!--              <div class="overline mb-1">-->
<!--                Achievements-->
<!--              </div>-->
<!--              <v-list-item-title class="headline mb-1">-->
<!--                {{ user.score }}-->
<!--              </v-list-item-title>-->
<!--            </v-list-item-content>-->

<!--            <v-list-item-avatar-->
<!--                size="70"-->
<!--            >-->
<!--              <v-icon-->
<!--                  size="50"-->
<!--                  v-text="'mdi-trophy'"-->
<!--              />-->
<!--            </v-list-item-avatar>-->
<!--          </v-list-item>-->
<!--        </v-card>-->
<!--      </v-col>-->
<!--      <v-col sm="6" md="3">-->
<!--        <v-card :loading="isLoading">-->
<!--          <v-list-item>-->
<!--            <v-list-item-content>-->
<!--              <div class="overline mb-1">-->
<!--                Rank-->
<!--              </div>-->
<!--              <v-list-item-title class="headline mb-1">-->
<!--                {{ $mapScoreToRank(user.score).text }}-->
<!--              </v-list-item-title>-->
<!--            </v-list-item-content>-->

<!--            <v-list-item-avatar-->
<!--                size="70"-->
<!--            >-->
<!--              <v-icon-->
<!--                  size="50"-->
<!--                  v-text="'mdi-account'"-->
<!--              />-->
<!--            </v-list-item-avatar>-->
<!--          </v-list-item>-->
<!--        </v-card>-->
<!--      </v-col>-->
<!--    </v-row>-->
  </v-container>
  <v-container fluid fill-height v-else-if="userNotFound">
      <v-layout fill-height align-center justify-center>
      <div class="headline">
        User not found :'(
      </div>
      </v-layout>
  </v-container>
  <div v-else>
  </div>
</template>

<script>
import backend from "@/backend";

export default {
  name: "Profile",
  data: () => {
    return {
      user: undefined,
      userNotFound: false
    }
  },
  computed:{
    isLoading(){
      return this.user === undefined
    }
  },
  beforeMount(){
    let currentUser = this.$router.currentRoute.params.who
    if (currentUser === this.$store.getters.getUser.username){
      this.user = this.$store.getters.getUser
      return
    }

    backend.getUser(currentUser).then((res) =>{
      if (res.data.errors.length > 0){
        this.$toast.error(`Failed to fetch user data : ${res.data.errors.join(" / ")}`)
        return
      }

      this.user = res.data.user
    }).catch((err)=>{
      if (err.response.status === 404){
        this.userNotFound = true
      // this.$toast.error(`Failed to fetch user data : ${res}`)
      }
    })
  }
}
</script>

<style scoped>

</style>
