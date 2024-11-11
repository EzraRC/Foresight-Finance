<template>
    <div class="marble-background">
        <!-- Loading indicator -->
        <div v-if="this.isLoading" class="loading-indicator">
            <img :src="require('@/assets/3d-models/gif-animations/loading.gif')" alt="Loading..." />
        </div>
        <div class="split left">
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

            <div v-if="quizData.length > 0 && !quizCompleted" class="progress-bar">
                <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
            </div>
        </div>
        <div class="split right">
            <div v-if="quizCompleted" class="final-score">
                <h1>Your Final Score: {{ finalScore }}%</h1>
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
import { query, collection, getDocs, orderBy, getDoc, doc } from "firebase/firestore";
import { db } from '@/firebase';

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

        submitAnswer(selectedAnswer) {
            const currentQuestion = this.quizData[this.questionNumber - 1];

            // Check if the selected answer is correct
            if (selectedAnswer === currentQuestion.correctAnswer) {
                this.score += 1;
            }

            // Move to the next question or end the quiz
            if (this.questionNumber < this.totalNumberOfQuestions) {
                this.questionNumber++;
                this.randomizeIncorrectAnswers(); // Shuffle answers for the next question
            } else {
                // Quiz is complete, show the final score
                this.quizCompleted = true;
            }
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
    background-color: rgba(2, 53, 90, 0.9);
    z-index: 0;
}

.final-score {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* Take the full height of the parent */
    width: 100%;
    /* Take the full width of the parent */
    color: #fff;
    font-size: 36px;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.6);
    padding: 20px;
    border-radius: 10px;
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

.split {
    z-index: 1;
    /* Make sure the content sits above the overlay */
    height: 75%;
    width: 50%;
    position: fixed;
    padding-top: 20px;
    overflow-x: hidden;
    padding-bottom: 50px;
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
    color: grey;
}

.question-text {
    color: lightgray;
    text-align: left;
}


.answer-button {
    width: 80%;
    padding: 20px;
    font-size: 24px;
    color: #fff;
    background-color: #6b6b6b;
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
    background-color: #026799;
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

/*Progress Bar */
.progress-bar {
    width: 90%;
    height: 20px;
    background-color: lightgray;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 20px;
    margin-top: 400px;
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
}
</style>