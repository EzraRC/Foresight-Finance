<template>
    <div class="marble-background">
        <!-- Loading indicator -->
        <div v-if="this.isLoading" class="loading-indicator">
            <img :src="require('@/assets/3d-models/gif-animations/loading.gif')" alt="Loading..." />
        </div>

        <!-- Feedback GIF and text based on answer correctness -->
        <div v-if="showFeedback" class="answer-feedback">
            <h1 v-if="isAnswerCorrect" class="feedback-text correct">Correct</h1>
            <h1 v-if="!isAnswerCorrect" class="feedback-text incorrect">Incorrect</h1>
            <img v-if="isAnswerCorrect" src="../assets/3d-models/gif-animations/bull.gif" alt="Correct Answer" class="feedback-gif" />
            <img v-if="!isAnswerCorrect" src="../assets/3d-models/gif-animations/bear.gif" alt="Incorrect Answer" class="feedback-gif" />
            <button class="next-button" @click="proceedToNextQuestion">Next Question</button>
        </div>

        <!-- Left side of the screen -->
        <div class="split left">

            <!-- Displaying final score GIFs after quiz completion -->
            <div v-if="quizCompleted" class="final-score-gifs">
                <div v-if="quizCompleted && (finalScore / 100 >= this.lessonData.passingGrade)">
                    <img src="../assets/3d-models/gif-animations/bull.gif" alt="bull">
                </div>
                <div v-if="quizCompleted && (finalScore / 100 < this.lessonData.passingGrade)">
                    <img src="../assets/3d-models/gif-animations/bear.gif" alt="bear">
                </div>
            </div>
            
            <!-- Displaying the final score when all questions are answered -->
            <h3 v-if="quizData.length > 0 && !quizCompleted" class="question-number">
                Question {{ questionNumber }} of {{ totalNumberOfQuestions }}
            </h3>
            <br>
            <br>
            <h1 v-if="quizData.length > 0 && !quizCompleted" class="question-text">
                {{ quizData[questionNumber - 1].question }}
            </h1>

            <!-- Progress bar -->
            <div v-if="quizData.length > 0 && !quizCompleted" class="progress-bar">
                <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
            </div>
        </div>

        <!-- Right side of the screen -->
        <div class="split right">
            <div v-if="quizCompleted">
                <h1 class="final-score">Your Final Score: {{ finalScore }}%</h1>
                <p class="final-score-reminder">If you did not pass the quiz, don't worry! We only keep your highest
                    passing score!</p>
            </div>
            <div v-if="!quizCompleted">
                <button v-for="(answer, index) in randomizedAnswers" :key="index" class="answer-button"
                    @click="submitAnswer(answer)">
                    <span class="label">{{ ['A', 'B', 'C', 'D'][index] }}</span> {{ answer }}
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { query, collection, getDocs, orderBy, getDoc, doc, where, setDoc } from "firebase/firestore";
import { db } from '@/firebase';
import { getAuth } from "firebase/auth";

