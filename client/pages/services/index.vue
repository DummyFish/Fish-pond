<template>
  <v-container fluid>
    <v-row>
      <v-col :cols="12"></v-col>
      <v-card class="ma-6 pa-6 mt-0">
        <v-card-text class="display-2 pl-7">Attack attempt count</v-card-text>
        <v-container fluid>
          <v-row dense>
            <v-col :key="honeypot.id" :cols="12">
              <v-card :color="colorMap[honeypot.id]" shaped class="ma-4">
                <v-card-text
                  class="display-1"
                  v-text="honeypot.id + ' main configration'"
                >
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="hostIp"
                    dense
                    single-line
                    persistent-hint
                    :append-outer-icon="'mdi-check-bold'"
                    :hint="'Service Port #'"
                    :placeholder="honeypot.ip"
                    :rules="[rules.ip]"
                    label="IP address"
                    @click:append-outer="toggleHoneypotConfig('ip')"
                  ></v-text-field>
                  <!-- <v-spacer></v-spacer>
                  <v-text-field
                    dense
                    single-line
                    persistent-hint
                    :append-outer-icon="'mdi-check-bold'"
                    :hint="'Log File Path'"
                    :placeholder="honeypot.path"
                    v-model="logPath"
                    :rules="[rules.path]"
                    label="Log File Path"
                    @click:append-outer="toggleHoneypotConfig('path')"
                  ></v-text-field> -->
                  <v-spacer></v-spacer>
                  <v-btn color="error" @click="resetAll">RESET ALL</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-col>
            <v-col
              v-for="(service, index) in services"
              :key="service.id"
              :cols="12"
            >
              <v-card :color="colorMap[service.id]" shaped class="ma-4">
                <v-card-text class="display-1" v-text="service.id + ' service'">
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-switch
                    persistent-hint
                    :hint="'Service Status'"
                    :input-value="booleanMapping(service.status)"
                    :label="switchLabel(service.status)"
                    @change="toggleServiceStatus(index)"
                  ></v-switch>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="ports[index]"
                    dense
                    single-line
                    persistent-hint
                    :append-outer-icon="'mdi-check-bold'"
                    :hint="'Service Port #'"
                    :placeholder="service.port"
                    :rules="[rules.port]"
                    label="Port"
                    @click:append-outer="toggleServicePort(index)"
                  ></v-text-field>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    rules: {
      required: (value) => !!value || 'Required.',
      port: (value) => (value <= 65535 && value >= 0) || 'Invalid Port #',
      ip: (value) => {
        const pattern = RegExp(
          `^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$`
        )
        return pattern.test(value) || 'Invalid IP address'
      },
      path: (value) => {
        const pattern = RegExp(`/^[a-z]:((\\|/)[a-z0-9s_@-^!#$%&+={}[]]+)$`)
        return pattern.test(value) || 'Invalid IP address'
      }
    },
    ports: ['', '', '', '', '', '', '', ''],
    hostIp: '',
    logPath: ''
  }),
  computed: {
    colorMap() {
      return this.$store.state.servicesColorMapping
    },
    services() {
      return this.$store.state.servicesConfig.services
    },
    honeypot() {
      return this.$store.state.servicesConfig.honeypot
    }
  },
  beforeCreate() {
    this.$store.dispatch('fetch_all_config')
  },
  created() {},
  // mounted() {
  //   this.$store.dispatch('fetch_all_config')
  // },
  methods: {
    toggleServiceStatus(index) {
      //   console.log(`update ${index} ${value} ${event}`);
      //   this.$store.commit('update', { index, value })
      const payload = this.services[index].status === '0' ? '1' : '0'
      // const serviceId = this.services[index].id
      this.$store.dispatch('update_services_configration', {
        index,
        payload,
        type: 'status'
      })
    },
    toggleServicePort(index) {
      console.log(this.ports)
      const payload = this.ports[index]
      // const serviceId = this.services[index].id
      console.log(payload)
      this.$store.dispatch('update_services_configration', {
        index,
        payload,
        type: 'port'
      })
    },
    toggleHoneypotConfig(type) {
      const payload = this.hostIp
      this.$store.dispatch('update_honeypot_configration', {
        payload,
        type: 'ip'
      })
    },
    booleanMapping(num) {
      return num === '1'
    },
    switchLabel(num) {
      return num === '1' ? 'Running' : 'Offline'
    },
    resetAll() {
      this.$store.dispatch('reset')
    }
  }
}
</script>

<style></style>
