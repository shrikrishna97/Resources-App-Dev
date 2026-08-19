<template>
  <div>
    <h1>Create Parking Lot</h1>
    <form @submit.prevent="createLot">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="form.name" required />
      </div>
      <div>
        <label for="city">City:</label>
        <input type="text" id="city" v-model="form.city" required />
      </div>
      <div>
        <label for="location">Location:</label>
        <input type="text" id="location" v-model="form.location" required />
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model.number="form.price" required />
      </div>
      <div>
        <label for="total_spots">Total Spots:</label>
        <input type="number" id="total_spots" v-model.number="form.total_spots" required />
      </div>
      <button type="submit">Create Lot</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminCreateLot',
  data() {
    return {
      form: {
        name: '',
        city: '',
        location: '',
        price: 0,
        total_spots: 0,
      },
    }
  },
  methods: {
    async createLot() {
      try {
        const token = localStorage.getItem('admin_token')
        await axios.post('http://localhost:5000/api/create/parkinglot', this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        alert('Parking lot created successfully!')
        this.form = {
          name: '',
          city: '',
          location: '',
          price: 0,
          total_spots: 0,
        }
        this.$emit('lot-created')
      } catch (error) {
        console.error('Error creating parking lot:', error)
        alert('Failed to create parking lot. Please try again.')
      }
    },
  },
}
</script>
