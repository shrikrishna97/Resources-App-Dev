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
      <button @click="activeTab = 'spots'" :class="{ active: activeTab === 'spots' }">Spots</button>
      <button @click="activeTab = 'reservations'" :class="{ active: activeTab === 'reservations' }">Reservations</button>
    </nav>
    <main>
      <AdminLots v-if="activeTab === 'lot'" />
      <AdminCreateLot v-if="activeTab === 'create'" />
      <AdminUsers v-if="activeTab === 'users'" />
      <AdminSpots v-if="activeTab === 'spots'" />
      <AdminReservations v-if="activeTab === 'reservations'" />
    </main>
    <div></div>

  </div>
</template>
<script>
import AdminLots from '@/components/AdminLots.vue';
import AdminUsers from '../components/AdminUsers.vue';
import AdminCreateLot from '../components/AdminCreateLot.vue';
import AdminReservations from '../components/AdminReservations.vue';
import AdminSpots from './AdminSpots.vue';    
export default {
  name: 'AdminDashboard',
  components: { AdminLots, AdminUsers, AdminCreateLot, AdminReservations, AdminSpots },

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