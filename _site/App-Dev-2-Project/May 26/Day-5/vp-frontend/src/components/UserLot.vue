<template>
  <div>
    <h1>Lots</h1>
    <p v-if="lots.length === 0">No lots found.</p>
    <table v-else>
      <thead>
        <tr>
          <th>Lot ID</th>
          <th>Lot Name</th>
          <th>City</th>
          <th>Location</th>
          <th>Total Spots</th>
          <th>Price (per hour)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.name }}</td>
          <td>{{ lot.city }}</td>
          <td>{{ lot.location }}</td>
          <td>{{ lot.total_spots }}</td>
          <td>{{ lot.price }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'UserLot',
  data() {
    return {
      lots: [],
    }
  },
  methods: {
    async fetchLots() {
      const token = localStorage.getItem('token');

      const res = await axios.get('http://127.0.0.1:5000/api/user/parking_lots', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      console.log(res.data)
      this.lots = res.data
    }
  },
  mounted() {
    this.fetchLots()
  }

}
</script>
