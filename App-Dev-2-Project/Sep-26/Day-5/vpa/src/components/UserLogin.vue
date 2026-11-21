<template>
  <div>
    user login
    <form @submit.prevent="handleLogin">
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
    <a href="#" @click="$emit('register-success')">Register</a>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "UserLogin",
  data() {
    return {
      form: {
        username: "",
        password: "",
      }
    }

  },
  methods: {
    async handleLogin() {
      try {
        console.log('Logging in with:', this.form);
        const response = await axios.post('http://127.0.0.1:5000/api/login', { username: this.form.username, password: this.form.password, role: 'user' });
        console.log('Login successful:', response.data);
        localStorage.setItem('user_token', response.data.access_token);
        this.$emit('loggedIn-success');
      } catch (error) {
        console.error('Error logging in:', error);
      }
      }
  }
}
</script>
