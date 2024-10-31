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
        <h1>An advanced way to get ahead of the ever-changing markets</h1>
        <p class="description-text" style="margin-top: 400px;">
          Build and maximize your portfolio with AI-enhanced pattern recognition
        </p>
        <div class="button-container" style="margin-top: 700px; margin-left: 625px;">
          <button class="action-button" @click="navigateToAIPR">Discover patterns now!</button>
        </div>
        <p class="description-text" style="margin-top: 1000px;">
          We offer a variety of different lessons ranging from beginner topics to advanced technical patterns!
        </p>
        <div class="button-container" style="margin-top: 1000px; margin-bottom: 50px;">
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
    };
  },
  mounted() {
    this.loading = false;

    this.images = Array.from({ length: 249 }, (_, index) =>
      require(`@/assets/3d-models/homePage/${String(index + 2).padStart(4, '0')}.jpg`)
    );

    this.preloadImages().then(() => {
      this.firstBufferImage = this.images[0];
      this.secondBufferImage = this.images[1];
    });

    window.addEventListener('scroll', this.debouncedScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.debouncedScroll);
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
      const scrollTop = document.documentElement.scrollTop;
      const maxScrollTop = 3000; // Fixed scroll length in pixels
      const scrollFraction = scrollTop / maxScrollTop;
      const index = Math.min(this.images.length - 1, Math.floor(scrollFraction * this.images.length));

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
    debouncedScroll() {
      const now = Date.now();
      if (now - this.lastUpdate > 20) {
        this.handleScroll();
        this.lastUpdate = now;
      }
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
  height: 3000px; /* Fixed scroll height */
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
  opacity: 1;
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
