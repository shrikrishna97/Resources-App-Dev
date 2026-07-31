<template>
  <div>
    <h2>User Summary</h2>
    <div><button @click="triggerExport">Export Reservations</button></div>

    <p>Total Reservation: {{ summary.total_reservations }}</p>
    <p>Active: {{ summary.active_reservations }}</p>
    <p>Completed: {{ summary.completed_reservations }}</p>
    <p>Total Spent: {{ summary.total_spent }}</p>
    <div v-if="summary.lot_names">
      <h3>Lot-wise Reservations</h3>
      <Bar :chart-data="countChartData" :options="{ responsive: true }" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'UserSummary',
  components: { Bar },
  data() {
    return {
      summary: [],
      exmsg: null,
    }
  },
  computed: {
    countChartData() {
      return {
        labels: this.summary.lot_names || [],
        datasets: [
          {
            label: 'Reservation',
            data: this.summary.lot_counts || [],
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
          },
        ],
      }
    },
  },
  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/user/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        console.log('Summary response:', response.data)
        console.log(response.data.lot_names)
        this.summary = response.data
        console.log(this.summary)
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
    async triggerExport() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://127.0.0.1:5000/api/user/export_reservations', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      if (response.status === 200) {
        alert('Reservation report sent to your email.')
      } else {
        alert('Failed to send reservation report.')
      }
    },
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>
