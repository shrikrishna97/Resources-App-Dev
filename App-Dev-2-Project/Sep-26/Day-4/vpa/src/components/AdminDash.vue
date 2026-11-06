<template>
  <div>

    <header>
      <h2>Admin Dashboard</h2>
      <button @click="logout()">Logout</button>
    </header>
    <nav>
      <button @click="activeTab = 'lots'">View Lots Details</button>
      <button @click="activeTab = 'users'">User Details</button>
    </nav>
    <div></div>
    <main>
      <AdminLots v-if="activeTab === 'lots'" />
      <AdminUser v-if="activeTab === 'users'" />
    </main>
  </div>
</template>

<script>
import AdminLots from './AdminLots.vue'
import AdminUser from './AdminUser.vue'
export default {
  name: 'AdminDash',
  components: {
    AdminLots,
    AdminUser,
  },
  data() {
    return {
      activeTab: 'lots',
    }
  },
  methods: {
    logout() {

      localStorage.removeItem('admin_token');
      localStorage.clear();
      this.$router.push('/')
      this.$emit('logout');
    }
  }
}
</script>
