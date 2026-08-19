<template>
  <div>
    <h1>Reservations</h1>
    <p v-if="reservations.length === 0">No reservations found.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Reservation ID</th>
          <th>User ID</th>
          <th>Spot ID</th>
          <th>Vehicle Number</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reservation in reservations" :key="reservation.id">
          <td>{{ reservation.id }}</td>
          <td>{{ reservation.user_id }}</td>
          <td>{{ reservation.spot_id }}</td>
          <td>{{ reservation.vehicle_number }}</td>
          <td>{{ reservation.start_time }}</td>
          <td>{{ reservation.end_time }}</td>
          <td>{{ reservation.cost }}</td>
          <td>{{ reservation.status }}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AdminReservations',
  data() {
    return {
      reservations: [],
    }
  },
  methods: {
    async fetchReservations() {
      const token = localStorage.getItem('admin_token');

      const res = await axios.get('http://127.0.0.1:5000/api/admin/reservations', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      console.log(res.data)
      this.reservations = res.data
    }
  },
  mounted() {
    this.fetchReservations()
  }
}
</script>
