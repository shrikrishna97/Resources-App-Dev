export default {
  props: ['loading', 'compact'],

  data() {
    return {
      query: '',
    };
  },

  methods: {
    submit() {
      this.$emit('search', this.query);
    },
  },

  template: `
    <div class="input-group" :class="{ 'input-group-lg': !compact }">
      <input
        type="text"
        class="form-control"
        :placeholder="compact ? 'Search another topic...' : 'Search a topic (e.g. Mars, AI)...'"
        v-model="query"
        @keyup.enter="submit"
      />
      <button class="btn btn-primary" type="button" @click="submit" :disabled="loading">
        <span v-if="!loading">Search</span>
        <span v-else class="spinner-border spinner-border-sm"></span>
      </button>
    </div>
  `,
};
