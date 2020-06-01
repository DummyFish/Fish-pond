export const state = () => ({
  accessGranted: false,
  serviceDataStats: null,
  servicesConfig: {
    services: [],
    honeypot: {}
  },
  servicesColorMapping: {
    ssh: '#AE6A6A',
    ftp: '#A98365',
    rdp: '#9E9E6F',
    redis: '#7BA375',
    smtp: '#5F9DA5',
    telnet: '#6278AF',
    tftp: '#736DB1',
    pop3: '#A979A9',
    honeypot: '#9C9C9A'
  },
  gitRepo: 'https://github.com/DummyFish/Fish-pond',
  password: '',
  logs: [],
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

// services: [
//   { id: 'ssh', status: 1, port: 22 },
//   { id: 'ftp', status: 1, port: 21 },
//   { id: 'rdp', status: 1, port: 3390 },
//   { id: 'redis', status: 1, port: 6379 },
//   { id: 'smtp', status: 1, port: 25 },
//   { id: 'telnet', status: 1, port: 23 },
//   { id: 'tftp', status: 1, port: 69 },
//   { id: 'pop3', status: 1, port: 995 }
// ],
// honeypot: {
//   id: 'honeypot',
//   path: '../logfile.log',
//   ip: '0.0.0.0'
// }

export const mutations = {
  INVERT_ACCESS_GRANTED(state) {
    state.accessGranted = !state.accessGranted
  },

  CHANGE_SERVICES_DATA_STATS(state, stats) {
    state.serviceDataStats = stats
  },

  UPDATE_SERVICES_CONFIGRATION(state, config) {
    state.servicesConfig.services[config.index][config.type] = config.payload
  },

  CHANGE_PASSWORD(state, newPswd) {
    state.password = newPswd
  },

  SET_LOGS(state, payload) {
    state.logs = payload
  },

  SET_TREND(state, payload) {
    state.trendData = payload
  },

  UPDATE_LOGS(state, newLogs) {
    for (const log in newLogs) {
      state.logs.pop()
      state.logs.unshift(log)
    }
  },

  SET_CONFIG(state, payload) {
    state.servicesConfig.services = payload
  },

  SET_HONEYPOT_CONFIG(state, payload) {
    state.servicesConfig.honeypot = payload
  },

  UPDATE_HONEYPOT_CONFIG(state, config) {
    state.servicesConfig.honeypot[config.type] = config.payload
  }
}

export const actions = {
  async fetch_init_data({ commit }) {
    let data = await this.$axios.$get('/api/stats')
    commit('CHANGE_SERVICES_DATA_STATS', data)
    data = await this.$axios.$get('/api/logs')
    commit('SET_LOGS', data)
    data = await this.$axios.$get('/api/trend')
    commit('SET_TREND', data)
    data = await this.$axios.$get('/api/config')
    commit('SET_CONFIG', data)
    data = await this.$axios.$get('/api/honeypot')
    commit('SET_HONEYPOT_CONFIG', data)
  },

  async fetch_update({ commit }) {
    let data = await this.$axios.$get('/api/stats')
    commit('CHANGE_SERVICES_DATA_STATS', data)
    data = await this.$axios.$get('/api/update')
    commit('SET_LOGS', data)
    data = await this.$axios.$get('/api/trend')
    commit('SET_TREND', data)
  },
  // async FETCH_LOGS({ commit }) {
  //   const data = await this.$axios.$get('/api/logs')
  //   commit('SET_LOGS', data)
  // },

  async update_logs({ commit }) {
    const data = await this.$axios.$get('/api/update')
    commit('UPDATE_LOGS', data)
  },

  async reset() {
    await this.$axios.$post('/api/reset')
  },

  async fetch_all_config({ commit }) {
    let data = await this.$axios.$get('/api/config')
    commit('SET_CONFIG', data)
    data = await this.$axios.$get('/api/honeypot')
    commit('SET_HONEYPOT_CONFIG', data)
  },

  async fetch_config({ commit }) {
    const data = await this.$axios.$get('/api/config')
    commit('SET_CONFIG', data)
  },

  async fetch_honeypot_config({ commit }) {
    const data = await this.$axios.$get('/api/honeypot')
    commit('SET_HONEYPOT_CONFIG', data)
  },

  async update_services_configration({ commit }, config) {
    await this.$axios
      .post('/api/config', config)
      .then(function(response) {
        console.log(response)
        commit('UPDATE_SERVICES_CONFIGRATION', config)
      })
      .catch(function(error) {
        console.log(error)
      })
  },

  async update_honeypot_configration({ commit }, config) {
    await this.$axios
      .post('/api/honeypot', config)
      .then(function(response) {
        console.log(response)
        commit('UPDATE_HONEYPOT_CONFIG', config)
      })
      .catch(function(error) {
        console.log(error)
      })
  }
}

export const getters = {
  getServiceDataStats(state) {
    return state.serviceDataStats
  }
}
