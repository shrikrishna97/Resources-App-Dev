<template>
  <div>
    <form @submit.prevent="loggedIn">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="form.username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
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
    async loggedIn() {
      try {
        console.log('Logging in with:', this.form);
        const response = await axios.post('http://127.0.0.1:5000/api/login', { username: this.form.username, password: this.form.password, role: 'admin' });
        console.log('Login successful:', response.data);
        localStorage.setItem('admin_token', response.data.access_token);
        this.$emit('login-success');
      } catch (error) {
        console.error('Error logging in:', error);
      }
    }
  }
}
</script>
