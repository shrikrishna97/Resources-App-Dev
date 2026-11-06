export default {
  props: ['topics'],

  template: `
    <div class="mt-4">
      <span class="text-muted me-2">Try:</span>
      <button
        v-for="topic in topics"
        :key="topic"
        type="button"
        class="btn btn-sm btn-outline-secondary rounded-pill me-1 mb-2"
        @click="$emit('select', topic)"
      >
        {{ topic }}
      </button>
    </div>
  `,
};
