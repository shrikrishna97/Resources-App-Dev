export const counter = {
  props: ["name", "message"],
  template: `<div>
            count something in the app {{name}}
            <h3>hello {{message}}</h3>
            <button @click="notifyParent">Notify Parent</button>
            <p><strong>Notice:</strong>
            <slot name="header">
            <h1>hi</h1>
            </slot>
            </p>
            </div>`,
  methods: {
    notifyParent() {
      this.$emit("child-clicked", "Hello from Child!");
    },
  },
};
