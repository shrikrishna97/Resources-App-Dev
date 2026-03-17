<template>
<div>
  VPA
<div>

<div @click="$router.push('/admin')">
    Admin View
</div>

<div @click="$router.push('/user')">
    User View
</div>
</div>

</div>


</template>

<script>
export default {
  name: 'LandingView'
}

</script>
