const store = new Vuex.Store({
  state: {
    count: 0
  },

  getters: {
    doubleCount(state) {
      return state.count * 2
    }
  },

  mutations: {
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    }
  },

  actions: {
    incrementAsync({ commit }) {
      setTimeout(() => {
        commit('increment')
      }, 1000)
    }
  }
})