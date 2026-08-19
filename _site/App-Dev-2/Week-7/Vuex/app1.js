Vue.component('counter-a', {
  template: `
    <div>
      <h3>Component A</h3>
      <p>Count: {{ count }}</p>
      <button @click="inc">+1 from A</button>
    </div>
  `,
  computed: {
    count() {
      return this.$store.state.count
    }
  },
  methods: {
    inc() {
      this.$store.commit('increment')
    }
  }
})

Vue.component('counter-b', {
  template: `
    <div>
      <h3>Component B</h3>
      <p>Count: {{ count }}</p>
      <p>Double: {{ doubleCount }}</p>
      <button @click="dec">-1 from B</button>
      <button @click="incAsync">+1 Async from B</button>
    </div>
  `,
  computed: {
    count() {
      return this.$store.state.count
    },
    doubleCount() {
      return this.$store.getters.doubleCount
    }
  },
  methods: {
    dec() {
      this.$store.commit('decrement')
    },
    incAsync() {
      this.$store.dispatch('incrementAsync')
    }
  }
})

new Vue({
  el: '#app',
  store
})