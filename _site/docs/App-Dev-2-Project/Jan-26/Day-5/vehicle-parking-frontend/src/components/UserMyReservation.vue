<template>
<div>
    <h2>My Reservations</h2>
    <ul>
        <li v-for="reservation in reservations" :key="reservation.id">
            <p>Parking Lot: {{ reservation.parking_lot.name }}</p>
            <p>Vehicle Number: {{ reservation.vehicle_number }}</p>
            <p>Start Time: {{ reservation.start_time }}</p>
            <p>End Time: {{ reservation.end_time }}</p>
            <p>Status: {{ reservation.status }}</p>
            <p>Cost: {{ reservation.cost }}</p>
            <button v-if="reservation.status === 'active'" @click="releaseReservation(reservation.id)">Release</button>
        </li>
        
    </ul>
</div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'UserMyReservation',
    data() {
        return {
            reservations: []
        }
    },
    methods: {
        async fetchReservations() {
            const token = localStorage.getItem('token')
            const res = await axios.get('http://localhost:5000/api/user/my_reservations', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.reservations = res.data
        },
        async releaseReservation(reservationId) {
            const token = localStorage.getItem('token')
            await axios.put(`http://localhost:5000/api/user_reservations/${reservationId}/release`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.fetchReservations() // Refresh the reservations list
        }
    },
    mounted() {
        this.fetchReservations()
    }
}
</script>
