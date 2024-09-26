<template>
    <!-- Show the loading screen when the page is not yet loaded -->
    <div v-if="isLoading" class="loading-screen">
        <h1>Loading...</h1>
        <p>Please wait while we load the content.</p>
    </div>

    <!-- Show the actual content after loading is done -->
    <div v-else-if="isAuthorized" class="marble-background">
        <div class="content-container">
            <h1 class="video-title">Lesson {{ lessonTitle }}</h1>
            <div class="iframe-container">
                <div v-html="videoUrl"></div> <!-- This will insert the iframe dynamically -->
            </div>
        </div>
    </div>

    <!-- Show "Not Authorized" page if user is not logged in -->
    <div v-else class="not-auth">
        <h1>Not Authorized</h1>
        <p>Please log in to access this page.</p>
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
    margin-top: -20vh;
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
.not-auth {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    color: #333;
}

.not-auth h1 {
    font-size: 32px;
    margin-bottom: 20px;
}

.not-auth p {
    font-size: 18px;
}
</style>
