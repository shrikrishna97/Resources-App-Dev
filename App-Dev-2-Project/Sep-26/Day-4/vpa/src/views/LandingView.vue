<script>
export default {
  name: 'LandingView',
}
</script>

<template>
  <div>
    <nav>
      <RouterLink to="/">Home</RouterLink> |
      <RouterLink to="/admin">Admin</RouterLink> |
      <RouterLink to="/user">User</RouterLink>
    </nav>
    Hi, This is the landing page. Please select a route from the navigation bar.
  </div>
</template>
