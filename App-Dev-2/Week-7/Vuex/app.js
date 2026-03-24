new Vue({
  el: '#app',
  store,
  // data: {
  //    return { msg: 'hello world' } 
  // },
  computed: {
    count() {
      return this.$store.state.count
    },
    doubleCount() {
      return this.$store.getters.doubleCount
    }
  },
  methods: {
    increment() {
      this.$store.commit('increment')
    },
    decrement() {
      this.$store.commit('decrement')
    },
    incrementAsync() {
      this.$store.dispatch('incrementAsync')
    }
  },

})