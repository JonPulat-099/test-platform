<template>
  <div class="auth-wrap">
    <Nuxt/>
    <div class="foot">
      <p> <span>&copy; 2023</span></p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "auth",
    middleware: ['no-auth'],
  }
</script>

<style>
.auth-wrap {
  background: url('/bg_main.jpg');
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 1;
}
.auth-wrap::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 2;
  background: rgba(255,255,255, .7);
}
</style>
