<template>
  <div>
    <div v-for="user in users" :key="user.id">
      <p>Name: {{ user.username }}</p>
      <p>Email: {{ user.email }}</p>
      <p>Role: {{ user.role }}</p>
      <p>Status: {{ user.status }}</p>
      <p></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "AdminUser",
  data() {
    return {
      users: []
    }
  },
  methods: {
    async fetchUsers() {
      await axios.get('http://127.0.0.1:5000/api/user_data', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        }
      })
      .then(response => {
        this.users = response.data;
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });

    }
  },
  mounted() {
    this.fetchUsers();
  }
}
</script>
