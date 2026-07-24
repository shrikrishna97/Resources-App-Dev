<template>
  <div>
    <h1>Lots Details</h1>
    <table>
      <thead>
        <tr>
          <th>Lot ID</th>
          <th>Lot Name</th>
          <th>Location</th>
          <th>Total Spots</th>
          <th>Price</th>
          <th>Is Deleted</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in lots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.name }}</td>
          <td>{{ lot.location }}</td>
          <td>{{ lot.total_spots}}</td>
          <td>{{  lot.price }}</td>
          <td>{{ lot.is_deleted }}</td>
        </tr>
      </tbody>
    </table>

  </div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLots',
  data() {
    return {
      lots: [],
         }
  },
  methods: {

    async fetchLots() {
      const token = localStorage.getItem('admin_token');

      const res = await axios.get('http://127.0.0.1:5000/api/admin/parking_lots', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      console.log(res.data)
      this.lots = res.data
    },
  },
  mounted() {
    this.fetchLots()
  },

}

</script>
