<template>
  <div :style="containerStyle">
    <h1 style="color: white;">Candlestick Chart</h1>
    
    <!-- Iframe displaying the candlestick chart -->
    <iframe :src="chartUrl" width="100%" height="600px" frameborder="0"></iframe>

    <!-- Container for search bar and stock info -->
    <div class="search-info-container">
      <!-- Search bar to input ticker symbol -->
      <div class="search-bar">
        <input 
          type="text" 
          v-model="ticker" 
          @keyup.enter="updateChart"
          placeholder="Enter stock ticker"
        />
        <button @click="updateChart">Search</button>
      </div>

      <!-- Stock information -->
      <div class="stock-info">
        <p>Stock Name: <span>{{ stockName }}</span></p>
        <p>Volume: <span>{{ volume }}</span></p>
        <p>Average Volume: <span>{{ averageVolume }}</span></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      ticker: 'NVDA',  // Default stock ticker
      chartUrl: this.getChartUrl('NVDA'), // Initialize with default ticker
      stockName: 'loading ...',  // Replace with dynamic data as needed
      volume: 'cannot obtain...',  // Replace with dynamic data as needed
      averageVolume: 'cannot calculate...', // Replace with dynamic data as needed
    };
  },
  methods: {
    getChartUrl(ticker) {
      return `http://localhost:8080/candlestick_chart.html?ticker=${ticker}&timestamp=${new Date().getTime()}`;
    },
    async updateChart() {
      // Make an API call to regenerate the chart with the new ticker
      try {
        const response = await fetch(`http://localhost:5000/generate_chart?ticker=${this.ticker}`);
        const data = await response.json();
        if (data.success) {
          // If the chart generation is successful, update the iframe URL
          this.chartUrl = this.getChartUrl(this.ticker);
          this.stockName = data.stockName;
          this.volume = data.volume;
          this.averageVolume = data.averageVolume;
        }
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
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

/* Container for search bar and stock info */
.search-info-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

/* Styling for the search bar */
.search-bar {
  flex: 1;
  margin-right: 20px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  width: 200px;
  margin-right: 10px;
}

.search-bar button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

/* Styling for the stock information */
.stock-info {
  flex: 1;
  color: white;
  font-size: 18px;
}

.stock-info p {
  margin: 5px 0;
}

.stock-info span {
  font-weight: bold;
}
</style>
