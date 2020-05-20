export const state = () => ({
  accessGranted: false,
  serviceDataStats: null
})

export const mutations = {
  invertAccessGranted(state) {
    state.accessGranted = !state.accessGranted
  },

  changeServicesDataStats(state, stats) {
    state.serviceDataStats = stats
  }
}

export const actions = {
  async FETCH_SERVICES_DATA({ commit }) {
    const data = await this.$axios.$get('/api/stats')
    commit('changeServicesDataStats', data)
  }
}

export const getters = {
  getServiceDataStats(state) {
    return state.serviceDataStats
  }
}
