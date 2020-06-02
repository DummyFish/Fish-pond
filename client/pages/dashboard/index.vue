<template>
  <v-container fluid>
    <v-row>
      <v-col :cols="9">
        <v-card class="ma-6 pa-6 mt-0">
          <v-card-text class="display-2 pl-7">Attack attempt count</v-card-text>
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
          <!-- <v-card-text>
            <v-sheet color="rgba(0, 0, 0, .12)">
              <v-sparkline
                :labels="trendData.labels"
                :value="trendData.value"
                color="rgba(255, 255, 255, .7)"
                height="100"
                padding="24"
                stroke-linecap="round"
                smooth
              >
              </v-sparkline>
            </v-sheet>
          </v-card-text> -->
          <streamGraph> </streamGraph>
        </v-card>
      </v-col>
      <v-col :col="3">
        <v-card class="mr-6 pa-6 mt-0">
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
  data: () => ({
    // items: [
    //   {
    //     id: 'ssh',
    //     color: '#AE6A6A',
    //     count: 10
    //   },
    //   { id: 'ftp', color: '#A98365', count: 15 },
    //   { id: 'rdp', color: '#9E9E6F', count: 6 },
    //   { id: 'redis', color: '#7BA375', count: 8 },
    //   { id: 'smtp', color: '#5F9DA5', count: 1 },
    //   { id: 'telnet', color: '#6278AF', count: 4 },
    //   { id: 'tftp', color: '#736DB1', count: 9 },
    //   { id: 'pop3', color: '#A979A9', count: 9 }
    // ],
    // logs: [
    //   {
    //     id: 1,
    //     ip: '172.134.2.4',
    //     service: 'rdp',
    //     time: '2020-5-15 10:04:15'
    //   },
    //   {
    //     id: 2,
    //     ip: '143.123.78.9',
    //     service: 'rdp',
    //     time: '2020-5-14 22:30:20'
    //   },
    //   {
    //     id: 3,
    //     ip: '246.3.243.23',
    //     service: 'smtp',
    //     time: '2020-5-14 21:02:54'
    //   },
    //   {
    //     id: 4,
    //     ip: '132.35.2.83',
    //     service: 'telnet',
    //     time: '2020-5-14 06:53:28'
    //   },
    //   {
    //     id: 5,
    //     ip: '193.8.13.235',
    //     service: 'ssh',
    //     time: '2020-5-13 00:03:23'
    //   }
    // ],
    // colorMap: {
    //   ssh: '#AE6A6A',
    //   ftp: '#A98365',
    //   rdp: '#9E9E6F',
    //   redis: '#7BA375',
    //   smtp: '#5F9DA5',
    //   telnet: '#6278AF',
    //   tftp: '#736DB1',
    //   pop3: '#A979A9'
    // },
    // trendData: {
    //   labels: [
    //     '2020-5-10',
    //     '2020-5-11',
    //     '2020-5-12',
    //     '2020-5-13',
    //     '2020-5-14',
    //     '2020-5-15',
    //     '2020-5-16',
    //     '2020-5-17',
    //     '2020-5-18',
    //     '2020-5-19'
    //   ],
    //   value: [2, 5, 10, 7, 13, 35, 23, 6]
    // }
  }),
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
  // created() {
  //   if (!this.$auth.loggedIn) {
  //     console.log('before create')
  //     this.$router.push({
  //       path: '/login'
  //     })
  //   }
  // },
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