export default {
    name: 'QuizView',
    data() {
        return {
            isLoading: true,
            lessonId: this.$route.params.lessonID,
            questionNumber: 1,
            quizCompleted: false,
            totalNumberOfQuestions: null,
            score: 0,
            quizData: [],
            randomizedAnswers: [],
            lessonData: [],
            isAnswerCorrect: null,
            showFeedback: false,
        };
    },
    async created() {
        await this.getQuizData();
    },
    computed: {
        progressPercentage() {
            if (!this.totalNumberOfQuestions) return 0;
            return (this.questionNumber / this.totalNumberOfQuestions) * 100;
        },
        finalScore() {
            // Calculate the score percentage (if quiz is completed)
            return this.quizCompleted ? ((this.score / this.totalNumberOfQuestions) * 100).toFixed(2) : 0;
        },
    },
    methods:
    {
        async getQuizData() {
            try {
                console.log("Route Parameter (lessonId):", this.lessonId);

                // Reference to the lesson document
                const lessonRef = doc(db, "lessons", this.lessonId);
                const lessonDoc = await getDoc(lessonRef);
                if (lessonDoc.exists()) {
                    this.lessonData = lessonDoc.data();
                } else {
                    console.error('No such document!');
                }
                console.log(this.lessonData.passingGrade)


                // Reference to the quiz subcollection within the lesson document
                const quizRef = collection(lessonRef, "quiz");

                // Fetch the quiz subcollection documents
                const quizSnapshot = await getDocs(quizRef);

                // Log each document in the quiz subcollection
                // quizSnapshot.forEach(doc => {
                //     console.log("Quiz Document ID:", doc.id);
                //     console.log("Quiz Document Data:", doc.data());
                // });

                // Map through the snapshot to retrieve data and store it in quizData
                this.quizData = quizSnapshot.docs
                    .map(doc => ({
                        id: doc.id,
                        ...doc.data()
                    }))
                    .sort((a, b) => a.order - b.order);  // Sort by 'order' field

                this.isLoading = false
                console.log("Complete Quiz Data Array:", this.quizData);
                console.log(this.quizData[0])
                //First question is loaded
                // Initialize question number and total questions only if quizData is not empty
                if (this.quizData.length > 0) {
                    this.questionNumber = 1;
                    this.totalNumberOfQuestions = this.quizData.length;
                    this.randomizeIncorrectAnswers();
                }
            } catch (error) {
                console.error("Error retrieving quiz data:", error);
            }
        },

        async submitAnswer(selectedAnswer) {
            const currentQuestion = this.quizData[this.questionNumber - 1];

            // Check if the selected answer is correct
            if (selectedAnswer === currentQuestion.correctAnswer) {
                this.score += 1;
                this.isAnswerCorrect = true;
                this.showFeedback = true;
            }
            else {
                this.isAnswerCorrect = false;
                this.showFeedback = true;
            }

            // Move to the next question or end the quiz
            if (this.questionNumber < this.totalNumberOfQuestions) {
                this.questionNumber++;
                this.randomizeIncorrectAnswers();
            } else {
                // Quiz is complete, calculate final score and check passing condition
                this.quizCompleted = true;
                const finalScore = (this.score / this.totalNumberOfQuestions) * 100;
                const userPassed = finalScore >= this.lessonData.passingGrade * 100;

                if (userPassed) {
                    const auth = getAuth();
                    const user = auth.currentUser;
                    if (!user) {
                        console.error("No user is logged in.");
                        return;
                    }

                    const uid = user.uid;

                    try {
                        // Reference to the user's quiz progress in the `educationalProgress` collection
                        const progressRef = doc(db, "educationalProgress", `${uid}_${this.lessonId}`);
                        const progressDoc = await getDoc(progressRef);

                        if (progressDoc.exists()) {
                            const existingScore = progressDoc.data().score;

                            // Update only if the new score is higher
                            if (finalScore > existingScore) {
                                await updateDoc(progressRef, {
                                    score: finalScore,
                                    completedAt: new Date()
                                });
                                console.log("Score updated to new high score:", finalScore);
                            } else {
                                console.log("Existing score is higher; no update made.");
                            }
                        } else {
                            // If no previous progress exists, create a new document
                            await setDoc(progressRef, {
                                uid: uid,
                                lessonId: this.lessonId,
                                score: finalScore,
                                completedAt: new Date()
                            });
                            console.log("New quiz progress created for user:", finalScore);
                        }
                    } catch (error) {
                        console.error("Error updating quiz progress:", error);
                    }
                }
            }
        },

        proceedToNextQuestion() {
            this.isAnswerCorrect = null;
            this.showFeedback = false;
        },

        randomizeIncorrectAnswers() {
            const currentQuestion = this.quizData[this.questionNumber - 1];

            // Randomly select three incorrect answers
            const incorrectAnswers = [...currentQuestion.incorrectAnswers];
            const selectedIncorrectAnswers = [];
            while (selectedIncorrectAnswers.length < 3 && incorrectAnswers.length > 0) {
                const randomIndex = Math.floor(Math.random() * incorrectAnswers.length);
                selectedIncorrectAnswers.push(incorrectAnswers.splice(randomIndex, 1)[0]);
            }

            // Combine the correct answer with the selected incorrect answers
            const allAnswers = [currentQuestion.correctAnswer, ...selectedIncorrectAnswers];

            // Shuffle the combined answers
            this.randomizedAnswers = allAnswers
                .map(value => ({ value, sort: Math.random() }))
                .sort((a, b) => a.sort - b.sort)
                .map(({ value }) => value);
        },
    },
    async mounted() {

    },
}
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
    background-image: url("../assets/marbleBackgroundNavyBlueTint.png");
}

