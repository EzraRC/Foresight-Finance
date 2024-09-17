<template>
  <div>
    <h1>Candlestick Chart</h1>
    <img :src="chartUrl" alt="Candlestick Chart" />
  </div>
</template>

<script>
export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      chartUrl: this.getChartUrl(),  // Initialize with the current timestamp
    };
  },
  mounted() {
    // Automatically refresh the chart every 5 seconds
    setInterval(() => {
      this.chartUrl = this.getChartUrl();  // Update the image URL to force a refresh
    }, 5000);  // Refresh every 5000ms (5 seconds)
  },
  methods: {
    getChartUrl() {
      // Add a timestamp to prevent browser caching
      return `http://localhost:5000/chart?timestamp=${new Date().getTime()}`;
    }
  }
};
</script>

<style scoped>
img {
  width: 100%;
  max-width: 800px;
}
</style>
