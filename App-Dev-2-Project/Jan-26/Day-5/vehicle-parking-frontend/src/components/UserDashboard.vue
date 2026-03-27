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
      <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary' }">
        Summary
      </button>
    </nav>
    <main>
      <UserLot v-if="activeTab === 'lot'" />
      <UserReservation v-if="activeTab === 'create'" />
      <UserMyReservation v-if="activeTab === 'my_reservations'" />
      <UserSummary v-if="activeTab === 'summary'" />
    </main>
  </div>
</template>
<script>
// import axios from 'axios'
import UserReservation from '../components/UserReservation.vue';
import UserLot from '../components/UserLot.vue';
import UserMyReservation from '../components/UserMyReservation.vue';
import UserSummary from '../components/UserSummary.vue';

export default {
  name: 'UserDashboard',
  components: { UserReservation, UserLot, UserMyReservation, UserSummary },
  data() {
    return {
      activeTab: 'lot',
    }
  },
}
</script>
