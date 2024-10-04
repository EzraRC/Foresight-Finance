<template>
    <div class="chart-background">
        <!-- The Pie chart will only render if the data is available -->
        <PieChart v-if="chartData && chartData.labels.length" :chartData="chartData" :options="options" />
    </div>
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

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
                labels: ['Beginner Lessons Completed', 'Intermediate Lessons Completed', 'Expert Lessons Completed'], // Data labels
                datasets: [
                    {
                        label: 'Dataset 1',
                        backgroundColor: ['#4BC0C0', '#36A2EB', '#FF6384'],
                        data: [300, 50, 100], // First dataset values
                    },
                    {
                        //inner circle
                        label: 'Dataset 2',
                        backgroundColor: ['rgba(255,255,255,0)', 'rgba(255,255,255,0)', 'rgba(255,255,255,0)'],
                        data: [0, 0, 0], // Second dataset values
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                },
            },
        };
    },
};
</script>

<style scoped>
/* Add custom styles if necessary */
.chart-background{
    background-color: rgba(255, 255, 255, 0.75);
    border-radius: 1rem;
    padding-bottom: 25px;
}
</style>