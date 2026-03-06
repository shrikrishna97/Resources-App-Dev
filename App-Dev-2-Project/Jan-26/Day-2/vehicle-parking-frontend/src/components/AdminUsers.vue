<template>
  <div>
    <div>Users</div>
    <div >
      <h3>{{ message }}</h3>
      <!-- <h3>{{ items }}</h3> -->
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminUsers',
  data() {
    return {
      message: "",
      items: ""
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
      this.message = res.data.message
      // Implement API call to fetch user details and update user_details array
    },
  },

  mounted() {
    this.fetchUserDetails()
  },
}
</script>
