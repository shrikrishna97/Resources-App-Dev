<template>
  <div>
    <div v-if ="!isloggedIn">
      <AdminLogin @logged-in="handleAdminLogin" />
    </div>
    <div v-else>
      <AdminDashboard />
    </div>

  </div>

</template> 
<script>
import AdminDashboard from '@/components/AdminDashboard.vue';
import AdminLogin from '@/components/AdminLogin.vue';

export default {
  name: "AdminView",
  components: {
    AdminLogin,
    AdminDashboard
  },
  data() {
    return {
      isloggedIn: false
    }
  },
  methods: {
    handleAdminLogin() {
      this.isloggedIn = true;
    }
  }

}
</script>
