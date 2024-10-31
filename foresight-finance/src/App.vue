<template>
  <div id="app">
    <NavBar /> <!-- Fixed navbar rendered at the top -->
    <router-view /> <!-- Main content rendered below -->
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
</script>

<style>
#app {
  font-family: "Monda", sans-serif;
}

/* Ensure NavBar stays fixed across the app */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: 80px; /* Adjust to your navbar height */
  z-index: 1000; /* Keep above other elements */
}

/* Offset main content to avoid overlap with the fixed navbar */
#app > .scroll-wrapper {
  margin-top: 80px; /* Adjust to match navbar height */
}
</style>