.marble-background::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}

.final-score {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* Take the full height of the parent */
    width: 69%;
    /* Take the full width of the parent */
    color: #fff;
    font-size: 36px;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 10px;
}

.final-score-reminder {
    color: #fff;
}

.final-score-gifs {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90%;
    /* Take the full height of the parent */
    width: 100%;
    /* Take the full width of the parent */
    color: #fff;
    font-size: 36px;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
}

.feedback-text {
    color: #fff;
    text-align: center;
    font-size: 48px;
    margin-bottom: 20px;
    animation: fadeIn 0.5s ease-in-out;
    margin-left: 750px;
    margin-top: -100px;
}

.correct {
    color: #4caf50; /* Green color for correct answers */
}

.incorrect {
    color: #f44336; /* Red color for incorrect answers */
}

.split {
    z-index: 1;
    /* Make sure the content sits above the overlay */
    height: 75%;
    width: 50%;
    position: fixed;
    padding-top: 20px;
    overflow-x: hidden;
    padding-bottom: 50px;
    overflow-y: hidden;
}

/* Control the left side */
.left {
    left: 0;
    padding-left: 60px;
}

/* Control the right side */
.right {
    right: 0;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

/* If you want the content centered horizontally and vertically */
.centered {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;

}

.question-number {
    color: #e3b130;
}

.question-text {
    color: rgb(255, 255, 255);
    text-align: left;
}


.answer-button {
    width: 80%;
    padding: 20px;
    font-size: 24px;
    color: black;
    background-color: #aeaeae;
    border: none;
    border-radius: 8px;
    margin: 15px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    position: relative;
    overflow: hidden;
    text-align: left;
}

.answer-button:hover {
    background-color: #e3b130;
    transform: scale(1.02);
}

.answer-button .label {
    width: 40px;
    height: 40px;
    background-color: #fff;
    color: #02355A;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    margin-right: 20px;
    font-size: 20px;
}
.feedback-gif {
    margin-right: 800px;
    scale: 2.0;
}

.answer-feedback {
    position: relative;
    width: 100%;
    height: 100%;
    background-image: url('@/assets/marbleBackgroundNavyBlueTint.png');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border-radius: 10px;
    z-index: 1000;
}

.answer-feedback img {
    max-width: 500px;
    height: auto;
}

.next-button {
    margin-top: 20px;
    margin-left: 750px;
    padding: 12px 24px;
    background-color: #e3b130;
    border: none;
    border-radius: 8px;
    font-size: 18px;
    color: black;
    cursor: pointer;
    transition: background-color 0.3s;
}

.next-button:hover {
    background-color: #ffb347;
}

/*Progress Bar */
.progress-bar {
    width: 40%;
    height: 20px;
    background-color: lightgray;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
    margin-top: 400px;
    position: fixed;
}

.progress {
    height: 100%;
    background-color: rgba(236, 172, 32, 1);
    width: 0%;
    /* Initial width */
    transition: width 0.3s ease;
    /* Smooth transition */
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
    z-index: 2;
    min-height: 100%;
    min-width: 100%;
    background-color: #02355A;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>