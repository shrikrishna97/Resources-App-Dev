<template>
  <div>user register
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="form.username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="form.password" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <a href="#" @click="$emit('login-success')">Already have an account? Login</a>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "UserRegister",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
      }
    }
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/register', this.form);
        console.log('Registration successful:', response.data);
        this.$emit('registration-success');
      }catch (error) {
        console.error('Error registering:', error);
      }
    }
  }
}

</script>
