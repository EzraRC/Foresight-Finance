<template>
  <div :style="containerStyle">
    <h1 style="color: white;">Candlestick Chart</h1>
    <iframe :src="chartUrl" width="100%" height="600px" frameborder="0"></iframe>
    <div class="stock-info">
      <p>Stock Name: <span>{{ stockName }}</span></p>
      <p>Volume: <span>{{ volume }}</span></p>
      <p>Average Volume: <span>{{ averageVolume }}</span></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      chartUrl: this.getChartUrl(),  // Initialize with the current timestamp
      stockName: 'NVIDIA',           // Replace with dynamic data as needed
      volume: '12,345,678',          // Replace with dynamic data as needed
      averageVolume: '1,234,567',   // Replace with dynamic data as needed
    };
  },
  mounted() {
    // Automatically refresh the chart every 61 seconds
    setInterval(() => {
      this.chartUrl = this.getChartUrl();  // Update the iframe URL to force a refresh
    }, 61000);
  },
  methods: {
    getChartUrl() {
      // Add a timestamp to prevent browser caching
      return `http://localhost:8080/candlestick_chart.html?timestamp=${new Date().getTime()}`;
    }
  },
  computed: {
    containerStyle() {
      return {
        backgroundColor: 'rgba(32, 52, 68, 1.0)',
        padding: '20px',
        borderRadius: '10px',
      };
    }
  }
};
</script>

<style scoped>

iframe {
  margin-top: 20px;
  width: 100%;
  height: 600px;
  border: none;
}

.stock-info {
  margin-top: 20px;
  color: white;
  font-size: 18px;
}

.stock-info p {
  margin: 5px 0;
  color: white;
}

.stock-info span {
  font-weight: bold;
}
</style>
