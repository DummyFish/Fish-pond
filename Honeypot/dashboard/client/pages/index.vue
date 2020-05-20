<template>
  <v-container fluid>
    <v-row>
      <v-col :cols="9">
        <v-card class="ma-6 pa-6 mt-0">
          <v-text class="display-2 pl-7">Attack attempt count</v-text>
          <v-container fluid>
            <v-row dense>
              <v-col v-for="item in items" :key="item.id" :cols="3">
                <v-card :color="item.color" shaped class="ma-4">
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
          <v-text class="display-2 pl-7">
            Total attack counts in last 10 days
          </v-text>
          <v-card-text>
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
          </v-card-text>
        </v-card>
      </v-col>
      <v-col :col="3">
        <v-card class="mr-6 pa-6 mt-0">
          <v-timeline dark dense>
            <v-timeline-item
              v-for="log in logs"
              :key="log.id"
              :color="colorMap[log.service]"
            >
              <v-card>
                <v-card-text>
                  <p class="display-1 text--primary">
                    {{ log.service }}
                  </p>
                  <p>ip address:</p>
                  <div class="text--primary">
                    {{ log.ip }}
                  </div>
                  <p>time:</p>
                  <div class="text--primary">
                    {{ log.time }}
                  </div>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import individualCount from '../components/individualCount'

export default {
  components: {
    // individualCount
  },
  data: () => ({
    items: [
      {
        id: 'ssh',
        color: '#FFADAD',
        count: 10
      },
      { id: 'ftp', color: '#FFD6A5', count: 15 },
      { id: 'rdp', color: '#FDFFB6', count: 6 },
      { id: 'redis', color: '#CAFFBF', count: 8 },
      { id: 'smtp', color: '#9BF6FF', count: 1 },
      { id: 'telnet', color: '#A0C4FF', count: 4 },
      { id: 'tftp', color: '#BDB2FF', count: 9 },
      { id: 'pop3', color: '#FFC6FF', count: 9 }
    ],
    logs: [
      {
        id: 1,
        ip: '172.134.2.4',
        service: 'rdp',
        time: '2020-5-15 10:04:15'
      },
      {
        id: 2,
        ip: '143.123.78.9',
        service: 'rdp',
        time: '2020-5-14 22:30:20'
      },
      {
        id: 3,
        ip: '246.3.243.23',
        service: 'smtp',
        time: '2020-5-14 21:02:54'
      },
      {
        id: 4,
        ip: '132.35.2.83',
        service: 'telnet',
        time: '2020-5-14 06:53:28'
      },
      {
        id: 5,
        ip: '193.8.13.235',
        service: 'ssh',
        time: '2020-5-13 00:03:23'
      }
    ],
    colorMap: {
      ssh: '#FFADAD',
      ftp: '#FFD6A5',
      rdp: '#FDFFB6',
      redis: '#CAFFBF',
      smtp: '#9BF6FF',
      telnet: '#A0C4FF',
      tftp: '#BDB2FF',
      pop3: '#FFC6FF'
    },
    trendData: {
      labels: [
        '2020-5-10',
        '2020-5-11',
        '2020-5-12',
        '2020-5-13',
        '2020-5-14',
        '2020-5-15',
        '2020-5-16',
        '2020-5-17',
        '2020-5-18',
        '2020-5-19'
      ],
      value: [2, 5, 10, 7, 13, 35, 23, 6]
    }
  })
}
</script>
<style>
.rounded {
  border-radius: 100px;
}
</style>
