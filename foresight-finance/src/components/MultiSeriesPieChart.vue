<template>
    <div>
      <!-- The Pie chart will only render if the data is available -->
      <PieChart
        v-if="chartData && chartData.labels.length"
        :chartData="chartData"
        :options="options"
      />
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
          labels: ['Red', 'Blue', 'Yellow', 'Green'], // Data labels
          datasets: [
            {
              label: 'Dataset 1',
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
              data: [300, 50, 100, 40], // First dataset values
            },
            {
              label: 'Dataset 2',
              backgroundColor: ['#FF9F40', '#9966FF', '#FFCD56', '#4BC0C0'],
              data: [100, 200, 150, 120], // Second dataset values
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
  </style>
  