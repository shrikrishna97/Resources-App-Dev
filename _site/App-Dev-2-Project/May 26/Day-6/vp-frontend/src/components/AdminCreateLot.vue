<template>
  <div>
    <h2>Create Lot</h2>
    <form @submit.prevent="createlot">
      <div>
        <label for="name">Lot Name:</label>
        <input type="text" id="name" v-model="name" required />
      </div>
      <div>
        <label for="city">City:</label>
        <input type="text" id="city" v-model="city" required />
      </div>
      <div>
        <label for="location">Location:</label>
        <input type="text" id="location" v-model="location" required />
      </div>
      <div>
        <label for="total_spots">Total Spots:</label>
        <input type="number" id="total_spots" v-model="total_spots" required />
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model="price" step="0.01" required />
      </div>
      <button type="submit">Create Lot</button>
    </form>
  </div>
</template>
<script>
import axios from 'axios';
  export default {
    name: 'AdminCreateLot',
    data() {
      return {
        name: '',
        city: '',
        location: '',
        total_spots: 0,
        price: 0,
      }
  },
  methods: {
    async createlot() {
      const lot = {
        name: this.name,
        city: this.city,
        location: this.location,
        total_spots: this.total_spots,
        price: this.price,
      }
      await axios.post('http://127.0.0.1:5000/api/parking_lots', lot, {
          headers: { Authorization: `Bearer ${localStorage.getItem('admin_token')}` },
        })
        .then((response) => {
          console.log('Lot created successfully:', response.data)
          alert('Lot created successfully!')
          // Optionally, you can reset the form fields here
          this.name = ''
          this.city = ''
          this.location = ''
          this.total_spots = 0
          this.price = 0
        })
        .catch((error) => {
          console.error('Error creating lot:', error)
        })
    }
  }
  }
</script>
