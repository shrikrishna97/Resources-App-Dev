<template>
  <div>
    <h1>User Reservations</h1>
    <form @submit.prevent="createReservation">
      <div>
        <label for="lot">Select Lot:</label>
        <select v-model="form.selected_lotId" required>
          <option v-for="lot in lot_details" :key="lot.id" :value="lot.id">
            {{ lot.name }}
          </option>
        </select>
      </div>

      <div>
        <label for="vehicle_number">Vehicle Number:</label>
        <input type="text" v-model="form.vehicle_number" required />
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
  name: 'UserReservations',
  data() {
    return {
      lot_details: [],
      form: {
        parking_lot_id: '',
        vehicle_number: '',
        start_time: '',
        end_time: '',
      },
    }
  },
  methods: {
    async fetchLotDetails() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://127.0.0.1:5000/api/user/parking_lots', {
        headers: { Authorization: `Bearer ${token}` },
      })
      // console.log(res.data)
      this.lot_details = res.data
    },
  },
  createReservation() {
    console.log(this.form)

    const formData = {
      parking_lot_id: this.form.selected_lotId,
      vehicle_number: this.form.vehicle_number,
      start_time: this.form.start_time,
      end_time: this.form.end_time,
    }
    const token = localStorage.getItem('token')
    console.log(token)
    const res = axios.post('http://127.0.0.1:5000/api/user_reservations', formData, {
      headers: { Authorization: `Bearer ${token}` },
    })
    console.log(res.data)
    this.form.parking_lot_id = ''
    this.form.vehicle_number = ''
    this.form.start_time = ''
    this.form.end_time = ''
  },
  mounted() {
    this.fetchLotDetails()
  },
}
</script>
