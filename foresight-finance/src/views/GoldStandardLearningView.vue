<template>
  <div class="marble-background" v-if="loggedIn">
    <div class="split left">
      <div class="centered">
        <MultiSeriesPieChart @error="handleError" />
      </div>
    </div>
    <div class="split right">
      <div class="accordion-container" v-if="userExpLevel">
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
                <span v-if="isQuizPassed(lesson.ID)">✔️</span>
              </p>
            </div>
          </div>
        </div>
        <!-- Intermediate Lessons Accordion -->
        <button class="accordion" :class="{ locked: userExpLevel < 2 }" @click="toggleAccordion($event, 2)">
          Intermediate Lessons
        </button>
        <div v-if="userExpLevel < 2" class="tooltip-text">Complete the intermediate lessons to unlock this section!
        </div>
        <div class="panel">
          <div v-if="hasIntermediateLessons">
            <div v-for="lesson in intermediateLessons" :key="lesson.id">
              <p class="lesson-text">Lesson {{ lesson.ID }}:
                <router-link :to="{ name: 'LearningView', params: { lessonID: lesson.ID } }">
                  {{ lesson.title }}
                </router-link>
                <span v-if="isQuizPassed(lesson.ID)">✔️</span>
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
                <span v-if="isQuizPassed(lesson.ID)">✔️</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="not-authorized">
    <div class="not-authorized-container">
      <h1 class="animated-text">Error 403: Access Denied :(</h1>
      <p>You don’t have permission to access this page. <br><br>Please log in or create an account with us</p>
      <router-link to="/LogInSignUp">
        <button class="login-button">Go to Login</button>
      </router-link>
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
      userExpLevel: null, // User's experience level
      user: null, // User object
      loading: true, // To handle the loading state
      loggedIn: true,
      userProgression: []
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
        if (!user) {
          // If the user is not logged in, redirect to the login page
          this.loggedIn = false
          return; // Stop execution if not logged in
        }

        // Step 2: User is logged in, store user information
        this.user = user
        try {
          // Fetch the user's experience level from Firestore
          const userExpCollection = collection(db, 'users')
          const userQuery = query(userExpCollection, where("UID", "==", user.uid));
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

          this.fetchUserProgress(this.user.uid)

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
    async fetchUserProgress(uid) {
      const progressRef = collection(db, 'educationalProgress');
      const q = query(progressRef, where('uid', '==', uid));

      const querySnapshot = await getDocs(q);
      querySnapshot.forEach((doc) => {
        this.userProgression.push(doc.data().lessonId)
      });
    },
    isQuizPassed(lessonID) {
      return this.userProgression.includes(lessonID.toString())
    },
    handleError(err) {
      console.error("Error from MultiSeriesPieChart:", err);
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


/* Loading Screen Styles */
.not-authorized {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-image: url("../assets/educationPageBackground.png");
  background-color: rgba(24, 50, 67, 0.95);
  z-index: 3;
}

.not-authorized-container {
  background-color: rgba(24, 50, 67, 0.6);
  padding: 75px;
  text-align: center;
}

.not-authorized-container p {
  font-size: 1.2rem;
  margin-bottom: 20px;
  animation: fadeInSlideUp 1s ease-in-out;
  color: white;
  cursor: default;
}

.animated-text {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  animation: fadeInSlideUp 1s ease-in-out;
  color: white;

}



.login-button {
  background-color: #e3b030a6;
  border: none;
  outline: none;
  color: black !important;
  padding: 0.5rem 1rem;
  text-align: center;
  text-decoration: none;
  border-radius: 18px;
  cursor: pointer;
  scale: 1.5;
}

.login-button:hover {
  scale: 1.55;
  background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
  color: black;
  /* Ensure text stays black on hover */
  -webkit-text-fill-color: black;
  /* For WebKit browsers */
  animation: shine 2s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
}




/* Tooltip styling */
.tooltip-text {
  display: none;
  position: absolute;
  left: 0px;
  /* Position the tooltip to the left of the button */
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

.accordion.locked:hover+.tooltip-text {
  display: block;
  opacity: 1;
}
</style>
