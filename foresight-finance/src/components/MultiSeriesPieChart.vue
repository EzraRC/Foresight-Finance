<template>
    <div class="chart-background">
        <PieChart v-if="chartData && chartData.labels.length" :chartData="chartData" :options="options" />
    </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { db } from '@/firebase'; // Import your Firestore database instance
import { collection, query, where, getDocs } from 'firebase/firestore';
import { getAuth } from 'firebase/auth'; // Import Firebase Auth to get current user

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
    name: 'MultiSeriesPieChart',
    components: {
        PieChart: Pie,
    },
    data() {
        return {
            chartData: {
                labels: [
                    'Beginner Lessons Completed %',
                    'Beginner Lessons Remaining %',
                    'Intermediate Lessons Completed %',
                    'Intermediate Lessons Remaining %',
                    'Expert Lessons Completed %',
                    'Expert Lessons Remaining %',
                ],
                datasets: [
                    {
                        label: 'User Progress',
                        backgroundColor: ['#4BC0C0', '#D3D3D3', '#36A2EB', '#D3D3D3', '#FF6384', '#D3D3D3'],
                        data: [0, 100, 0, 100, 0, 100], // Start with 0 completed and 100 remaining for each category
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const value = context.raw;
                                return `${context.label}: ${value}% completed`;
                            },
                        },
                    },
                },
            },
        };
    },

    async created() {
        const auth = getAuth();

        // Use Firebase Auth's listener to detect auth state change
        auth.onAuthStateChanged(async (user) => {
            if (user) {
                // User is authenticated, proceed with fetching data
                await this.fetchUserProgress(user.uid);
            } else {
                // User not authenticated, handle accordingly (e.g., redirect or show a message)
                console.warn("User not authenticated");
            }
        });
    },
    methods: {
        async fetchUserProgress() {
            const auth = getAuth();
            const user = auth.currentUser;

            if (user) {
                const uid = user.uid;
                const progressRef = collection(db, 'educationalProgress');
                const q = query(progressRef, where('uid', '==', uid));

                let beginnerCount = 0;
                let intermediateCount = 0;
                let expertCount = 0;

                const querySnapshot = await getDocs(q);
                querySnapshot.forEach((doc) => {
                    const lessonId = doc.data().lessonId;
                    if (lessonId >= 1 && lessonId <= 8) {
                        beginnerCount++;
                    } else if (lessonId >= 9 && lessonId <= 16) {
                        intermediateCount++;
                    } else if (lessonId >= 17 && lessonId <= 24) {
                        expertCount++;
                    }
                });

                // Calculate completed and remaining percentages
                const totalLessonsPerCategory = 8;
                const beginnerPercentage = (beginnerCount / totalLessonsPerCategory) * 100;
                const intermediatePercentage = (intermediateCount / totalLessonsPerCategory) * 100;
                const expertPercentage = (expertCount / totalLessonsPerCategory) * 100;

                const beginnerRemaining = 100 - beginnerPercentage;
                const intermediateRemaining = 100 - intermediatePercentage;
                const expertRemaining = 100 - expertPercentage;

                // Update chart data with both completed and remaining values
                this.chartData.datasets[0].data = [
                    beginnerPercentage, beginnerRemaining,
                    intermediatePercentage, intermediateRemaining,
                    expertPercentage, expertRemaining,
                ];
            }
        },
    },
};
</script>

<style scoped>
.chart-background {
    background-color: rgba(255, 255, 255, 0.75);
    border-radius: 1rem;
    padding-bottom: 25px;
}
</style>
