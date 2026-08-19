<template>
<div>
    <h1>User Registration</h1>
    <form @submit.prevent="handleRegister">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" v-model="form.username" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="form.email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="form.password" required>
        </div>
        <button type="submit">Register</button>

    </form>
    <a href="#" @click.prevent="$emit('login-here')">Already have an account? Login</a>
</div>

</template>

<script>
import axios from 'axios'

export default {
    name: 'UserRegister',
    emits:['registered'],
    data() {
        return {
            form : {
                username: '',
                email: '',
                password: ''
            }
        }
    },
    methods: {
        async handleRegister() {
            try {
                await axios.post('http://localhost:5000/api/register', this.form)
                this.$emit('registered')
            } catch (error) {
                console.error('Registration failed:', error);
            }
            
        }
    }
}
</script>