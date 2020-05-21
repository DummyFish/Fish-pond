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
  }
})

export const mutations = {
  invertAccessGranted(state) {
    state.accessGranted = !state.accessGranted
  },

  changeServicesDataStats(state, stats) {
    state.serviceDataStats = stats
  },

  updateServicesConfigration(state, config) {
    state.servicesConfig.services[config.index][config.type] = config.payload
  }
}

export const actions = {
  async FETCH_SERVICES_DATA({ commit }) {
    const data = await this.$axios.$get('/api/stats')
    commit('changeServicesDataStats', data)
  },

  UPDATE_SERVICES_CONFIGRATION({ commit }, config) {
    commit('updateServicesConfigration', config)
  }
}

export const getters = {
  getServiceDataStats(state) {
    return state.serviceDataStats
  }
}
