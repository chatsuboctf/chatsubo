<template>
  <v-container class="pt-6">
    <div v-if="!boxNotFound && !isLoading">
      <v-container fluid>
        <v-row>
          <v-layout>
            <v-col md="12" sm="12">
              <v-card
                  color="secondary"
              >
                <v-row >
                  <v-col sm="12" lg="4">
                    <v-card
                        elevation="4"
                        style="position: absolute; left: 10px; top: -15px"
                        color="secondaryLighter"
                    >
                      <box-card
                          :box="boxData"
                          with-stats
                          :animate-hover="false"
                          flat
                          color="secondaryLighter"
                      />
                    </v-card>
                    <v-container style="height: 105px" />
                  </v-col>
                  <v-spacer/>
                  <v-col sm="12" lg="7">
                    <v-row>
                      <v-col sm="12" md="12">
                        <detail-card
                            flat
                            color="secondary"
                            title="Address"
                        >
                          <template slot="text">
                            <v-tooltip transition="slide-fade-transition" bottom>
                              <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                    :loading="boxAddressLoading"
                                    v-clipboard:copy="boxAddress || 'N/A'"
                                    v-clipboard:success="onClipboardCopy"
                                    v-clipboard:error="onClipboardError"
                                    text
                                    :color="isCopied ? 'green' : undefined"
                                    style="transition: .3s ease-in-out"
                                    class="headline"
                                    v-bind="attrs"
                                    v-on="on"
                                >
                                  <v-layout
                                      justify-center
                                      fill-height
                                      align-center
                                  >
                                    {{boxAddress || 'N/A'}}
                                    <v-icon
                                        class="pl-2"
                                        size="20"
                                        v-text="'mdi-clipboard'"
                                    />
                                  </v-layout>
                                </v-btn>
                              </template>
                              Copy
                            </v-tooltip>
                          </template>
                        </detail-card>
                      </v-col>
                      <!--                      <v-col sm="12" md="6">-->
                      <!--                        <v-layout-->
                      <!--                            justify-center-->
                      <!--                            align-center-->
                      <!--                        >-->
                      <!--                          <v-card-->
                      <!--                              class="pr-2 pt-0"-->
                      <!--                              flat-->
                      <!--                              max-width="400"-->
                      <!--                          >-->
                      <!--                            <v-card-text-->
                      <!--                                class="pa-0"-->
                      <!--                            >-->
                      <!--                              <v-layout-->
                      <!--                                  justify-space-around-->
                      <!--                                  align-center-->
                      <!--                              >-->
                      <!--                                <safety-switch-->
                      <!--                                    label="Reset"-->
                      <!--                                    :loading.sync="loaders.resetBox"-->
                      <!--                                    color="warning"-->
                      <!--                                    @click="askReset"-->
                      <!--                                    icon="mdi-refresh"-->
                      <!--                                />-->
                      <!--                              </v-layout>-->
                      <!--                            </v-card-text>-->
                      <!--                          </v-card>-->
                      <!--                        </v-layout>-->
                      <!--                      </v-col>-->
                    </v-row>
                  </v-col>
                </v-row>
                <!--                    style="padding-top: 105px"-->
                <v-card-text
                    v-if="isBoxDynamic"
                >
                  <v-layout
                      justify-start
                  >
                    <v-icon
                        small
                        class="pr-2"
                        v-text="'mdi-clock'"
                    />
                    <span
                        v-text="!queueState.state ? 'Duration' : 'Time left'"
                        style="color: white !important;"
                        class="overline"
                    />
                  </v-layout>
                  <v-layout
                      justify-start
                      align-center
                      fluid
                      class="pb-2"
                  >
                    <v-layout
                        align-center
                        style="font-weight: bold; font-size: 24px"
                    >
                      <span
                          v-if="!queueState.state"
                          style="color: rgba(255, 255, 255, .9) !important;"
                          class="mr-3"
                          v-text="`${boxData.duration} minutes`"
                      />
                      <span
                          v-else-if="queueState.state !== 'running'"
                          class="mr-3"
                          v-text="startStopButtonLegend"
                      />
                      <span
                          v-else
                          class="mr-3"
                          v-text="timeLeft.fmt"
                      />
                      <div>
                        <v-btn
                            :color="queueState.state !== 'running' ? 'green' : 'red'"
                            :outlined="queueState.state === 'running'"
                            :loading="loaders.startStopBox"
                            class="px-2 pl-1"
                            @click="startStopBox"
                        >
                          <!--                          <template v-slot:loader>-->
                          <!--                            <div>-->
                          <!--                              {{startStopButtonLegend}}-->
                          <!--                                  <v-progress-circular-->
                          <!--                                      indeterminate-->
                          <!--                                      size="20"-->
                          <!--                                      width="2"-->
                          <!--                                      color="white"-->
                          <!--                                  />-->
                          <!--                            </div>-->
                          <!--                          </template>-->

                          <span
                              v-show="!loaders.startStopBox"
                          >
                          <v-icon
                              v-text="queueState.state === '' ? 'mdi-play' : 'mdi-stop'"
                              class="mr-1"
                          />
                          {{queueState.state === '' ? "Start" : "Stop"}}
                          </span>

                        </v-btn>
                        <!--                        <span-->
                        <!--                            class="ml-1 overline"-->
                        <!--                        >-->
                        <!--                          {{startStopButtonLegend}}-->
                        <!--                        </span>-->

                        <!--                        <v-btn-->
                        <!--                            v-else-->
                        <!--                            color="red"-->
                        <!--                            class="px-2 pl-1"-->
                        <!--                            outlined-->
                        <!--                            :loading="loaders.stopBox"-->
                        <!--                            @click="stopBox"-->
                        <!--                        >-->
                        <!--                          <v-icon-->
                        <!--                              v-text="'mdi-stop'"-->
                        <!--                              class="mr-1"-->
                        <!--                          />-->
                        <!--                          Stop-->
                        <!--                        </v-btn>-->
                      </div>
                    </v-layout>
                  </v-layout>
                </v-card-text>

                <v-card-text
                    class="pt-4"
                >
                  <v-layout
                      justify-start
                  >
                    <v-icon
                        small
                        class="pr-2"
                        v-text="'mdi-card-text'"
                    />
                    <span
                        style="color: white !important;"
                        class="overline"
                    >
                        Description
                      </span>
                  </v-layout>
                  <pre style="white-space: pre-wrap" v-text="boxData.description" />
                </v-card-text>
                <v-row>
                  <v-col
                      sm="12"
                      md="6"
                  >
                    <v-card
                        flat
                        color="secondary"
                        class="pb-0"
                    >
                      <v-card-title
                          class="overline mb-0 pb-0"
                      >
                        <v-layout
                            style="width: 100%"
                            justify-start
                        >
                          <v-icon
                              small
                              class="pr-2"
                              v-text="'mdi-flag'"
                          />
                          <span class="overline">
                            Flags
                      </span>
                        </v-layout>

                      </v-card-title>
                      <v-card-text>
                        <v-layout
                            align-center
                            column
                            fluid
                        >
                          <v-card
                              style="width: 100%;"
                              class="mb-6"
                              color="secondary"
                              flat
                          >
                            <v-card-text
                                class="pa-0"
                            >
                              <v-layout
                                  align-center
                                  justify-center
                              >
                                <v-text-field
                                    color="accent"
                                    hide-details
                                    :disabled="isFlagInputDisabled"
                                    v-model="flagValue"
                                    label="Flag"
                                    placeholder="flag{...}"
                                    @keyup.enter.native="checkFlag"
                                >
                                  <template slot="append-outer">
                                    <v-btn
                                        block
                                        color="accent"
                                        :outlined="isFlagInputDisabled"
                                        :disabled="isFlagInputDisabled"
                                        @click="checkFlag"
                                    >
                                      <v-icon
                                          v-text="'mdi-check-all'"
                                          class="mr-1"
                                      />
                                      Check flag
                                    </v-btn>

                                  </template>
                                </v-text-field>
                              </v-layout>
                            </v-card-text>
                          </v-card>
                          <v-row
                              dense
                              class="flex-wrap"
                              style="width: 100%;"
                          >
                            <v-col
                                md="6"
                                v-for="(flag, idx) in boxData.flags"
                                :key="idx"
                            >
                              <v-sheet
                                  rounded
                              >
                                <v-card
                                    :color="flagCardColor(flag)"
                                    :outlined="!isFlagged(flag)"
                                    class="dashed-card"
                                    :style="!isFlagged(flag) ? 'border-color: grey !important;' : ''"
                                >
                                  <!--                style="border: 1px solid rgba(255,255,255,.4)"-->
                                  <v-card-title
                                      class="overline mb-1"
                                  >
                                    <v-layout
                                        column
                                        fill-height
                                        justify-center
                                        align-center
                                    >
                                      <div>
                                        <v-icon small v-text="flag.icon" />
                                        {{flag.name}} ({{flag.points}})
                                      </div>
                                    </v-layout>
                                  </v-card-title>
                                </v-card>
                              </v-sheet>
                            </v-col>
                          </v-row>
                        </v-layout>
                      </v-card-text>
                    </v-card>
                    <v-row
                        class="pb-0"
                    >
                      <v-col>
                        <v-card
                            flat
                            color="secondary"
                        >
                          <v-card-title
                              class="overline mb-0 pb-0"
                          >
                            <v-layout
                                style="width: 100%"
                                justify-start
                            >
                              <v-icon
                                  small
                                  class="pr-2"
                                  v-text="'mdi-coffee-maker'"
                              />
                              <span
                                  class="overline"
                                  v-text="boxData.authors.length > 1 ? 'Authors' : 'Author'"
                              />
                            </v-layout>
                          </v-card-title>
                          <v-card-text
                              class="pb-1"
                          >
                            <v-chip-group
                                column
                            >
                              <v-chip
                                  label
                                  color="secondaryLighter"
                                  :ripple="false"
                                  v-for="author in boxData.authors"
                                  :key="author.name"
                              >
                                <v-avatar left>
                                  <img
                                      :src="author.avatar"
                                      :alt="`${author.name} avatar`"
                                  />
                                </v-avatar>
                                {{author.name}}
                              </v-chip>
                            </v-chip-group>
                          </v-card-text>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-col>
                  <v-col sm="12" md="6">
                    <detail-card
                        color="secondary"
                        extended
                        class="pt-1"
                        no-icon
                        flat
                    >
                      <template slot="title">
                        <v-layout
                            style="width: 100%"
                            justify-start
                        >
                          <v-icon
                              small
                              class="pr-2"
                              v-text="'mdi-map'"
                          />
                          <span class="overline">
                        Realm
                      </span>
                        </v-layout>
                      </template>
                      <template slot="text">
                        <v-row
                            dense
                            class="py-2"
                            style="width: 100%"
                            align="center"
                            justify="space-between"
                        >
                          <v-col sm="12" lg="9">
                            <v-select
                                item-color="accent"
                                hide-details
                                color="accent"
                                outlined
                                dense
                                v-model="currentRealm"
                                :items="availableRealms"
                            />
                          </v-col>
                          <v-col sm="12" lg="3">
                            <v-btn
                                block
                                @click="downloadVPN"
                                color="accent"
                            >
                              <v-icon
                                  v-text="'mdi-download'"
                                  class="pr-1"
                              />
                              VPN
                            </v-btn>
                          </v-col>
                        </v-row>

                      </template>
                    </detail-card>
                    <span
                        v-if="sessionCreds && sessionCreds.length > 0"
                    >
                    <detail-card
                        color="secondary"
                        extended
                        class="pt-1"
                        no-icon
                        flat
                        v-for="(access, idx) in sessionCreds"
                        :key="idx"
                    >
                      <template slot="title">
                        <v-layout
                            style="width: 100%"
                            justify-start
                            class="pb-2"
                        >
                          <v-icon
                              small
                              class="pr-2"
                              v-text="'mdi-key-chain-variant'"
                          />
                          <span class="overline">
                            Access ({{access.type}})
                           </span>
                        </v-layout>
                      </template>
                      <template slot="text">
                        <v-layout
                            justify-center
                            align-start
                            style="width: 100%"
                            column
                        >
                          <v-row
                              dense
                              style="width: 100%"
                              align="center"
                              justify="center"
                              class="pb-4"
                          >
                            <v-col sm="12" lg="9">
                              <v-text-field
                                  outlined
                                  prepend-inner-icon="mdi-account"
                                  hide-details
                                  v-model="access.username"
                                  label="Username"
                                  readonly
                                  dense
                              >
                              </v-text-field>
                            </v-col>
                            <v-col sm="12" lg="3">
                              <v-btn
                                  block
                                  v-clipboard:copy="access.username"
                                  v-clipboard:success="() => $toast.success('Copied to clipboard')"
                                  v-clipboard:error="(e) => $toast.error(e.text)"
                                  text
                              >
                                <v-icon
                                    small
                                    v-text="'mdi-clipboard'"
                                    class="mr-1"
                                />
                                Copy
                              </v-btn>
                            </v-col>
                          </v-row>
                          <v-row
                              dense
                              style="width: 100%"
                              align="center"
                              justify="center"
                              class="pb-4"
                          >
                            <v-col sm="12" lg="9">
                              <v-text-field
                                  outlined
                                  prepend-inner-icon="mdi-lock"
                                  v-model="access.password"
                                  label="Password"
                                  hide-details
                                  :append-icon="showPass ? 'mdi-eye-outline' : 'mdi-eye-off-outline'"
                                  @click:append="() => (showPass = !showPass)"
                                  :type="showPass ? 'text' : 'password'"
                                  dense
                                  readonly
                              >
                              </v-text-field>
                            </v-col>
                            <v-col sm="12" lg="3">
                              <v-btn
                                  block
                                  v-clipboard:copy="access.password"
                                  v-clipboard:success="() => $toast.success('Copied to clipboard')"
                                  v-clipboard:error="(e) => $toast.error(e.text)"
                                  text
                              >
                                <v-icon
                                    small
                                    v-text="'mdi-clipboard'"
                                    class="mr-1"
                                />
                                Copy
                              </v-btn>
                            </v-col>
                          </v-row>
                          <v-row>
                            <v-col>
                              <v-btn
                                  v-clipboard:copy="`ssh ${access.username}@${boxAddress} -o PreferredAuthentications=password`"
                                  v-clipboard:success="() => $toast.success('Copied to clipboard')"
                                  v-clipboard:error="(e) => $toast.error(e.text)"
                                  text
                                  v-if="access.type.toLowerCase() === 'ssh'"
                              >
                                <v-icon
                                    small
                                    v-text="'mdi-clipboard'"
                                    class="mr-1"
                                />
                                <span
                                    style="display: inline-block; max-width: 275px"
                                    class="text-truncate"
                                >
                                ssh {{access.username}}@{{boxAddress}}
                                </span>
                              </v-btn>
                            </v-col>
                          </v-row>

                          <span
                              class="overline"
                          >

                          </span>

                        </v-layout>
                      </template>
                    </detail-card>
                    </span>
                    <span
                        v-else
                    >
                      <detail-card
                          color="secondary"
                          extended
                          class="pt-1"
                          no-icon
                          flat
                      >
                      <template slot="title">
                        <v-layout
                            style="width: 100%"
                            justify-start
                            class="pb-2"
                        >
                          <v-icon
                              small
                              class="pr-2"
                              v-text="'mdi-key-chain-variant'"
                          />
                          <span class="overline">
                            Access
                           </span>
                        </v-layout>
                      </template>
                      <template slot="text">
                        <v-layout
                            justify-center
                            align-start
                            style="width: 100%"
                            column
                        >
                          <v-row
                              dense
                              style="width: 100%"
                              align="center"
                              justify="center"
                              class="pb-4"
                          >
                            <v-col sm="12" lg="9">
                              <v-text-field
                                  outlined
                                  prepend-inner-icon="mdi-account"
                                  hide-details
                                  disabled
                                  label="Username"
                                  readonly
                                  dense
                              >
                              </v-text-field>
                            </v-col>
                            <v-col sm="12" lg="3">
                              <v-btn
                                  block
                                  disabled
                                  text
                              >
                                <v-icon
                                    small
                                    v-text="'mdi-clipboard'"
                                    class="mr-1"
                                />
                                Copy
                              </v-btn>
                            </v-col>
                          </v-row>
                          <v-row
                              dense
                              style="width: 100%"
                              align="center"
                              justify="center"
                              class="pb-4"
                          >
                            <v-col sm="12" lg="9">
                              <v-text-field
                                  outlined
                                  prepend-inner-icon="mdi-lock"
                                  disabled
                                  label="Password"
                                  hide-details
                                  type="password"
                                  dense
                                  readonly
                              >
                              </v-text-field>
                            </v-col>
                            <v-col sm="12" lg="3">
                              <v-btn
                                  disabled
                                  block
                                  text
                              >
                                <v-icon
                                    small
                                    v-text="'mdi-clipboard'"
                                    class="mr-1"
                                />
                                Copy
                              </v-btn>
                            </v-col>
                          </v-row>
                        </v-layout>
                      </template>
                    </detail-card>
                    </span>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-layout>
        </v-row>
      </v-container>
      <v-container fluid>
        <check-flag-loading
            :show="showFlagModal"
            :success.sync="checkFlagSuccess"
            :duration="checkFlagDuration"
            @close="closeCheckFlagLoading"
        >
          <template slot="success">
            <div
                style="color: rgba(255,255,255,.9)"
                class="headline"
            >
              <v-icon v-text="'mdi-check-circle-outline'" />
              Valid
            </div>
          </template>
          <template slot="failure">
            <div
                style="color: rgba(255,255,255,.9)"
                class="headline"
            >
              <v-icon v-text="'mdi-close-circle-outline'" />
              Invalid
            </div>
          </template>
        </check-flag-loading>
      </v-container>
    </div>
    <v-layout
        v-else-if="!isLoading && boxNotFound"
        fill-height
        align-center
        justify-center
        column
        style="height: 40vh; color: rgba(255,255,255,.7)"
    >
      <div
          class="mb-4"
      >
        <v-icon
            size="80"
            color="rgba(255,255,255,.85)"
            v-text="'mdi-package-variant'"
        />
      </div>
      <span class="overline" style="font-size: 20px !important">
          Box not found
        </span>
    </v-layout>
    <v-layout
        v-else-if="isLoading"
        fill-height
        align-center
        justify-center
        column
        style="height: 40vh; color: rgba(255,255,255,.7)"
    >
      <div
          class="mb-4"
      >
        <v-progress-circular
            indeterminate
        />
      </div>
    </v-layout>

  </v-container>
