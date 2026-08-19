<template>
  <div>
    <div>Users</div>
    <div >
      <div v-for="user in users" :key="user.id">
        <p>{{ user.id }}</p>
        <p>{{ user.username }}</p>
        <p>{{ user.email }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminUsers',
  data() {
    return {
      users: [],
    }
  },
  methods: {
    async fetchUserDetails() {
      const token = localStorage.getItem('admin_token')
      const res = await axios.get('http://localhost:5000/api/get-data', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      console.log('User Details response:', res.data)
      this.users = res.data || []
    },
  },

  mounted() {
    this.fetchUserDetails()
  },
}
</script>
