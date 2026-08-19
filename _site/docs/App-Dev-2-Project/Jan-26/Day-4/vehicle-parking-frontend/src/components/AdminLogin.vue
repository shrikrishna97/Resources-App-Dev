<template>
  <div>
    <h1>Admin Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" v-model="form.username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="form.password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminLogin',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://localhost:5000/api/admin/login', this.form)
        console.log('Admin Login response:', response.data)
        localStorage.setItem('admin_token', response.data.data.access_token)
        this.$emit('logged-in')
      } catch (error) {
        console.error('Admin Login error:', error)
      }
    },
  },
}
</script>
