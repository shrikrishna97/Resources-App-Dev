<template>
  <div>
    <div>Admin here it is</div>

    <div v-if="!isloggedIn" >
      <AdminLogin  @login-success="handleLoginSuccess"/>
    </div>

    <div v-else>
      <AdminDash />
    </div>
  </div>
</template>

<script>
import AdminLogin from '../components/AdminLogin.vue'
import AdminDash from '../components/AdminDash.vue'
// import axios from 'axios';

export default {
  name: 'AdminView',
  components: {
    AdminLogin,
    AdminDash,
  },
  data() {
    return {
      isloggedIn: false,
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isloggedIn = true
    },
  },
}
</script>
