const Child = {
  props: ["name"],

  template: `
    <div>
        {{name}}
        <button @click="$emit('remove')">
            Delete
        </button>
    </div>
            `,
};

new Vue({
  el: "#app",
  components: { Child },

  data() {
    return {
      student: "Alice",
    };
  },

  methods: {
    deleteStudent() {
      this.student = "";
    },
  },
});
