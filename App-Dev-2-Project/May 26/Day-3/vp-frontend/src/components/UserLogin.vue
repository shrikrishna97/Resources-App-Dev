<template>
  <div>
    <form @submit.prevent="loggedIn">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="form.username" placeholder="Username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="form.password" placeholder="Password" />
      </div>
      <button type="submit">Login</button>
    </form>

    <a href="#" @click="$emit('register-success')">Switch to Registration</a>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLogin',
  emits: ['login-success', 'register-success'],
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    }
  },
  methods: {
    async loggedIn() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          username: this.form.username,
          password: this.form.password,
          role: 'user',

        })
        console.log('Login successful:', response.data)
        localStorage.setItem('token', response.data.access_token)
        this.$emit('loggedIn-success')
      } catch (error) {
        console.error('Login error:', error)
      }
    },
  },
}
</script>
