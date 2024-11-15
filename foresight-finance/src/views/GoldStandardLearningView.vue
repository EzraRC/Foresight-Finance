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
        <button class="accordion" :class="{ locked: userExpLevel < 1 }" @click="toggleAccordion($event, 1)">
          Beginner Lessons
        </button>
        <div v-if="userExpLevel < 1" class="tooltip-text">Complete the beginner lessons to unlock this section!</div>
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
        </div>

        <!-- Intermediate Lessons Accordion -->
        <button class="accordion" :class="{ locked: userExpLevel < 2 }" @click="toggleAccordion($event, 2)">
          Intermediate Lessons
        </button>
        <div v-if="userExpLevel < 2" class="tooltip-text">Complete the intermediate lessons to unlock this section!</div>
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
        </div>

        <!-- Expert Lessons Accordion -->
        <button class="accordion" :class="{ locked: userExpLevel < 3 }" @click="toggleAccordion($event, 3)">
          Expert Lessons
        </button>
        <div v-if="userExpLevel < 3" class="tooltip-text">Complete the expert lessons to unlock this section!</div>
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
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import MultiSeriesPieChart from '@/components/MultiSeriesPieChart.vue';
import { query, collection, getDocs, orderBy, where } from "firebase/firestore";
import { db } from '@/firebase';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useRouter } from 'vue-router';

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
      userExpLevel: 0, // User's experience level
      user: null, // User object
      loading: true, // To handle the loading state
    };
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
    },
  },
  mounted() {
    // Call the method to check user and fetch data
    this.fetchUserAndLessons();
  },
  methods: {
    async fetchUserAndLessons() {
      const auth = getAuth();
      const router = useRouter();

      // Step 1: Check if user is authenticated first
      onAuthStateChanged(auth, async (user) => {
        console.log(user)
        if (!user) {
          // If the user is not logged in, redirect to the login page
          router.push({ name: 'Login' });
          return; // Stop execution if not logged in
        }

        // Step 2: User is logged in, store user information
        this.user = user;

        try {
          // Fetch the user's experience level from Firestore
          const userQuery = query(collection(db, 'users'), where("UID", "==", user.uid));
          const userQuerySnapshot = await getDocs(userQuery);

          // Step 3: Check if the query found any document
          if (!userQuerySnapshot.empty) {
            const userDoc = userQuerySnapshot.docs[0]; // Get the first matching document
            this.userExpLevel = userDoc.data().expLevel || 1; // Default to level 1 if no data
          } else {
            console.log('User document not found');
            // Handle the case where the document doesn't exist, maybe create one
          }
          // Step 4: After verifying the user, fetch lessons
          const lessonsCollection = query(collection(db, 'lessons'), orderBy("ID"));
          const lessonSnapshot = await getDocs(lessonsCollection);

          const lessons = lessonSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
          this.beginnerLessons = lessons.filter(lesson => lesson.levelNeeded === 1);
          this.intermediateLessons = lessons.filter(lesson => lesson.levelNeeded === 2);
          this.expertLessons = lessons.filter(lesson => lesson.levelNeeded === 3);

        } catch (error) {
          console.error("Error fetching data:", error);
        } finally {
          // Step 5: Set loading to false after all data is fetched
          this.loading = false;
        }
      });
    },
    toggleAccordion(event, requiredLevel) {
      if (this.userExpLevel < requiredLevel) {
        return; // Do nothing if the user lacks the required experience level
      }

      const button = event.target;
      const panel = button.nextElementSibling;

      button.classList.toggle('active');
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    },
  },
};
</script>


<style scoped>
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
  background-image: url("../assets/educationPageBackgroundEDITED.png");
  background-color: #183243;
}

.split {
  z-index: 1;
  /* Make sure the content sits above the overlay */
  height: 100%;
  width: 50%;
  position: fixed;
  padding-top: 20px;
  overflow-x: hidden;
  margin-bottom: 200px;
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
  align-items: center;
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
  width: 120%;
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
  background-color: #654f16;
  /* Change background color when active */
  color: white;
  /* Change text color when active */
}

/* The Panel (hidden by default, animated open and close) */
.panel {
  background-color: #e3b130;
  overflow: hidden;
  padding: 0 18px;
  /* Initial padding */
  max-height: 0;
  width: 120%;
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
  color: #e3b130;
  /* Change text color when the panel is open */
}

.lesson-text {
  color: #000000;
  margin-top: 15px;
  margin-bottom: 15px;
}

.accordion:after {
  content: '\02795';
  font-size: 13px;
  color: #000000;
  float: right;
  margin-left: 5px;
}

.active:after {
  content: "\2796";
  /* Change icon to minus when active */
}



/* Tooltip styling */
.tooltip-text {
  display: none;
  position: absolute;
  left: 0px; /* Position the tooltip to the left of the button */
  top: 50%;
  transform: translateY(-50%);
  background-color: #333;
  color: white;
  padding: 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  max-width: 200px;
  box-sizing: border-box;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.accordion.locked:hover + .tooltip-text {
  display: block;
  opacity: 1;
}
</style>
