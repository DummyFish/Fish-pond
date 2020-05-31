export const state = () => ({
  accessGranted: false,
  serviceDataStats: null,
  servicesConfig: {
    services: [
      { id: 'ssh', status: 1, port: 22 },
      { id: 'ftp', status: 1, port: 21 },
      { id: 'rdp', status: 1, port: 3390 },
      { id: 'redis', status: 1, port: 6379 },
      { id: 'smtp', status: 1, port: 25 },
      { id: 'telnet', status: 1, port: 23 },
      { id: 'tftp', status: 1, port: 69 },
      { id: 'pop3', status: 1, port: 995 }
    ],
    honeypot: {
      id: 'honeypot',
      path: '../logfile.log',
      ip: '0.0.0.0'
    }
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
  trendData: null
})

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

  update_services_configration({ commit }, config) {
    commit('UPDATE_SERVICES_CONFIGRATION', config)
  }
}

export const getters = {
  getServiceDataStats(state) {
    return state.serviceDataStats
  }
}
