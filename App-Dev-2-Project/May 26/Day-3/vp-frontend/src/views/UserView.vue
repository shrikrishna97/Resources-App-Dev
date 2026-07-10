<template>
  <div>
    User
    <div v-if="!isloggedIn">
      <div v-if="!isRegistered"><UserLogin @login-success="handleLoginSuccess" @registration-success="isRegistered = true"/></div>
      <div v-else><UserRegister @registration-success="handleRegistration"  /></div>
    </div>
    <div v-else>
      <UserDash />
    </div>
  </div>
</template>

<script>
import UserDash from '@/components/UserDash.vue'
import UserRegister from '@/components/UserRegister.vue'
import UserLogin from '@/components/UserLogin.vue'

export default {
  name: 'UserView',
  components: {
    UserDash,
    UserRegister,
    UserLogin,
  },
  data() {
    return {
      isloggedIn: false,
      isRegistered: false,
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isloggedIn = true
    },
    handleRegistration() {
      this.isRegistered = false
      // this.isloggedIn = true
      console.log(this.isRegistered)
      alert('Registration successful! You can now log in.')
    },
  },
}
</script>
