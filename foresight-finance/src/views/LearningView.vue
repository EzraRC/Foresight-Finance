<template>
    <!-- Show the loading screen when the page is not yet loaded -->
    <div v-if="isLoading" class="loading-screen">
        <div class="loading-indicator">
            <img :src="require('@/assets/3d-models/gif-animations/loading.gif')" alt="Loading..." />
        </div>
    </div>

    <!-- Authorized Content -->
    <div v-else-if="isAuthorized">
        <div class="marble-background">
            <div class="content-container">
                <h1 class="video-title">Lesson {{ lessonTitle }}</h1>
                <div class="iframe-container">
                    <div id="youtube-player"></div> <!-- Player container -->
                    <div v-if="showTooltip" class="tooltip-container">
                        <span class="tooltip">Seeking is disabled for this video.</span>
                    </div>
                </div>

                <!-- Controls Section -->
                <div class="controls-container">
                    <button @click="goBack10Seconds" class="control-button">Go Back 10s</button>
                    <button @click="togglePause" class="control-button">
                        {{ isPaused ? "Play" : "Pause" }}
                    </button>
                </div>

                <div class="quizButton-container">
                    <router-link :to="{ name: 'QuizView', params: { lessonID: this.lessonID } }">
                        <button>Ready to take the quiz?</button>
                    </router-link>
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
            isLoading: true,
            lessonID: null,
            lessonTitle: "",
            videoId: "",
            player: null,
            validTime: [], // Tracks the valid playback range
            showTooltip: false, // Tooltip visibility for seeking attempts
            isPaused: false, // Track the pause state
        };
    },
    methods: {
        async checkAuthAndLoadData() {
            auth.onAuthStateChanged(async (user) => {
                if (user) {
                    this.isAuthorized = true;
                    try {
                        const lessonId = this.$route.params.lessonID || "1";
                        const lessonDocRef = doc(db, "lessons", lessonId);
                        const lessonDoc = await getDoc(lessonDocRef);

                        if (lessonDoc.exists()) {
                            const lessonData = lessonDoc.data();
                            this.lessonID = lessonData.ID;
                            this.lessonTitle = lessonData.title;
                            this.videoId = this.extractVideoId(lessonData.URL);
                            this.loadYouTubeAPI();
                        } else {
                            console.error("No such document!");
                        }
                    } catch (error) {
                        console.error("Error fetching lesson data:", error);
                    }
                } else {
                    this.isAuthorized = false;
                }
                this.isLoading = false;
            });
        },
        extractVideoId(url) {
            const regExp = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)/;
            const match = url.match(regExp);
            return match && match[1] ? match[1] : "";
        },
        loadYouTubeAPI() {
            const script = document.createElement("script");
            script.src = "https://www.youtube.com/iframe_api";
            document.body.appendChild(script);
            window.onYouTubeIframeAPIReady = this.initializeYouTubePlayer;
        },
        initializeYouTubePlayer() {
            this.player = new YT.Player("youtube-player", {
                height: "390",
                width: "640",
                videoId: this.videoId,
                playerVars: {
                    modestbranding: 1,
                    controls: 0, // Disable controls (we'll add custom controls)
                    disablekb: 1,
                    enablejsapi: 1, // Ensure API is enabled for further controls
                },
                events: {
                    onReady: this.onPlayerReady,
                    onStateChange: this.onPlayerStateChange,
                },
            });
        },
        onPlayerReady() {
            this.updateValidTime();
            this.player.playVideo();
            this.isPaused = false;
        },
        onPlayerStateChange(event) {
            if (event.data === YT.PlayerState.PAUSED) {
                this.isPaused = true;
            } else {
                this.isPaused = false;
            }
        },
        goBack10Seconds() {
            const currentTime = this.player.getCurrentTime();
            this.player.seekTo(currentTime - 10, true);
        },
        togglePause() {
            if (this.isPaused) {
                this.player.playVideo();
            } else {
                this.player.pauseVideo();
            }
        },
        updateValidTime() {
            setInterval(() => {
                if (this.player && this.player.getPlayerState() === YT.PlayerState.PLAYING) {
                    const currentTime = Math.floor(this.player.getCurrentTime());
                    if (!this.validTime.includes(currentTime)) {
                        this.validTime.push(currentTime);
                    }
                }
            }, 1000);
        },
    },

    mounted() {
        this.checkAuthAndLoadData();
    },
};
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
    background-image: url("../assets/marbleBackgroundNavyBlueTint.png");
    overflow-y: auto;
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
    margin-top: 280px;
    font-size: 24px;
    display: inline-block;
    text-align: center;
}

.iframe-container {
    margin-top: 20px;
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
    /* 16:9 aspect ratio */
    height: 80%;
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
    margin-top: 30px;
    /* Add space above the button */
    z-index: 1;
    /* Ensures the button appears above the background */
}

.quizButton-container button {
    background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
    text-transform: uppercase;
    line-height: 1;
    text-align: center;
    color: #000;
    animation: shine 3s infinite ease-in-out;
    background-size: 200%;
    background-position: left;

    margin-bottom: 30px;
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
    background-image: url("../assets/educationPageBackground.png");
    background-color: rgba(24, 50, 67, 0.95);
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

.tooltip-container {
    position: relative;
    display: inline-block;
    margin-top: 10px;
}

.tooltip {
    visibility: hidden;
    background-color: #555;
    color: white;
    text-align: center;
    padding: 5px;
    border-radius: 5px;
    position: absolute;
    z-index: 1;
    bottom: 100%;
    left: 50%;
    margin-left: -20px;
    opacity: 0;
    transition: opacity 0.3s;
    width: 180px;
}

.tooltip-container .tooltip {
    visibility: visible;
    opacity: 1;
}

.controls-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

.control-button {
    padding: 10px 20px;
    background-color: #e3b130;
    border: none;
    cursor: pointer;
    font-size: 16px;
    border-radius: 5px;
}

.control-button:hover {
    background-color: #c79a1f;
}

@keyframes shine {
    from {
        background-position: -10%;
    }

    to {
        background-position: 110%
    }

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
