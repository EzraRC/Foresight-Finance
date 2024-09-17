<template>
  <div class="marble-background">
    <div class="auth-container">
      <!-- If the user is authenticated, show the welcome message and logout button -->
      <div v-if="user">
        <h2>Welcome, {{ user.email }}!</h2>
        <button @click="logout">Logout</button>
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
  </div>
</template>

<script>
// Import Firebase Auth from firebase.js
import { auth } from "../firebase.js";
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
  // Signup function
  signUp() {
    if (!this.email || !this.password || !this.username) {
      this.message = "Please fill in all fields.";
      return;
    }
    createUserWithEmailAndPassword(auth, this.email, this.password)
      .then((userCredential) => {
        this.message = `Welcome ${this.email}!`;
      })
      .catch((error) => {
        this.message = `Firebase: ${error.message}`;
      });
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
  // Logout function
  logout() {
    signOut(auth)
      .then(() => {
        this.message = "You have logged out.";
      })
      .catch((error) => {
        this.message = `Firebase: ${error.message}`;
      });
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

.auth-container {
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
</style>
