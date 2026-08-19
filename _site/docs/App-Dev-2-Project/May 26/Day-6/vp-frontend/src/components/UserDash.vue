<template>
  <div>

        <header>
      <h1>UserDashboard</h1>
      <button @click="logout()">Logout</button>
    </header>
    <nav>
      <button @click="activeTab = 'lots'">View Lots</button>
      <button @click="activeTab = 'createReservations'">Create Reservation</button>
      <button @click="activeTab = 'reservations'">View Reservations</button>
      <button @click="activeTab = 'summary'">User Summary</button>
    </nav>
    <main>
      <UserLot v-if="activeTab === 'lots'" />
      <UserReservations v-if="activeTab === 'createReservations'" />
      <MyReservations v-if="activeTab === 'reservations'" />
      <UserSummary v-if="activeTab === 'summary'" />
    </main>
  </div>
</template>


<script>
import UserLot from './UserLot.vue'
import UserReservations from './UserReservations.vue'
import MyReservations from './MyReservations.vue'
import UserSummary from './UserSummary.vue'
export default {
  name: 'UserDash',
  components: {
    UserLot,
    UserReservations,
    MyReservations,
    UserSummary
  },
  data() {
    return {
      activeTab: 'lots',
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    },
  },
}
</script>
