<template>
<div>
  <div v-if="!isLoggedIn">
      <UserLogin v-if="!showRegister" @logged-in="handlelogin" @register-here="showRegister =true"/>
      <UserRegister v-else  @registered="handleRegistration" @login-here="showRegister =false"/>
  </div>

<div v-else>
    <UserDashboard  />
</div>


</div>

</template>

<script>
import UserDashboard from '@/components/UserDashboard.vue';
import UserLogin from '../components/UserLogin.vue'
import UserRegister from '../components/UserRegister.vue'

export default {
  name: 'UserView',
  components: {
    UserLogin,
    UserDashboard,
    UserRegister
  },
  data () {
    return {
      isLoggedIn: false,
      showRegister: true
    }
  },
  methods: {
    handleRegistration() {
      this.showRegister = false;
      this.isLoggedIn = true;
    },
    handlelogin() {
      this.isLoggedIn = true;
    }
  }
}
</script>