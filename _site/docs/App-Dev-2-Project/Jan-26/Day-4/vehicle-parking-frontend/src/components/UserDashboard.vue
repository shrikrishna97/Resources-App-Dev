<template>
  <div>
    <nav>
      <button @click="activeTab = 'lot'">Lot</button>
      <button @click="activeTab = 'create'" :class="{ active: activeTab === 'create' }">
        Create Reservation
      </button>
      <button @click="activeTab = 'my_reservations'" :class="{ active: activeTab === 'my_reservations' }">
        My Reservations
      </button>
    </nav>
    <main>
      <UserLot v-if="activeTab === 'lot'" />
      <UserReservation v-if="activeTab === 'create'" />
      <UserMyReservation v-if="activeTab === 'my_reservations'" />
    </main>
  </div>
</template>
<script>
// import axios from 'axios'
import UserReservation from '../components/UserReservation.vue';
import UserLot from '../components/UserLot.vue';
import UserMyReservation from '../components/UserMyReservation.vue';

export default {
  name: 'UserDashboard',
  components: { UserReservation, UserLot, UserMyReservation },
  data() {
    return {
      activeTab: 'lot',
    }
  },
}
</script>
