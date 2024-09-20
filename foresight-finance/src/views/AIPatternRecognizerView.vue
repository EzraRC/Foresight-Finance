<template>
  <div>
    <h1>Candlestick Chart</h1>
    <iframe :src="chartUrl" width="100%" height="600px" frameborder="0"></iframe>
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
      this.chartUrl = this.getChartUrl();  // Update the iframe URL to force a refresh
    }, 61000);  // Refresh every 61 seconds
  },
  methods: {
    getChartUrl() {
      // Add a timestamp to prevent browser caching
      return `http://localhost:8080/candlestick_chart.html?timestamp=${new Date().getTime()}`;
    }
  }
};
</script>

<style scoped>
iframe {
  margin-top: 100px;
  width: 100%;
  height: 600px;
  border: none;
}
</style>
