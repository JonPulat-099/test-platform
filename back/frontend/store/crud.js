export const state = () => ({
  tests: [],
})

export const getters = {}

export const actions = {
  FETCH_TESTS({commit}) {
    return new Promise(((resolve, reject) => {
      this.$axios.$get('core-tests/')
        .then(data => {
          // console.log(data)
          commit('SET_TESTS', data)
          resolve(data)
        })
        .catch(reject)
    }))
  },
}

export const mutations = {
  SET_TESTS(state, payload) {
    state.tests = payload
  },
}
