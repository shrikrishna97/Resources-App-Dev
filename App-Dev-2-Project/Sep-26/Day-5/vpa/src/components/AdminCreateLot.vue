<template>
  <div>
    <h1>Create Parking Lot</h1>
    <form @submit.prevent="handleCreateLot">
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
        <label for="total_spots">Total Spots:</label>
        <input type="number" id="total_spots" v-model="form.total_spots" required />
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model="form.price" required />
      </div>
      <button type="submit">Create Lot</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "AdminCreateLot",
  data() {
    return {
      form: {
        name: "",
        city: "",
        location: "",
        total_spots: "",
        price: ""
      }
    }
  },
  methods: {
    async handleCreateLot() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/create_parking_lot', this.form, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        });
        console.log('Parking lot created:', response.data);
        this.form.city = '';
        this.form.location = '';
        this.form.name = '';
        this.form.price = '';
        this.form.total_spots = '';
      }
      catch (error) {
        console.error('Error creating parking lot:', error);
      }
    }
  }
}

</script>
