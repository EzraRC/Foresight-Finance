<template>
  <div class="marble-background">
    <div class="auth-container">
      <!-- If the user is authenticated, show the welcome message and logout button -->
      <div v-if="user">
        <h2>Welcome, {{ user.displayName || user.username }}!</h2>
        <router-link to="/AIPR"><button class="">AI Pattern Recognizer</button></router-link>
        <router-link to="/GSlearning"><button class="">Gold Standard Learning</button></router-link>
      </div>

      <!-- If the user is not authenticated -->
      <form v-else @submit.prevent="handleSubmit">
        <div v-if="isSignUpMode">
          <input v-model="username" type="text" placeholder="Username" />
          <input v-model="email" type="email" placeholder="Email" />
          <input v-model="password" type="password" placeholder="Password" />
          <button @click="signUp">Sign Up</button>
          <p @click="switchMode">Already have an account? Click here</p>
        </div>

        <div v-else>
          <input v-model="email" type="text" placeholder="Email" />
          <input v-model="password" type="password" placeholder="Password" />
          <button @click="login">Login</button>
          <p @click="switchMode">Don't have an account? Click here</p>
        </div>
        <div class="auth-message">{{ message }}</div>
      </form>
    </div>
    <!-- Modal Popup for Level Selection -->
    <div v-if="showLevelModal" class="modal-overlay">
      <div class="modal">
        <h3>Select Your Level</h3>
        <button @click="selectLevel('1')">Beginner</button>
        <button @click="selectLevel('2')">Intermediate</button>
        <button @click="selectLevel('3')">Expert</button>
        <button @click="signUp" :disabled="!selectedLevel">Create Account</button>
      </div>
    </div>
  </div>
</template>

<script>
// Import Firebase Auth from firebase.js
import { auth } from "../firebase.js";
import { getAuth, updateProfile } from "firebase/auth";
import { query, collection, getDocs, orderBy, doc, addDoc } from "firebase/firestore";
import { db } from '@/firebase';

import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from "firebase/auth";

export default {
  name: "LogInSignUpView",
  data() {
    return {
      email: "",
      password: "",
      username: "",
      message: "",
      user: null,  // New state to hold authenticated user
      isSignUpMode: false, // Tracks whether in signup mode
      showLevelModal: false,
      selectedLevel: null,
    };
  },
  mounted() {
    // Listen for authentication state changes
    onAuthStateChanged(auth, (user) => {
      if (user) {
        this.user = user; // If a user is logged in, set the user data
      } else {
        this.user = null; // If no user is logged in, reset the user data
      }
    });
  },
  methods: {
    // Switch between signup and login mode
    switchMode() {
      this.isSignUpMode = !this.isSignUpMode;
      this.message = ''; // Reset the message when switching modes
    },
    async addUserToFirestore(userCredential) {
      try {
        console.log("before add doc")
        const userDoc = await addDoc(collection(db, "users"), {
          expLevel: parseInt(this.selectedLevel),
          UID: userCredential.user.uid,
        });
        console.log("Document created successfully:", userDoc.id);
        return userDoc
      } catch (error) {
        console.error("Error adding document:", error);
        throw error; // Re-throw to be caught in signUp
      }
    },
    // Signup function
    async signUp() {
      if (!this.selectedLevel && (this.username && this.password && this.email)) {
        this.showLevelModal = true;
        this.message = 'Please select a level before creating your account.';
        this.selectedLevel = null;
        return;
      }

      try {
        // Create user with email and password
        const userCredential = await createUserWithEmailAndPassword(auth, this.email, this.password)
        console.log("User Credential:", userCredential);
        const updateAuth = getAuth();
        updateProfile(updateAuth.currentUser, {
          displayName: this.username
        }).then(() => {
          console.log("GOOD")
        }).catch((error) => {
          console.log("BAD")
        });

        // Prepare user data for Firestore
        const userData = {
          UID: userCredential.user.uid,
          expLevel: parseInt(this.selectedLevel) // Ensure expLevel is stored as a number
        };

        // Add user data to Firestore
        const userDoc = await addDoc(collection(db, "users"), userData);
        console.log("Document created successfully:", userDoc.id);

        // Display success message and close the modal
        this.message = `Welcome ${this.email}! Level selected: ${this.selectedLevel}`;
        this.showLevelModal = false; // Close modal on successful signup
        this.selectedLevel = null
      } catch (error) {
        console.error("Error during signup or Firestore operation:", error);
        this.message = `Firebase: ${error.message}`;
        this.showLevelModal = false; // Close modal on successful signup
      }
    },
    // Login function
    login() {
      if (!this.email || !this.password) {
        this.message = "Please fill in all fields.";
        return;
      }
      // Log the user in with email and password
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          this.message = `Welcome back ${this.email}!`;
        })
        .catch((error) => {
          this.message = `Firebase: ${error.message}`;
        });
    },
    selectLevel(level) {
      this.selectedLevel = level;
    },
    handleSubmit() {
      // Prevent default form submission
    },
  },
};
</script>

<style>
.marble-background {
  position: fixed;
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
  z-index: 1;
  /* Set a base z-index */
  background-image: url("../assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg");
}

.marble-background::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(2, 53, 90, 0.3);
  /* Navy blue with opacity */
  z-index: 0;
  /* Ensure the overlay is below the auth container */
}

.auth-container {
  position: relative;
  /* Make z-index effective */
  z-index: 2;
  /* Position above the marble background and its overlay */
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

input {
  display: block;
  margin: 10px 0;
  padding: 10px;
  width: 100%;
}

button {
  padding: 10px 20px;
  margin: 5px;
  cursor: pointer;
}

p {
  color: blue;
  cursor: pointer;
  margin-top: 10px;
}

.auth-message {
  color: red;
  margin-top: 10px;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3;
  /* Ensure the modal is above all other content */
}

.modal {
  position: relative;
  /* Optional: if you need to position modal content */
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin-bottom: 20px;
}

.modal button {
  margin: 10px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>
