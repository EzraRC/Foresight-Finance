<template>
  <div class="zoom-background">
    <h2 id="FFLogoHeader">Foresight Finance</h2>

  </div>
</template>

<script>
window.addEventListener('DOMContentLoaded', () => {
  //will run scripts on zoom background
  let box = document.querySelector(".zoom-background");
  let images = [require('@/assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg'), require('@/assets/marbleHOMEPAGE-zoom-0.jpg')]
  //^^list of images
  window.addEventListener('scroll', () => {
    let scrollPosition = window.scrollY;
    
    let viewportHeight = window.innerHeight;
    let imageIndex = Math.floor(scrollPosition / viewportHeight % images.length);
    box.style.backgroundImage = `url(${images[imageIndex]})`;
  })

})

export default {
  name: 'HomeView',
  components: {

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
  height: 600vh;
}

.zoom-background {
  position: fixed;
  margin-top: 9vh;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: url(../assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background-image 1.5s;
}

#FFLogoHeader {
  color: white;
}
</style>
