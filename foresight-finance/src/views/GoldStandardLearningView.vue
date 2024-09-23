<template>
  <div class="marble-background">
    <div class="split left">
      <div class="centered">
        <MultiSeriesPieChart />
      </div>
    </div>
    <div class="split right">
      <!-- Other content for the right side -->
    </div>
  </div>
</template>

<script>
import MultiSeriesPieChart from '@/components/MultiSeriesPieChart.vue';

export default {
  name: 'GoldStandardLearningView',
  components: {
    MultiSeriesPieChart,
  },
};
</script>

<style>
body{
  height: 100vh;
}

.marble-background{
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
  background-image: url("../assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg");
}

/* Split the screen in half */
.split {
  height: 100%;
  width: 50%;
  position: fixed;
  z-index: 1;
  top: 10;
  overflow-x: hidden;
  padding-top: 20px;
}

/* Control the left side */
.left {
  left: 0;
}

/* Control the right side */
.right {
  right: 0;
}

/* If you want the content centered horizontally and vertically */
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

/* Style the image inside the centered container, if needed */
.centered img {
  width: 150px;
  border-radius: 50%;
}
</style>