<template>
    <!-- Show the loading screen when the page is not yet loaded -->
    <div v-if="isLoading" class="loading-screen">
        <!-- Loading indicator -->
        <div v-if="isLoading" class="loading-indicator">
            <img :src="require('@/assets/3d-models/gif-animations/loading.gif')" alt="Loading..." />
        </div>
    </div>

    <!-- Show the actual content after loading is done -->
    <div v-else-if="isAuthorized">
        <div class="marble-background">
            <div class="content-container">
                <h1 class="video-title">Lesson {{ lessonTitle }}</h1>
                <div class="iframe-container">
                    <div v-html="videoUrl"></div> <!-- This will insert the iframe dynamically -->
                </div>
                <div class="quizButton-container">
                    <router-link :to="{ name: 'QuizView', params: { lessonID: this.lessonId } }"><button>Ready to take
                            the quiz?</button></router-link>
                </div>
            </div>
        </div>
    </div>

    <!-- Show "Not Authorized" page if user is not logged in -->
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
import { auth, db } from "../firebase";
import { doc, getDoc } from "firebase/firestore";

export default {
    name: 'LearningView',
    data() {
        return {
            isAuthorized: false,
            isLoading: true,  // New boolean flag to control loading state
            lessonID: null,
            lessonTitle: '',
            videoUrl: '',
        };
    },
    methods: {
        async checkAuthAndLoadData() {
            auth.onAuthStateChanged(async (user) => {
                if (user) {
                    // User is logged in, fetch the lesson data
                    this.isAuthorized = true;
                    try {
                        const lessonId = this.$route.params.lessonID || '1';

                        // Reference to the lesson document
                        const lessonDocRef = doc(db, 'lessons', lessonId);

                        // Fetch the lesson document
                        const lessonDoc = await getDoc(lessonDocRef);

                        if (lessonDoc.exists()) {
                            const lessonData = lessonDoc.data();
                            this.lessonID = lessonData.ID;
                            this.lessonTitle = lessonData.title;
                            this.videoUrl = lessonData.URL;
                        } else {
                            console.error('No such document!');
                        }
                    } catch (error) {
                        console.error("Error fetching lesson data:", error);
                    }
                } else {
                    // User is not logged in, show the not authorized page
                    this.isAuthorized = false;
                }

                // Data loading is done, set isLoading to false
                this.isLoading = false;
            });
        }
    },
    mounted() {
        this.checkAuthAndLoadData();
    }
}
</script>

<style>
body {
    height: 100vh;
    margin: 0;
}

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
    background-image: url("../assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg");
}

.content-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    max-width: 1200px;
    /* Max width of the content */
    max-height: 60vh;
    z-index: 1;
    width: 100%;
    height: 100%;
    padding: 20px;
    margin-top: -10vh;
}

.video-title {
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    margin-bottom: 20px;
    font-size: 24px;
    display: inline-block;
    text-align: center;
}

.iframe-container {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
    /* 16:9 aspect ratio */
    height: 0;
    max-width: 100%;
}

.iframe-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

h1 {
    text-align: center;
}

.quizButton-container {
    display: flex;
    justify-content: center;
    /* Centers the button horizontally */
    margin-top: 20px;
    /* Add space above the button */
    z-index: 1;
    /* Ensures the button appears above the background */
}

.quizButton-container button {
    background-color: #e3b130;
    padding: 10px 20px;
    /* Adjust padding as needed */
    font-size: 16px;
    /* Font size for the button */
    cursor: pointer;
    /* Show pointer cursor on hover */
}


/* Loading Screen Styles */
.loading-screen {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    color: #333;
}

.loading-screen h1 {
    font-size: 32px;
    margin-bottom: 20px;
}

.loading-screen p {
    font-size: 18px;
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
    background-image: url("../assets/marbleHOMEPAGE-zoom-0-50-Darker.jpg");
    z-index: 3;
}

.not-authorized-container {
    background-color: rgba(24, 50, 67, 0.95);
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
    background-color: #e3b130;
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


.loading-indicator {
  color: white;
  font-size: 40px;
  text-align: center;
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 70px;
  margin-bottom: -18px;
}

@keyframes fadeInSlideUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }

}

@keyframes shine {
    from {
        background-position: -20%;
    }

    to {
        background-position: 120%
    }

}
</style>
