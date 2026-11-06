<template>
  <div>
    <h1>Admin Lots</h1>
    <ul>
      <li v-for="lot in lots" :key="lot.id">
        {{ lot.name }} - {{ lot.city }} - {{ lot.location }} - {{ lot.total_spots }} - {{ lot.price }}
      </li>
    </ul>

  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: "AdminLots",
  data() {
    return {
      lots: []
    }
  },
  methods: {
    async fetchLots() {
      await axios.get('http://127.0.0.1:5000/api/admin/parking_lots', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        }
      })
      .then(response => {
        this.lots = response.data;
      })
      .catch(error => {
        console.error('Error fetching parking lots:', error);
      });

    }
  },
  mounted() {
    this.fetchLots();
  }
}
</script>
