<template>
  <div>
    <h1>This is an about page {{ title }}</h1>
    <button @click="handleClick">Click</button>

  </div>
</template>

<script>
export default {
  name: 'MyComponent',
  data() {
    return {
      title: 'Hello World',
    }
  },
  methods: {
    handleClick() {
      this.title = 'You clicked the button!';
    }
  },
  mounted() {
    console.log('Component has been mounted!');
  }
}
</script>

<style scoped>
.my-component {
  padding: 20px;
}

h1 {
  color: #42b983;
}
</style>
