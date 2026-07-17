<template>
  <div>
    <form @submit.prevent="registerUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" placeholder="Username" v-model="form.username" />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" placeholder="Email" v-model="form.email" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" placeholder="Password" v-model="form.password" />
      </div>
      <button type="submit">Register</button>
    </form>

    <a href="#" @click="$emit('login-success')">Switch to Login</a>


  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "UserRegister",
  emits: ['registration-success', 'login-success'],
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
      },

    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post("http://localhost:5000/register", this.form);
        console.log(response.data);
        alert("Registration successful!");
        this.$emit('registration-success');
        // this.$router.push(-1);
      } catch (error) {
        console.error(error);
        alert("Registration failed. Please try again.");
      }
    },
  }

}
</script>
