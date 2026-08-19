<template>
  <div>
    <header>
      <h2>Admin Dashboard</h2>
      <button @click="logout()">Logout</button>
    </header>
    <nav>
      <button @click="activeTab = 'lot'" ">Lot</button>
      <button @click="activeTab = 'users'" :class="{ active: activeTab === 'users' }">Users</button>
    </nav>
    <main>
      <AdminLots v-if="activeTab === 'lot'" />
      <AdminUsers v-if="activeTab === 'users'" />
    </main>
    <div></div>
    <h1>Admin Dashboard</h1>
    <p>Welcome to the admin dashboard. Here you can manage parking lots, view user data, and perform administrative tasks.</p>

  </div>
</template>
<script>
import AdminLots from '@/components/AdminLots.vue';
import AdminUsers from '../components/AdminUsers.vue';

export default {
  name: 'AdminDashboard',
  components: { AdminLots, AdminUsers },

  data() {
    return {
      activeTab: 'lot',
      // Add any necessary data properties here
    }
  },
  methods: {

    logout() {
      localStorage.removeItem('admin_token');
      this.$router.push('/');
    }
  }
}
</script>