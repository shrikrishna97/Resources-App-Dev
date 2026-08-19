<template>
  <div>
    <div>Reservations</div>

    <table>
      <thead>
        <tr>
        <th>ID</th>
        <th>User</th>
        <th>Vehicle Number</th>
        <th>Lot Name</th>
        <th>City</th>
        <th>Spot Number</th>
        <th>Start Time</th>
        <th>End Time</th>
        <th>Status</th>
        <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reservation in reservations" :key="reservation.id">
          <td>{{ reservation.id }}</td>
          <td>{{ reservation.user_name }}</td>
          <td>{{ reservation.vehicle_number }}</td>
          <td>{{ reservation.parking_lot.name }}</td>
          <td>{{ reservation.parking_lot.city }}</td>
          <td>{{ reservation.spot_number }}</td>
          <td>{{ reservation.start_time }}</td>
          <td>{{ reservation.end_time }}</td>
          <td>{{ reservation.status }}</td>
          <td>Rp.{{ reservation.cost }}</td>
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
      try {
        const token = localStorage.getItem('admin_token')
        const response = await axios.get('http://localhost:5000/api/admin/reservations', {
          headers: { Authorization: `Bearer ${token}` },
        })
        console.log('API response:', response.data)
          this.reservations = response.data
        // console.log('Fetched reservations:', this.reservations)
      } catch (error) {
        console.error('Error fetching reservations:', error)
      }
    },
  },
  mounted() {
    this.fetchReservations()
  },
}
</script>
