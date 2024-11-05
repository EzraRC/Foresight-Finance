<template>
  <div v-if="!loading">
    <!-- Fixed Background Animation Layer -->
    <div 
      class="zoom-background" 
      :class="{ hidden: isFirstBufferHidden }" 
      :style="{ backgroundImage: `url(${firstBufferImage})` }">
    </div>
    <div 
      class="zoom-background" 
      :class="{ hidden: !isFirstBufferHidden }" 
      :style="{ backgroundImage: `url(${secondBufferImage})` }">
    </div>

    <!-- Scrolling Content Layer -->
    <div class="scroll-wrapper">
      <div class="centered-content" style="margin-top: 330px;">
        <!-- Heading with fade-out effect at scrollPosition > 30 -->
        <h1 
          class="scrolling-text" 
          :class="{ 'fade-out': scrollPosition > 30 }">
          An advanced way to get ahead of the ever-changing markets
        </h1>

        <!-- Button with fade-out effect at scrollPosition > 1900 -->
        <div class="button-container scrolling-text" style="margin-top: 1800px; margin-left: 600px;">
          <button 
            class="action-button" 
            @click="navigateToAIPR"
            :class="{ 'fade-out': scrollPosition > 1650 }">
            Discover patterns now!
          </button>
        </div>

        <div class="button-container scrolling-text" style="margin-top: 2000px; margin-bottom: 50px; margin-left: -1300px;">
          <button class="action-button" @click="navigateToLearning">Learn with us!</button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="spinner">
    <span>Loading...</span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
      firstBufferImage: '',
      secondBufferImage: '',
      isFirstBufferHidden: false,
      loading: true,
      lastUpdate: 0,
      scrollPosition: 0
    };
  },
  mounted() {
    this.loading = false;

    // Load images into the images array
    this.images = Array.from({ length: 999 }, (_, index) =>
      require(`@/assets/3d-models/homePage/${String(index + 2).padStart(4, '0')}.jpg`)
    );

    // Preload the images and set the initial buffer images
    this.preloadImages().then(() => {
      this.firstBufferImage = this.images[0];
      this.secondBufferImage = this.images[1];
    });

    // Set up the scroll event listener
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    preloadImages() {
      return Promise.all(
        this.images.map(image => {
          return new Promise(resolve => {
            const img = new Image();
            img.src = image;
            img.onload = resolve;
          });
        })
      );
    },
    handleScroll() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const maxScrollTop = 4000; // Define maximum scroll height
      const scrollFraction = scrollTop / maxScrollTop;
      const index = Math.min(this.images.length - 1, Math.floor(scrollFraction * this.images.length));

      this.scrollPosition = scrollTop;

      const nextImage = this.images[index];
      if (nextImage !== this.getCurrentBufferImage()) {
        this.swapBuffers(nextImage);
      }
    },
    swapBuffers(nextImage) {
      const img = new Image();
      img.src = nextImage;
      img.onload = () => {
        if (this.isFirstBufferHidden) {
          this.firstBufferImage = nextImage;
        } else {
          this.secondBufferImage = nextImage;
        }
        this.isFirstBufferHidden = !this.isFirstBufferHidden;
      };
    },
    getCurrentBufferImage() {
      return this.isFirstBufferHidden ? this.secondBufferImage : this.firstBufferImage;
    },
    navigateToAIPR() {
      this.$router.push('/AIPR');
    },
    navigateToLearning() {
      this.$router.push('/GSlearning');
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  overflow-y: scroll;
  overflow-x: hidden;
}

.scroll-wrapper {
  height: 4000px; /* Fixed scroll height */
}

.zoom-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: #203444;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.zoom-background.hidden {
  opacity: 0;
}

.centered-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  z-index: 10;
  position: relative;
  margin-top: 100px;
}

.centered-content h1 {
  color: white;
  font-size: 4rem;
  font-family: 'Trebuchet MS', sans-serif;
}

.description-text {
  color: white;
  font-size: 1.8rem;
  font-family: 'Trebuchet MS', sans-serif;
  max-width: 70%;
  text-align: center;
}

.button-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 100px;
}

.action-button {
  background-color: #f9c802;
  color: black;
  font-size: 1.5rem;
  border: none;
  padding: 15px 30px;
  cursor: pointer;
  font-family: 'Trebuchet MS', sans-serif;
  width: 300px;
  text-align: center;
}

.action-button:hover {
  background-color: #e1b702;
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: white;
}

/* Custom fade-out effect */
.fade-out {
  opacity: 0;
  transition: opacity 0.5s ease;
}

@media (max-width: 768px) {
  .centered-content h1 {
    font-size: 2.5rem;
  }

  .description-text {
    font-size: 1.2rem;
  }

  .action-button {
    font-size: 1.2rem;
    padding: 10px 20px;
  }
}
</style>
