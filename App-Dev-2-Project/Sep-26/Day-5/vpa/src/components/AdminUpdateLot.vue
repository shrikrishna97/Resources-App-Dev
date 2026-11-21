<template>
  <div>
    <h1>Update Parking Lot</h1>
    <form @submit.prevent="handleUpdateLot">
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
      <button type="submit">Update Lot</button>
    </form>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: "AdminUpdateLot",
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
    async handleUpdateLot() {
      try {
        const lotId = this.$route.params.id;
        const response = await axios.put(`http://127.0.0.1:5000/api/update_parking_lot/${lotId}`, this.form, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`
          }
        });
        console.log('Lot updated successfully:', response.data);
        this.$router.go(-1);
      } catch (error) {
        console.error('Error updating lot:', error);
      }
    }
  },
  mounted() {
    const lotId = this.$route.params.id;
    axios.get(`http://127.0.0.1:5000/api/parking_lot/${lotId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
      .then(response => {
        this.form = response.data;
      })
      .catch(error => {
        console.error('Error fetching lot details:', error);
      });
  }
}
</script>
