<template>
  <div>
    <h2>Create Reservation</h2>
    <form @submit.prevent="createReservation">
      <div>
        <label for="lot">Select Lot:</label>
        <select v-model="form.selected_lot" required>
          <option v-for="lot in lot_details" :key="lot.id" :value="lot.id">
            {{ lot.name }} - Rs{{ lot.price }}/hr
          </option>
        </select>
      </div>
      <div>
        <label for="vehicle_number">Vehicle Number:</label>
        <input type="text" id="vehicle_number" v-model="form.vehicle_number" required />
      </div>
      <div>
        <label for="start_time">Start Time:</label>
        <input type="datetime-local" v-model="form.start_time" required />
      </div>
      <div>
        <label for="end_time">End Time:</label>
        <input type="datetime-local" v-model="form.end_time" required />
      </div>
      <button type="submit">Create Reservation</button>
    </form>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {
      lot_details: [],
      form: {
        selected_lot: null,
        vehicle_number: '',
        start_time: '',
        end_time: '',
      },
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
      createReservation() {
        const token = localStorage.getItem('token')
        axios
          .post(
            'http://localhost:5000/api/user_reservation', this.form,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          )
          .then((response) => {
            console.log('Reservation created:', response.data)
            alert('Reservation created successfully!')
          })
          .catch((error) => {
            console.error('Error creating reservation:', error)
            alert('Failed to create reservation. Please try again.')
          })
    },
  },
  mounted() {
    this.fetchLotDetails()
  },
}
</script>
