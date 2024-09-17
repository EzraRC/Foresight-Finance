<template>
    <nav class="navbar">
      <div class="FFLogo">
        <router-link to="/">Foresight Finance</router-link>
      </div>
      <ul class="links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/AIPR">AI Pattern Recognizer</router-link></li>
        <li><router-link to="/GSlearning">Gold Standard Learning</router-link></li>
      </ul>
      <div v-if="isAuthenticated" class="greeting">
        {{ greetingMessage }} {{ username }}
      </div>
      <router-link
        class="login_btn"
        :to="isAuthenticated ? '/' : '/LoginSignUp'"
        @click="isAuthenticated ? logout() : null"
      >
        {{ isAuthenticated ? 'Logout' : 'Login' }}
      </router-link>
      <div class="toggle_btn">
        <i class="fa-solid fa-bars"></i>
      </div>
    </nav>
    <div class="dropdown_menu">
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/AIPR">AI Pattern Recognizer</router-link></li>
      <li><router-link to="/GSlearning">Gold Standard Learning</router-link></li>
      <li>
        <router-link
          class="login_btn"
          :to="isAuthenticated ? '/' : '/LoginSignUp'"
          @click="isAuthenticated ? logout() : null"
        >
          {{ isAuthenticated ? 'Logout' : 'Login' }}
        </router-link>
      </li>
    </div>
  </template>
  
  <script>
  // Import Firebase Auth to track user authentication state and handle signout
  import { auth } from "../firebase.js";
  import { onAuthStateChanged, signOut } from "firebase/auth";
  
  export default {
    data() {
      return {
        isAuthenticated: false, // Tracks user authentication state
        username: '', // Stores the logged-in user's display name
        greetingMessage: '', // Stores the greeting message based on the time of day
      };
    },
    methods: {
      // Fetch the current time and set the greeting message
      setGreeting() {
        const hour = new Date().getHours();
        if (hour < 12) {
          this.greetingMessage = 'Good morning';
        } else if (hour < 18) {
          this.greetingMessage = 'Good afternoon';
        } else {
          this.greetingMessage = 'Good evening';
        }
      },
      // Sign out the user and redirect to the login page
      logout() {
        signOut(auth)
          .then(() => {
            this.isAuthenticated = false;
            this.$router.push('/LoginSignUp'); // Redirect to login page
          })
          .catch((error) => {
            console.error('Error signing out:', error);
          });
      }
    },
    mounted() {
      // Listen for authentication state changes
      onAuthStateChanged(auth, (user) => {
        if (user) {
          this.isAuthenticated = true;
          this.username = user.displayName || user.email; // Use display name or fallback to email
          this.setGreeting(); // Set greeting based on time of day
        } else {
          this.isAuthenticated = false;
        }
      });
  
      // Handle the toggle button for the dropdown menu
      const toggleBtn = document.querySelector('.toggle_btn');
      const toggleBtnIcon = document.querySelector('.toggle_btn i');
      const dropDownMenu = document.querySelector('.dropdown_menu');
  
      toggleBtn.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open');
        const isOpen = dropDownMenu.classList.contains('open');
        toggleBtnIcon.classList = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
      });
    }
  };
  </script>

<style>
li {
    list-style: none;
}

.links {
    display: flex;
    gap: 2rem;
}

.navbar {
    padding: 25px;
    background-color: #183243;
    position: fixed;
    width: 100%;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2vh;
    height: 90px;
    gap: 10rem;
}

.navbar a {
    font-weight: bold;
    color: #fff;
    text-decoration: none;
}

.navbar .toggle_btn {
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    display: none;
}

.login_btn {
    background-color: #e3b130;
    border: none;
    outline: none;
    color: black !important;
    padding: 0.5rem 1rem;
    text-align: center;
    text-decoration: none;
    border-radius: 18px;
    cursor: pointer;
}

.login_btn:hover {
    scale: 1.05;
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    border: none;
    outline: none;
    color: black;
    padding: 0.5rem 1rem;
    text-align: center;
    text-decoration: none;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 18px;
    animation: shine 3s infinite ease-in-out;
    background-size: 250%;
    background-position: left;
}

.login_btn.router-link-exact-active {
    scale: 1.05;
    color: black;
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    animation: shine 3s infinite ease-in-out;
    background-size: 250%;
    background-position: left;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 16px;
}

.links a:hover {
    font-weight: bold;
    text-decoration: none;
    text-align: center;
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s infinite ease-in-out;
    background-size: 200%;
    background-position: left;
}

.FFLogo {
    font-size: 1.5rem;
    text-transform: uppercase;
    line-height: 1;
    text-align: center;
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s infinite ease-in-out;
    background-size: 200%;
    background-position: left;
    margin: auto 1rem;
}

.links a.router-link-exact-active {
    /*Will have the actice nav bar links be animated gold when active */
    font-size: 1.5vw;
    text-transform: uppercase;
    line-height: 1;
    text-align: center;
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s infinite ease-in-out;
    background-size: 200%;
    background-position: left;
}

/*DROPDOWN */
.dropdown_menu {
    position: absolute;
    display: none;
    right: 2rem;
    top: 70px;
    width: 300px;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(15px);
    border-radius: 10px;
    overflow: hidden;
    transition: height .2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 1;
}

.dropdown_menu.open {
    height: 185px;
}

.dropdown_menu li {
    padding: 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.dropdown_menu li a {
    color: #fff;
    text-decoration: none;
}

.dropdown_menu li a:hover {
    color: #e3b130;
    text-decoration: none;
}

.dropdown_menu .login_btn {
    width: 100%;
    justify-content: center;
    display: flex;
}

/*Responsive design*/
@media (max-width: 992px) {

    .navbar .links,
    .navbar .login_btn {
        display: none;
    }

    .navbar .toggle_btn {
        display: block;
    }

    .dropdown_menu {
        display: block;
    }
}

@media (max-width: 576px) {

    .dropdown_menu {
        left: 2rem;
        width: unset;
    }
}

@keyframes shine {
    from {
        background-position: -10%;
    }

    to {
        background-position: 110%
    }

}

/*Greeting message*/
.greeting {
    text-transform: uppercase;
    text-align: center;
    background: white;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s infinite ease-in-out;
    background-size: 200%;
    background-position: left;
    margin-right: 1rem;
}

@keyframes shine {
    from {
        background-position: -10%;
    }

    to {
        background-position: 110%;
    }
}

</style>