</template>

<script>
import backend from "@/backend";
import CheckFlagLoading from "@/components/modals/CheckFlagLoading";
import DetailCard from "@/components/boxes/DetailCard";
import BoxCard from "@/components/boxes/BoxCard";
import {defaults} from "../lib/defaults";
// import SafetySwitch from "@/components/interactive/SafetySwitch";

export default {
  name: "BoxProfile",
  components: {
    CheckFlagLoading,
    DetailCard,
    BoxCard,
    // SafetySwitch
  },
  data: () => {
    return {
      submissions: [],
      submissionsLoading: false,
      queueState: JSON.parse(JSON.stringify(defaults.queueState)),
      sessionStateLoopID: null,
      showPass: false,
      flagValue: "",
      isCopied: false,
      showFlagModal: false,
      checkFlagSuccess: undefined,
      checkFlagDuration: 5000,
      box: null,
      timeLeft:{
        tickID: null,
        delta: 0,
        fmt: "",
      },
      boxAddress: null,
      sessionCreds: null,
      boxSession: null,
      boxNotFound: false,
      realms: undefined,
      boxAddressLoading: false,
      safeties: {
        reset: false
      },
      loaders: {
        resetBox: false,
        startStopBox: false,
      }
    }
  },
  methods: {
    loadSubmissionsForCurrentUser(){
      this.submissionsLoading = true

      backend.listSubmissionsForCurrentUser(this.$store.getters.getUser.id).then((res) => {
        if (res.data.data === undefined){
          this.submissions = []
        }else{
          this.submissions = res.data.data
        }
      }).catch(() => {
        this.$toast.error(`Failed to fetch submissions for current user`, { duration: 10000 })
      }).finally(() => {
        this.submissionsLoading = false
      })
    },
    startQueueStatePolling(taskID){
      this.updateQueueState(taskID)
      this.queueState.tickID = setInterval(() => {
        this.updateQueueState(taskID)
      }, 5000)
    },
    isFlagged(flag){
      for (const sub of this.submissions) {
        if (sub.flag_id === flag.id && sub.valid){
          return true
        }
      }

      return false
      // return this.$store.getters.getUser.flags.map(f => f.id).includes(flag.id)
    },
    startStopBox(){
      if (this.boxSession === null){
        this.startBox()
      }else{
        this.stopBox()
      }
    },
    updateQueueState(taskID){
      backend.fetchQueueState(taskID).then((res) =>{
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to start box : ${res.data.errors.join(" / ")}`)
          return
        }

        this.queueState.state = res.data.data.state
      }).catch((res)=>{
        if (res.response.status === 404){
          // this.$toast.error(`Session not found`)
          this.clearBuilding()
          return
        }

        this.$toast.error(`Failed to start box : ${res.data.errors.join(" / ")}`)
      })
    },
    startBox(){
      this.boxAddress = null

      const data = {
        realm: this.currentRealm,
        box: this.boxData,
        user: this.$store.getters.getUser
      }

      this.loaders.startStopBox = true
      backend.startBox(data).then((res) =>{
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to start box : ${res.data.errors.join(" / ")}`)
          this.clearBuilding()
          return
        }

        this.startQueueStatePolling(res.data.data.taskID)

        this.updateFormatedTimeLeft()
        this.timeLeft.tickID = setInterval(() => {
          this.updateFormatedTimeLeft()
        }, 1000)

        this.queueState.state = "pending"
      }).catch((res)=>{
        this.$toast.error(`Failed to start box : ${res.response.data.errors}`)
        this.clearBuilding()
      }).finally(() => {
        // this.loaders.startStopBox = false
      })
    },
    stopBox(){
      this.boxAddress = null
      this.queueState = JSON.parse(JSON.stringify(defaults.queueState))
      clearTimeout(this.timeLeft.tickID)
      this.timeLeft.tickID = null

      const data = {
        realm: this.currentRealm,
        session: this.boxSession,
        user: this.$store.getters.getUser
      }

      this.loaders.startStopBox = true
      backend.stopBox(data).then((res) =>{
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to stop box : ${res.data.errors.join(" / ")}`)
          return
        }

        this.loadBoxSessions()
      }).catch((res)=>{
        this.$toast.error(`Failed to stop box : ${res.response.data.errors}`)
      }).finally(() => {
        this.loaders.startStopBox = false
      })
    },
    askReset(){
      const data = {
        realm: this.currentRealm,
        box: this.boxData,
        user: this.$store.getters.getUser,
        session: this.boxSession,
      }

      this.loaders.resetBox = true
      backend.askReset(data).then((res) =>{
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to ask for reset : ${res.data.errors.join(" / ")}`)
        }
      }).catch((res)=>{
        this.$toast.error(`Failed to ask for reset : ${res.response.data.errors}`)
      }).finally(() => {
        this.safeties.reset = false
        this.loaders.resetBox = false
      })
    },
    reloadUser(){
      let email = this.$store.getters.getUser.email

      backend.getUser(this.$store.getters.getUser.username).then((res) =>{
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to fetch user data : ${res.data.errors.join(" / ")}`)
          return
        }

        res.data.user.email = email
        this.$store.commit("setUser", res.data.user)
      }).catch((err)=>{
        if (err.response.status === 404){
          this.userNotFound = true
          // this.$toast.error(`Failed to fetch user data : ${res}`)
        }
      })
    },
    closeCheckFlagLoading(){
      this.showFlagModal = false
      setTimeout(() => {
        this.checkFlagSuccess = undefined
      }, 500)
    },
    checkFlag(){
      if (this.flagValue.length === 0){
        this.$toast.info("Missing flag")
        return
      }

      const data = {
        flag: this.flagValue,
        user: this.$store.getters.getUser,
        realm: this.currentRealm,
        box_id: this.boxData.id,
      }

      this.showFlagModal = true

      backend.checkFlag(data).then((res) => {
        if (res.data.data.success) {
          this.reloadUser()
          this.loadBox()
          this.checkFlagSuccess = true
          return
        }

        this.checkFlagSuccess = false
      }).catch((res) => {
        if ([400, 404].includes(res.response.status)){
          this.$toast.info(res.response.data.errors.join(" / "))
        }else if (res.response.status === 403){
          this.$toast.info("Submissions have been frozen")
          this.showFlagModal = false
          return
        }else if (res.response.status === 409){
          this.$toast.info("This flag has already been validated")
          this.showFlagModal = false
          return
        }

        this.checkFlagSuccess = false
      })
    },
    onClipboardCopy: function () {
      this.$toast.success('Copied to clipboard')
      this.isCopied = true
      setTimeout(() => {
        this.isCopied = false
      }, 200)
    },
    onClipboardError: function (e) {
      this.$toast.error(e.text)
    },
    downloadVPN() {
      const data = {
        "realm": this.currentRealm,
        "username": this.$store.getters.getUser.username
      }
      backend.getVPNAccessFor(data).then((res) => {
        if (res.data.errors.length > 0){
          this.$toast.error(`Failed to fetch realms data : ${res.data.errors}`)
          return
        }

        let filename = `chatsubo-${this.currentRealm}.conf`

        let blob = new Blob([res.data.config], { type: 'application/text' })
        if (window.navigator.msSaveOrOpenBlob) {
          window.navigator.msSaveBlob(blob, filename)
        } else {
          let elem = window.document.createElement('a')
          elem.href = window.URL.createObjectURL(blob)
          elem.download = filename
          document.body.appendChild(elem)
          elem.click()
          document.body.removeChild(elem)
        }
        console.log(res.data)
      }).catch((res) => {
        if (res.response.status === 404){
          this.$toast.error(`Failed to fetch realms data : ${res.response.data.errors}`)
          return
        }

        this.$toast.error(`Failed to fetch realms data : ${res.response.errors}`)

      })
    },
    loadBox(){
      let currentBox = this.$router.currentRoute.params.box

      backend.getBox(currentBox).then((res) => {
        if (res.data.errors.length > 0) {
          this.$toast.error(`Failed to fetch box data : ${res.data.errors.join(" / ")}`)
          return
        }

        this.box = res.data.boxes[0]
        this.loadRealms()

      }).catch((res) => {
        if (res.response.status === 404) {
          this.boxNotFound = true

          // this.$toast.error(`Failed to fetch box data : ${res}`)
        }
      })
    },
    loadBoxSessions(){
      this.boxSessionsLoading = true
      this.boxAddress = null
      this.sessionCreds = null

      let data = {
        realm: this.currentRealm,
        boxName: this.$router.currentRoute.params.box,
        user: this.$store.getters.getUser
      }

      backend.getBoxSession(data).then((res) => {
        if (res.data.errors.length > 0) {
          this.$toast.error(`Failed to fetch box session : ${res.data.errors.join(" / ")}`)
          return
        }

        this.boxSession = res.data.data.session
        this.boxAddress = res.data.data.session.address
        this.sessionCreds = res.data.data.session.creds
      }).catch((res) => {
        if (res.response && res.response.status === 404) {
          this.boxNotFound = true
          this.$toast.error(`Failed to fetch box session : ${res.response.data.errors.join(" / ")}`)
        }

        this.boxSession = null
      }).finally(() => {
        this.boxSessionsLoading = false
      })
    },
    loadBoxAccess(){
      this.boxAddressLoading = true
      let data = {
        realm: this.currentRealm,
        boxName: this.$router.currentRoute.params.box,
      }

      backend.getBoxAccess(data).then((res) => {
        if (res.data.errors.length > 0) {
          this.$toast.error(`Failed to fetch box address : ${res.data.errors.join(" / ")}`)
          return
        }

        this.boxAddress = res.data.data.address.address
        this.sessionCreds = res.data.data.creds
      }).catch((res) => {
        if (res.response && res.response.status === 404) {
          this.boxNotFound = true
        }

        this.$toast.error(`Failed to fetch box address : ${res.response.data.errors.join(" / ")}`)
        this.boxAddress = null
      }).finally(() => {
        this.boxAddressLoading = false
      })
    },
    loadRealms(){
      backend.getRealmsFor(this.$router.currentRoute.params.box).then((res) => {
        if (res.data.errors.length > 0) {
          this.$toast.error(`Failed to fetch realms data : ${res.data.errors.join(" / ")}`)
          return
        }

        this.realms = res.data.realms
      }).catch((res) => {
        if (res.response.status === 500){
          this.$toast.error(`Failed to fetch realms data`)
          return
        }
        this.$toast.error(`Failed to fetch realms data : ${res.data.errors.join(" / ")}`)
      })
    },
    flagCardColor(flag){
      let color = "secondary"
      if (flag.deleted){
        color = "grey"
      }else if (this.isFlagged(flag)){
        color = "success"
      }

      return color
    },
    resetTimer(){
      clearTimeout(this.timeLeft.tickID)
      this.timeLeft.tickID = null
    },
    updateFormatedTimeLeft(){
      // if (this.queueState.state !== "running"){
      //   console.log("called")
      //   this.timeLeft.fmt = this.startStopButtonLegend
      //   return
      // }
      //
      if (!this.boxSession){
        this.resetTimer()
        return
      }

      const secondsSinceStarted = (Date.now() - new Date(this.boxSession.started_at)) / 1000
      const boxDurationInSeconds = this.box.duration * 60
      const delta = boxDurationInSeconds - secondsSinceStarted
      const minutes = parseInt(delta / 60, 10)
      const seconds = parseInt(delta % 60, 10)

      this.timeLeft.fmt = `${minutes}m ${seconds.toString().padStart(2, '0')}s`

      if (delta < 1){
        this.clearBuilding()
      }
    },
    clearBuilding(){
      this.resetTimer()
      this.loadBoxSessions()
      this.queueState.state = ""
      clearInterval(this.queueState.tickID)
      this.queueState.tickID = null
    }
  },
  computed: {
    isFlagInputDisabled(){
      if (this.$store.getters.getSettings.freeze_scoreboard){
        return true
      }

      if (this.isBoxDynamic){
        return this.queueState.state !== 'running'
      }

      return false
    },
    startStopButtonLegend(){
      switch (this.queueState.state){
        case "pending":
          return `Queued... (${this.queueState.position}/${this.queueState.queueLen})`
        case "started":
          return "Building..."
        default:
          return "Pending..."
      }
    },
    isBoxDynamic(){
      if (this.box === undefined){
        return false
      }

      return this.box.kind === "dynamic"
    },
    currentRealm: {
      get: function () {
        let realm

        if (this.availableRealms.includes(this.$store.getters.getRealm)){
          realm = this.$store.getters.getRealm
        }else{
          realm = this.availableRealms.length > 0 ? this.availableRealms[0] : null
        }

        this.$store.commit('setRealm', realm)
        return realm
      },
      set: function (realm) {
        this.$store.commit('setRealm', realm)
      }
    },
    isLoading() {
      return this.box === null && this.availableRealms.length === 0
    },
    isBoxAccessLoading() {
      return this.boxAddress === null && this.availableRealms.length === 0
    },
    availableRealms(){
      if (this.realms === undefined || this.realms === null){
        return []
      }

      return this.realms
    },
    boxData() {
      if (this.box === null || this.box === undefined) {
        return {}
      }

      return this.box
    },
  },
  watch:{
    "boxSession.task_id": {
      handler (newTaskID, oldTaskID) {
        if (newTaskID && oldTaskID !== newTaskID){
          this.updateQueueState(newTaskID)
        }
      }
    },
    "queueState.state": {
      handler(newState, oldState){
        switch (newState){
          case "pending":
          case "started":
            this.loaders.startStopBox = true

            if (this.boxSession && oldState === ""){
              this.startQueueStatePolling(this.boxSession.task_id)
            }
            break
          case "running":
            this.loaders.startStopBox = true
            if (this.queueState.tickID){
              clearInterval(this.queueState.tickID)
              this.queueState.tickID = null
              this.loadBoxSessions()
            }
            this.loaders.startStopBox = false

            break
            // default:
            //   clearTimeout(this.timeLeft.tickID)
        }
      }
    },
    boxSession(val){
      if (!val){
        if (this.queueState.tickID){
          clearInterval(this.queueState.tickID)
          this.queueState.tickID = null
        }
        if (this.timeLeft.tickID){
          clearInterval(this.timeLeft.tickID)
          this.timeLeft.tickID = null
        }
        this.queueState.state = ""
        return
      }

      if (this.queueState.state && this.queueState.state !== "running" && !this.queueState.tickID){
        this.updateQueueState(val.task_id)
        this.queueState.tickID = setInterval(() => {
          this.updateQueueState(val.task_id)
        }, 5000)
      }

      if (!this.timeLeft.tickID){
        this.updateFormatedTimeLeft()
        this.timeLeft.tickID = setInterval(() => {
          this.updateFormatedTimeLeft()
        }, 1000)
      }
    },
    currentRealm(){
      if (this.isBoxDynamic){
        this.loadBoxSessions()
      }else{
        this.loadBoxAccess()
      }
    }
  },
  beforeMount() {
    this.loadBox()
  },
  mounted() {
    this.loadSubmissionsForCurrentUser()
  },
  beforeRouteLeave(to, from, next){
    clearTimeout(this.timeLeft.tickID)
    clearInterval(this.queueState.tickID)
    next()
  }
}
</script>

<style scoped>
.small-caption{
  font-size: .7rem !important;
}

.dashed-card{
  border-style: dashed !important;
}
</style>
