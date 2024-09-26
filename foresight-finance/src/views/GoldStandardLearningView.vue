<template>
  <div class="marble-background">
    <div class="split left">
      <div class="centered">
        <MultiSeriesPieChart />
      </div>
    </div>
    <div class="split right">
      <!-- Other content for the right side -->
      <button class="accordion">Beginner Lessons</button>
      <div class="panel">
        <p>Lorem ipsum...</p>
      </div>

      <button class="accordion">Intermediate Lesson</button>
      <div class="panel">
        <p>Lorem ipsum...</p>
      </div>

      <button class="accordion">Expert Lessons</button>
      <div class="panel">
        <p>Lorem ipsum...</p>
      </div>
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
body {
  height: 100vh;
}

.marble-background {
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
  align-items: center;
}

/* Control the left side */
.left {
  left: 0;
}

/* Control the right side */
.right {
  justify-content: center;
  align-items: center;
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



/*Accordian styles */
/* Style the buttons that are used to open and close the accordion panel */
.accordion {
  background-color: #444;
  color: #eee;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  text-align: left;
  border: none;
  outline: none;
  transition: 0.4s;
}

/* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
.active,
.accordion:hover {
  background-color: #555;
}

/* Style the accordion panel. Note: hidden by default */
.panel {
  padding: 0 18px;
  background-color: darkslategrey;
  display: none;
  overflow: hidden;
}
</style>