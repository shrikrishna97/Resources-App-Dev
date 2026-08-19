<template>
  <div>
    <h2>Admin User Management</h2>
    <ul>
      <li v-for="user in users" :key="user.username">
        <!-- {{ users[0] }} -->
        {{ user.username }} - {{ user.email }} - {{ user.role }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminUser',
  data() {
    return {
      users: [],
    }
  },
  methods: {
    async fetchUsers() {
      const res = await axios.get('http://127.0.0.1:5000/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('admin_token')}` },
      })
      console.log('Users fetched successfully:', res.data)
      this.users =
        res.data ||
        []
    },
  },
  mounted() {
    this.fetchUsers()
  },
}
</script>
