<template>
  <v-container fluid>
    <v-row>
      <v-col :cols="9">
        <v-card class="ma-6 pa-6 mt-0">
          <v-card-text class="display-2 pl-7">Attack Count</v-card-text>
          <v-container fluid>
            <v-row dense>
              <v-col v-for="item in items" :key="item.id" :cols="3">
                <v-card :color="colorMap[item.id]" shaped class="ma-4">
                  <v-card-text class="display-1" v-text="item.id">
                  </v-card-text>
                  <v-card-text class="display-4" v-text="item.count">
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card class="ma-6 pa-6 mt-0">
          <v-card-text class="display-2 pl-7">
            Attack Trends
          </v-card-text>
          <streamGraph></streamGraph>
        </v-card>
      </v-col>
      <v-col :col="3">
        <v-card class="mr-6 pa-6 mt-0">
          <v-card-text class="display-2 pl-7">Attack Timeline</v-card-text>
          <v-timeline dark dense>
            <v-slide-x-transition group>
              <v-timeline-item
                v-for="log in logs"
                :key="log.id"
                :color="colorMap[log.service]"
              >
                <v-card>
                  <v-card-text>
                    <span class="display-1 text--primary">
                      {{ log.service }}
                    </span>
                    <br />
                    <span class="text--primary">IP Address:</span>
                    <br />
                    <span>
                      {{ '  ' + log.ip }}
                    </span>
                    <br />
                    <span class="text--primary">Time:</span>
                    <br />
                    <span>
                      {{ '  ' + log.time }}
                    </span>
                    <br />
                    <span class="text--primary">Metadata:</span>
                    <br />
                    <span v-for="metadata in filter(log.meta)" :key="metadata">
                      {{ '  ' + metadata }}
                    </span>
                  </v-card-text>
                  <v-card-actions>
                    <!-- <v-spacer></v-spacer>
                  <v-btn>Details</v-btn> -->
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </v-slide-x-transition>
          </v-timeline>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import streamGraph from '@/components/streamGraph.vue'

export default {
  components: {
    streamGraph
  },
  data: () => ({}),
  computed: {
    colorMap() {
      return this.$store.state.servicesColorMapping
    },
    items() {
      return this.$store.state.serviceDataStats
    },
    logs() {
      return this.$store.state.logs
    },
    trendData() {
      return this.$store.state.trendData
    }
  },
  methods: {
    filter(arr) {
      return arr.filter((meta) => meta !== '')
    }
  },
  mounted() {
    this.$store.dispatch('fetch_init_data')
    // var updateLogs =
    window.setInterval(() => {
      this.$store.dispatch('fetch_update')
    }, 5000)
  }
}
</script>
<style>
.rounded {
  border-radius: 100px;
}
</style>
