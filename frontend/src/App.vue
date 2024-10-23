<script setup>
import './assets/base.css';
import './assets/main.css';
import './assets/styles.css';

</script>

<template>
  <main class="container">
    <header>
      <router-link to="/">
        <img src="/logo.jpg" alt="logo" class="logo" name="logo" />
      </router-link>
    </header>
    <router-view />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  margin:0 auto;
}

.logo {
  display: block;
  height: 100px;
  margin: 0 auto;
}
</style>
