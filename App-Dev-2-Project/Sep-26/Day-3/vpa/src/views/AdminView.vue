<template>
  <div>
    admin view

    <div v-if="!isLoggedIn">
    <AdminLogin @login-success="handleLoginSuccess"/>
    </div>

    <div v-else>
    <AdminDash />
    </div>
  </div>
</template>

<script>
import AdminLogin from '../components/AdminLogin.vue';
import AdminDash from '../components/AdminDash.vue';

export default {
  name: 'AdminView',
  components: {
    AdminLogin,
    AdminDash,
  },
  data() {
    return {
      isLoggedIn: false,
    };
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true;
    }
  }
}
</script>
