<template>
  <div>
    <h2>User Summary</h2>
    <p>Total Reservation: {{ summary.total }}</p>
    <p>Active: {{ summary.active_reservations }}</p>
    <p>Completed: {{ summary.completed_reservations }}</p>
    <p>Total Spent: {{ summary.total_spent }}</p>
    <div v-if="summary.lot_names">
      <h3>Lot-wise Reservations</h3>
      <Bar :data="countChartData" :options="{responsive: true}" />
    </div>
    <div>
    <button @click="triggerExport">Export Reservations</button>
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
          }]
      }
    }
  },
  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/api/user/summary',{
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }})
        this.summary = response.data
        console.log(this.summary)
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
    async triggerExport() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/api/export/reservations', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      this.exmsg = response.data
      console.log(this.exmsg)
      alert("check your mail!!")
    }
  },
  mounted() {
    this.fetchSummary()
  }

}
</script>
