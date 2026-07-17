<template>
  <div>
    <header>
      <h1>Admin Dashboard</h1>
      <button @click="logout()">Logout</button>
    </header>

    <nav>
      <button @click="activeTab = 'users'">View Users</button>
      <button @click="activeTab = 'create-lot'">Create Lot</button>
    </nav>
    <main>
      <AdminUser v-if="activeTab === 'users'" />
      <AdminCreateLot v-if="activeTab === 'create-lot'" />
    </main>
  </div>
</template>

<script>
// import axios from 'axios'
import AdminUser from './AdminUser.vue'
import AdminCreateLot from './AdminCreateLot.vue'
export default {
  name: 'AdminDash',
  components: {
    AdminUser,
    AdminCreateLot,
  },
  data() {
    return {
      activeTab: 'users',
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/')
    },
  },
}
</script>
