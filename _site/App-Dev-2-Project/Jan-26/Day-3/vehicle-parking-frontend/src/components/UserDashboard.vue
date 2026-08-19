<template>
  <div>
    <nav>
      <button @click="activeTab = 'lot'">Lot</button>
      <button @click="activeTab = 'create'" :class="{ active: activeTab === 'create' }">
        Create Reservation
      </button>
    </nav>
    <main>
      <UserLot v-if="activeTab === 'lot'" />
      <UserReservation v-if="activeTab === 'create'" />
    </main>
  </div>
</template>
<script>
// import axios from 'axios'
import UserReservation from '../components/UserReservation.vue';
import UserLot from '../components/UserLot.vue';
export default {
  name: 'UserDashboard',
  components: { UserReservation, UserLot },
  data() {
    return {
      activeTab: 'lot',
    }
  },
}
</script>
