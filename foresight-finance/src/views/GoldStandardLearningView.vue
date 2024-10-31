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
          <div v-if="hasBeginnerLessons">
            <div v-for="lesson in beginnerLessons" :key="lesson.id">
              <p class="lesson-text">Lesson {{ lesson.ID }}:
                <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID } }">
                  {{ lesson.title }}
                </router-link>
              </p>
            </div>
          </div>
          <div v-else>
            <p class="lesson-text">Oops, sorry! These lessons are either locked. Please complete the intermediate
              lessons before moving on :)</p>
          </div>
        </div>

        <!-- Intermediate Lessons Accordion -->
        <button class="accordion">Intermediate Lessons</button>
        <div class="panel">
          <div v-if="hasIntermediateLessons">
            <div v-for="lesson in intermediateLessons" :key="lesson.id">
              <p class="lesson-text">Lesson {{ lesson.ID }}:
                <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID } }">
                  {{ lesson.title }}
                </router-link>
              </p>
            </div>
          </div>
          <div v-else>
            <p class="lesson-text">Oops, sorry! These lessons are either locked. Please complete the intermediate
              lessons before moving on :)</p>
          </div>
        </div>

        <!-- Expert Lessons Accordion -->
        <button class="accordion">Expert Lessons</button>
        <div class="panel">
          <div v-if="hasExpertLessons">
            <div v-for="lesson in expertLessons" :key="lesson.id">
              <p class="lesson-text">Lesson {{ lesson.ID }}:
                <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID } }">
                  {{ lesson.title }}
                </router-link>
              </p>
            </div>
          </div>
          <div v-else>
            <p class="lesson-text">Oops, sorry! These lessons are either locked. Please complete the intermediate
              lessons before moving on :)</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MultiSeriesPieChart from '@/components/MultiSeriesPieChart.vue';
import { query, collection, getDocs, orderBy } from "firebase/firestore";
import { db } from '@/firebase';

export default {
  name: 'GoldStandardLearningView',
  components: {
    MultiSeriesPieChart,
  },
  computed: {
    hasBeginnerLessons() {
      return this.beginnerLessons.length > 0;
    },
    hasIntermediateLessons() {
      return this.intermediateLessons.length > 0;
    },
    hasExpertLessons() {
      return this.expertLessons.length > 0;
    }
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
    const lessonsCollection = query(collection(db, 'lessons'), orderBy("ID"));
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
  const acc = document.getElementsByClassName("accordion");
  let activePanel = null; // Track the currently active panel

  for (let i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
      // Close any currently open panel
      if (activePanel && activePanel !== this.nextElementSibling) {
        activePanel.style.maxHeight = null;
        activePanel.previousElementSibling.classList.remove("active");
      }

      // Toggle the clicked panel
      this.classList.toggle("active");
      const panel = this.nextElementSibling;

      if (panel.style.maxHeight) {
        // If the panel is already open, close it
        panel.style.maxHeight = null;
        activePanel = null;
      } else {
        // If the panel is closed, open it and set maxHeight dynamically
        panel.style.maxHeight = panel.scrollHeight + "px";
        activePanel = panel; // Update the active panel
      }
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

.marble-background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(2, 53, 90, 0.9); /* Navy blue (#000080) with 60% opacity */
  z-index: 0; /* Make sure the overlay sits behind other content */
}

.split {
  z-index: 1; /* Make sure the content sits above the overlay */
  height: 100%;
  width: 50%;
  position: fixed;
  padding-top: 20px;
  overflow-x: hidden;
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

  padding-top: 25vh;
  width: 50%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  min-width: 400px;

}

/* Accordion button styling */
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
  transition: background-color 0.4s ease, color 0.4s ease;
  margin: 0;
  border-bottom: 1px solid #555;
  box-sizing: border-box;
  font-size: 1.2rem;
}

.accordion.active {
  background-color: #666;
  /* Change background color when active */
  color: white;
  /* Change text color when active */
}

/* The Panel (hidden by default, animated open and close) */
.panel {
  background-color: grey;
  overflow: hidden;
  padding: 0 18px;
  /* Initial padding */
  max-height: 0;
  /* Initial height of 0 for hidden state */
  transition: max-height 0.4s ease, padding 0.4s ease;
  /* Smooth animation */
  box-sizing: border-box;
  color: #eee;
  font-weight: bold;
}

/* Animation when the accordion is active (open state) */
.panel.active {
  background-color: #333;
  /* Change panel background when active */
  color: rgb(109, 109, 109);
  /* Change text color when the panel is open */
}

.lesson-text {
  color: #eee;
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
  /* Change icon to minus when active */
}
</style>
