<template>
  <div>
    <div>Lots</div>
    <div v-for="lot in lot_details" :key="lot.id">
      <h3>{{ lot.name }}</h3>
      <p>City: {{ lot.city }}</p>
      <p>Price: {{ lot.price }}</p>
      <p>Total Spots: {{ lot.total_spots }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLot',
  data() {
    return {
      lot_details: [],
    }
  },
  methods: {
    async fetchLotDetails() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5000/api/get/user/parkinglots', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      // Implement API call to fetch lot details and update lot_details array
      this.lot_details = res.data
    },
  },

  mounted() {
    this.fetchLotDetails()
  },
}
</script>
