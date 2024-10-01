<template>
  <div class="marble-background">
    <div class="split left">
      <div class="centered">
        <MultiSeriesPieChart />
      </div>
    </div>
    <div class="split right">
      <div class="accordion-container">
        <!-- Beginner Lessons Accordion -->
        <button class="accordion">Beginner Lessons</button>
        <div class="panel">
          <div v-for="lesson in beginnerLessons" :key="lesson.id">
            <p>Lesson {{ lesson.ID }}: 
              <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID }}">{{ lesson.title }}</router-link>
            </p>
          </div>
        </div>

        <!-- Intermediate Lessons Accordion -->
        <button class="accordion">Intermediate Lessons</button>
        <div class="panel">
          <div v-for="lesson in intermediateLessons" :key="lesson.id">
            <p>Lesson {{ lesson.ID }}: 
              <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID }}">{{ lesson.title }}</router-link>
            </p>
          </div>
        </div>

        <!-- Expert Lessons Accordion -->
        <button class="accordion">Expert Lessons</button>
        <div class="panel">
          <div v-for="lesson in expertLessons" :key="lesson.id">
            <p>Lesson {{ lesson.ID }}: 
              <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID }}">{{ lesson.title }}</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MultiSeriesPieChart from '@/components/MultiSeriesPieChart.vue';
import { collection, getDocs } from "firebase/firestore";
import { db } from '@/firebase';

export default {
  name: 'GoldStandardLearningView',
  components: {
    MultiSeriesPieChart,
  },
  data() {
    return {
      beginnerLessons: [],
      intermediateLessons: [],
      expertLessons: [],
    };
  },
  async mounted() {
    try {
      // Fetch lessons collection from Firebase
      const lessonsCollection = collection(db, 'lessons');
      const lessonSnapshot = await getDocs(lessonsCollection);

      // Organize lessons by levelNeeded
      const lessons = lessonSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      this.beginnerLessons = lessons.filter(lesson => lesson.levelNeeded === 1);
      this.intermediateLessons = lessons.filter(lesson => lesson.levelNeeded === 2);
      this.expertLessons = lessons.filter(lesson => lesson.levelNeeded === 3);

      console.log("Beginner Lessons:", this.beginnerLessons);
      console.log("Intermediate Lessons:", this.intermediateLessons);
      console.log("Expert Lessons:", this.expertLessons);
    } catch (error) {
      console.error("Error fetching lessons:", error);
    }

    // Accordion functionality
    var acc = document.getElementsByClassName("accordion");
    for (let i = 0; i < acc.length; i++) {
      acc[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        panel.style.display = panel.style.display === "block" ? "none" : "block";
        panel.style.maxHeight = panel.style.maxHeight ? null : panel.scrollHeight + "px";
      });
    }
  }
};
</script>

<style>
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
  display: flex;
  justify-content: center;
}

/* If you want the content centered horizontally and vertically */
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  
}


/* Accordion container */
.accordion-container {
  
  padding-top: 35vh;
  width: 50%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  min-width: 400px;
}

/* Accordion button styling */
.accordion {
  background-color: #444;
  color: #eee;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  text-align: left;
  border: none;
  outline: none;
  transition: background-color 0.4s ease;
  margin: 0;
  border-bottom: 1px solid #555;
  box-sizing: border-box;
  font-size: 1.2rem;
}

.panel {
  background-color: darkslategrey;
  overflow: hidden;
  padding: 0 18px;
  display: none;
  box-sizing: border-box;
  transition: max-height 0.4s ease;
  cursor: default;
}

.accordion:after {
  content: '\02795';
  font-size: 13px;
  color: #777;
  float: right;
  margin-left: 5px;
}

.active:after {
  content: "\2796";
}
</style>
