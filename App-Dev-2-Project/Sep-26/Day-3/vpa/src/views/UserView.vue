<template>
  <div>
    user
    <div v-if="!isLoggedIN">

      <div v-if="!isRegistered"><UserLogin @loggedIn-success="handleLoginSuccess" @register-success="isRegistered = true" /></div>
      <div v-else>
        <UserRegister @registration-success="handleRegistration" @login-success="isRegistered = false"  />
      </div>

    </div>
    <div v-else>
      <UserDash />
    </div>
  </div>
</template>

<script>
import UserLogin from '@/components/UserLogin.vue'
import UserRegister from '../components/UserRegister.vue'
import UserDash from '../components/UserDash.vue'
export default {
  name: 'UserView',
  components: {
    UserRegister,
    UserLogin,
    UserDash,
  },
  data() {
    return {
      isLoggedIN: false,
      isRegistered: false,
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIN = true
    },
    handleRegistration() {
      this.isRegistered = false
      this.isLoggedIn = false
    },
  },
}
</script>
