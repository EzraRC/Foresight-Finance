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

/* Offset main content to avoid overlap with the fixed navbar */
#app > .scroll-wrapper {
  margin-top: 80px; /* Adjust to match navbar height */
}
</style>
