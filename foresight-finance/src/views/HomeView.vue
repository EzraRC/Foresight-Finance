<template>
  <!-- IMPORTANT: Have a spinner or some sort of loading screen -->
  <div v-if="!loading">
    <!-- Fixed background -->
    <div class="zoom-background" :style="{ backgroundImage: `url(${currentImage})` }"></div>

    <!-- Text that scrolls with the page -->
    <div class="scrolling-content">
      <!-- Foresight Finance Logo Container -->
      <div class="logo-container">
        <h2 id="FFLogoHeader">Foresight Finance</h2>
      </div>

      <!-- Motto Container -->
      <div class="motto-container">
        <h1>An advanced way to get ahead of the ever-changing markets</h1>
      </div>

      <!-- Transparent navy bubble for text -->
      <div class="bubble-container">
        <p class="bubble-text">Build and maximize your portfolio with AI-enhanced pattern recognition</p>
      </div>

      <!-- Candlestick chart SVG with background -->
      <div class="svg-container">
        <img src="@/assets/example_candlestick_chart.svg" alt="Candlestick Chart" class="candlestick-svg" />
      </div>

      <!-- Discover button -->
      <div class="button-container" style="margin-bottom: -200px;">
        <button class="discover-button" @click="navigateToAIPR">Discover patterns now!</button>
      </div>

      <!-- Educational Page promotion bubbles-->
      <div class="new-bubble-container" style="margin-left: 900px; text-align: right; display: flex; align-items: center;">
        <p class="new-bubble-text">We offer a variety of different lessons ranging from beginner topics, all the way to advanced technical patterns!</p>
      </div>

      <div class="new-bubble-container" style="margin-bottom: 50px; margin-left: 900px; text-align: right; display: flex; align-items: center;">
        <p class="new-bubble-text">Want to learn more about financial markets, investment terms, and overall financial literacy?</p>
      </div>

      <!-- Learn with us button -->
      <div class="button-container" style="margin-bottom: 30px; margin-right: 160px; margin-left: 900px; text-align: right;">
        <button class="discover-button" @click="navigateToLearning">Learn with us!</button>
      </div>

      <!-- Gold bull GIF -->
      <div class="gold-bull-gif">
        <img src="@/assets/temporary-gold-bull.gif" alt="Gold Bull" class="gold-bull-gif" />
      </div>
    </div>
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
    this.loading = false;
    // Load images dynamically
    this.images = [
      require('@/assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg'),
      require('@/assets/marbleHOMEPAGE-zoom-0.jpg')
    ];

    // Set the initial background image
    this.currentImage = this.images[0];

    // Scroll event listener for background change
    window.addEventListener('scroll', () => {
      const scrollPosition = window.scrollY;
      const viewportHeight = window.innerHeight;

      if (scrollPosition < 1860) {
        const imageIndex = Math.floor(scrollPosition / viewportHeight) % this.images.length;
        this.currentImage = this.images[imageIndex];
      }
    });
  },
  methods: {
    // AIPR page
    navigateToAIPR() {
      this.$router.push('/AIPR');
    },

    // Learning page
    navigateToLearning() {
      this.$router.push('/GSlearning');
    }
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
  height: 350vh; /* Ensure there's enough height for scrolling */
}

/* Fixed background style */
.zoom-background {
  position: fixed;
  margin-top: 9.5vh; /* Leave space for the navbar */
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1; /* Lowest z-index for the background */
  transition: background-image 1.5s;
}

/* Scrolling content (text) */
.scrolling-content {
  position: relative;
  z-index: 10; /* Lower than navbar, higher than background */
  padding-left: 2rem;
  padding-top: 15vh;
}

/* Spinner style */
.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: white;
}

/* Foresight Finance Logo styling */
.logo-container {
  margin-bottom: 2rem;
  position: relative;
}

#FFLogoHeader {
  color: white;
  font-size: 3rem;
  font-family: 'Trebuchet MS', sans-serif;
  text-align: left;
}

/* Motto container styling */
.motto-container {
  position: relative;
}

.motto-container h1 {
  color: white;
  font-size: 8rem;
  font-family: 'Trebuchet MS', sans-serif;
  text-align: left;
  max-width: 70vw;
  line-height: 1.2;
}

/* Bubble container styling */
.bubble-container {
  background-color: rgba(18, 29, 39, 0.8); /* Transparent navy blue */
  padding: 20px 40px;
  border-radius: 15px;
  max-width: 35vw;
  text-align: center;
  margin: auto;
  margin-top: 100px;
  margin-bottom: 55px;
}

.bubble-text {
  color: white;
  font-size: 2rem;
  font-family: 'Trebuchet MS', sans-serif;
}

/* SVG container */
.svg-container {
  background-color: rgba(32, 52, 68, 0.8); /* Same transparent navy blue as the bubble */
  padding: 10px;
  border-radius: 15px;
  max-width: 50vw;
  margin: 10px auto; /* Add some margin to space the image */
  text-align: center;
}

.candlestick-svg {
  width: 100%;
  height: auto;
  display: inline-block;
}

/* Discover button styling */
.button-container {
  margin-bottom: 30px;
  margin-top: 50px;
  text-align: center;
}

.discover-button {
  background-color: #f9c802;
  color: black;
  font-size: 1.5rem;
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  cursor: pointer;
  font-family: 'Trebuchet MS', sans-serif;
}

.discover-button:hover {
  background-color: #e1b702;
}

/* New bubbles container */
.new-bubble-container {
  margin-top: 30px; /* Adjust spacing above new bubbles */
  text-align: right; /* Align to the right */
  background-color: #e1b702; /* Transparent navy blue */
  padding: 20px 40px;
  border-radius: 15px;
  max-width: 35vw;
  margin: auto;
  margin-top: 480px;
  margin-bottom: -400px;
}

/* New bubble styling */
.new-bubble {
  background-color: #e1b702; /* Gold colour */
  padding: 15px 30px; /* Smaller padding */
  border-radius: 10px; /* Smaller border radius */
  max-width: 30vw; /* Smaller width */
  margin: 10px 0; /* Vertical spacing */
}

.new-bubble-text {
  color: black;
  font-size: 1.5rem; /* Smaller font size */
  font-family: 'Trebuchet MS', sans-serif;
}

/* Gold bull GIF styling */
.gold-bull-gif {
  width: 800px;  /* Adjust the size as needed */
  height: auto; /* Maintain aspect ratio */
  margin-right: 10px; /* Space between the GIF and text */
  margin-top: -250px;
  margin-bottom: 100px;
}

/* Add any customizations for smaller screens */
@media (max-width: 768px) {
  .motto-container h1 {
    font-size: 3rem;
  }

  .bubble-text {
    font-size: 1.5rem;
  }

  .candlestick-svg {
    width: 90vw;
  }

  .discover-button {
    font-size: 1.2rem;
    padding: 10px 20px;
  }
}
</style>
