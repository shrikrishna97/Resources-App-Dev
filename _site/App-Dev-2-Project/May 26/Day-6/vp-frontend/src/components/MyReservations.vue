<template>
  <div>
    <h1>My Reservations</h1>
    <p v-if="reservations.length === 0">No reservations found.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Parking Lot</th>
          <th>Vehicle Number</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reservation in reservations" :key="reservation.id">
          <td>{{ reservation.parking_lot_name }}</td>
          <td>{{ reservation.vehicle_number }}</td>
          <td>{{ reservation.start_time }}</td>
          <td>{{ reservation.end_time }}</td>
          <td>{{ reservation.cost }}</td>
          <td>{{ reservation.status }}</td>
          <td></td>
            <button v-if="reservation.status === 'active'" @click="completeReservation(reservation.id)">Complete</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'MyReservations',
  data() {
    return {
      reservations: [],
    };
  },
  methods: {
    async fetchReservations() {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://127.0.0.1:5000/api/user_reservations', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      this.reservations = res.data;
    },
    async completeReservation(reservationId) {
      const token = localStorage.getItem('token');
      await axios.put(`http://127.0.0.1:5000/api/user_reservations/${reservationId}`, {}, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      this.fetchReservations(); // Refresh the reservations list after completing one
    },
  },
  mounted() {
    this.fetchReservations();
  },
}
</script>
