<template>
  <div class="scroll-container">
    <div class="image-container">
      <img :src="currentImage" alt="Frame" />
    </div>
  </div>
</template>

<script>
export default {
  name: "Test",
  data() {
    return {
      images: [
      require('@/assets/3d-models/bull-animation/0002.jpg'),
      require('@/assets/3d-models/bull-animation/0003.jpg'),
      require('@/assets/3d-models/bull-animation/0004.jpg'),
      require('@/assets/3d-models/bull-animation/0005.jpg'),
      require('@/assets/3d-models/bull-animation/0006.jpg'),
      require('@/assets/3d-models/bull-animation/0007.jpg'),
      require('@/assets/3d-models/bull-animation/0008.jpg'),
      require('@/assets/3d-models/bull-animation/0009.jpg'),
      require('@/assets/3d-models/bull-animation/0010.jpg'),
      require('@/assets/3d-models/bull-animation/0011.jpg'),
      require('@/assets/3d-models/bull-animation/0012.jpg'),
      require('@/assets/3d-models/bull-animation/0013.jpg'),
      require('@/assets/3d-models/bull-animation/0014.jpg'),
      require('@/assets/3d-models/bull-animation/0015.jpg'),
      require('@/assets/3d-models/bull-animation/0016.jpg'),
      require('@/assets/3d-models/bull-animation/0017.jpg'),
      require('@/assets/3d-models/bull-animation/0018.jpg'),
      require('@/assets/3d-models/bull-animation/0019.jpg'),
      require('@/assets/3d-models/bull-animation/0020.jpg'),
      require('@/assets/3d-models/bull-animation/0021.jpg'),
      require('@/assets/3d-models/bull-animation/0022.jpg'),
      require('@/assets/3d-models/bull-animation/0023.jpg'),
      require('@/assets/3d-models/bull-animation/0024.jpg'),
      require('@/assets/3d-models/bull-animation/0025.jpg'),
      require('@/assets/3d-models/bull-animation/0026.jpg'),
      require('@/assets/3d-models/bull-animation/0027.jpg'),
      require('@/assets/3d-models/bull-animation/0028.jpg'),
      require('@/assets/3d-models/bull-animation/0029.jpg'),
      require('@/assets/3d-models/bull-animation/0030.jpg'),
      require('@/assets/3d-models/bull-animation/0031.jpg'),
      require('@/assets/3d-models/bull-animation/0032.jpg'),
      require('@/assets/3d-models/bull-animation/0033.jpg'),
      require('@/assets/3d-models/bull-animation/0034.jpg'),
      require('@/assets/3d-models/bull-animation/0035.jpg'),
      require('@/assets/3d-models/bull-animation/0036.jpg'),

        // ... other images
      ],
      currentImage: require('@/assets/3d-models/bull-animation/0001.jpg'), // Initial image
      lastUpdate: 0, // Used for throttling updates
    };
  },
  mounted() {
    window.addEventListener("scroll", this.debouncedScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.debouncedScroll);
  },
  methods: {
    handleScroll() {
      const scrollTop = document.documentElement.scrollTop;
      const maxScrollTop =
        document.documentElement.scrollHeight - window.innerHeight;
      const scrollFraction = scrollTop / maxScrollTop;

      const index = Math.min(
        this.images.length - 1,
        Math.floor(scrollFraction * this.images.length)
      );
      this.currentImage = this.images[index];
    },
    debouncedScroll() {
      const now = Date.now();
      // Throttle: Only update every 50ms to prevent excessive triggering
      if (now - this.lastUpdate > 50) {
        this.handleScroll();
        this.lastUpdate = now;
      }
    },
  },
};
</script>

<style scoped>
.scroll-container {
  height: 400vh; /* Adjusted to create enough scrollable area */
  background-color: #eaeaea;
}

.image-container {
  position: fixed; /* Fixed position to keep the image centered */
  top: 50%; /* Center vertically */
  left: 50%; /* Center horizontally */
  transform: translate(-50%, -50%); /* Adjust to center the image */
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60%; /* Full width to support large images */
  background-color: #f0f0f0;
  z-index: 10; /* Ensure it stays above other content */
}

img {
  max-width: 100%;
  height: auto;
  transition: opacity 0.3s ease-in-out; /* Smooth transition for better visual experience */
}
</style>
