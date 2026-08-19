<template>
  <div>
    <h2>Admin Summary</h2>
    <div v-if="summary">
      <p>Total Reservations: {{ summary.total_reservations }}</p>
      <p>Total Revenue: ${{ summary.total_revenue }}</p>
      <div v-if="summary.lot_names">
        <Bar :data="countChartData" :options="{ responsive: true }" />
      </div>
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
  name: 'AdminSummary',
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
        const token = localStorage.getItem('admin_token')
        const response = await axios.get('http://localhost:5000/api/admin/summary', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.summary = response.data
        console.log(this.summary)
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>
