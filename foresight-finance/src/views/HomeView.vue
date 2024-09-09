<template>
  <!-- IMPORTANT: Have a spinner or some sort of loading screen -->
  <div v-if="!loading" class="zoom-background" :style="{ backgroundImage: `url(${currentImage})` }">
    <h2 id="FFLogoHeader">Foresight Finance</h2>
  </div>

  <div v-else class="spinner">
    <!-- Loading spinner or animation -->
    <span>Loading...</span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
      currentImage: '',
      loading: true
    };
  },
  mounted() {
    this.loading = false
    // Load images dynamically
    this.images = [
      require('@/assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg'),
      require('@/assets/marbleHOMEPAGE-zoom-0.jpg')
    ];

    // Set the initial background image
    this.currentImage = this.images[0];
    // Scroll event listener for background change
    window.addEventListener('scroll', () => {
      {
        const scrollPosition = window.scrollY;
        const viewportHeight = window.innerHeight;

        if (scrollPosition < 1860) {
          const imageIndex = Math.floor(scrollPosition / viewportHeight) % this.images.length;
          this.currentImage = this.images[imageIndex];
        }
      }
    });
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  height: 400vh;
}

.zoom-background {
  position: fixed;
  margin-top: 9.5vh;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-image 1.5s;
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: white;
}

#FFLogoHeader {
  color: white;
}
</style>