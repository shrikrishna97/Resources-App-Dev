<template>
  <div>
    <header>
      <h2>Admin Dashboard</h2>
      <button @click="logout()">Logout</button>
    </header>
    <nav>
      <button @click="activeTab = 'lot'">Lot</button>
      <button @click="activeTab = 'create'" :class="{active: activeTab === 'create'}">Create Lot</button>
      <button @click="activeTab = 'users'" :class="{ active: activeTab === 'users' }">Users</button>
    </nav>
    <main>
      <AdminLots v-if="activeTab === 'lot'" />
      <AdminCreateLot v-if="activeTab === 'create'" />
      <AdminUsers v-if="activeTab === 'users'" />
    </main>
    <div></div>

  </div>
</template>
<script>
import AdminLots from '@/components/AdminLots.vue';
import AdminUsers from '../components/AdminUsers.vue';
import AdminCreateLot from '../components/AdminCreateLot.vue';
export default {
  name: 'AdminDashboard',
  components: { AdminLots, AdminUsers, AdminCreateLot },

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