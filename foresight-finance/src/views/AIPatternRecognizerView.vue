<template>
  <div :style="containerStyle">
    <!-- Iframe displaying the candlestick chart -->
    <iframe :src="chartUrl" frameborder="0" v-if="!loading"></iframe>
    
    <!-- Loading indicator -->
    <div v-if="loading" class="loading-indicator">
      Loading...
    </div>

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
        <p style="color: white;">Symbol: <span>{{ stockCode }}</span></p> <!-- Updated label -->
        <p style="color: white;">Company Name: <span>{{ stockName }}</span></p> <!-- Updated label -->
        <p style="color: white;">Market Cap: <span>{{ marketCap }}</span></p> <!-- Updated label -->
        <p style="color: white;">% Change: <span>{{ percentChange }}</span></p> <!-- Updated label -->
        <p style="color: white;">Volume: <span>{{ volume }}</span></p>
      </div>
    </div>

    <!-- Countdown timer for refreshing the graph -->
    <div class="refresh-timer" v-if="refreshing">
      <p style="color: white;">Refreshing graph in: {{ countdown }}s</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      ticker: '',  // Default stock ticker
      chartUrl: this.getChartUrl(''), // Initialize with default ticker
      stockName: '...',  // Replace with dynamic data as needed
      stockCode: '...',  // New data property for stock code
      marketCap: '...',  // New data property for market cap
      percentChange: '...',  // New data property for percent change
      volume: '...',  // Replace with dynamic data as needed
      loading: false, // Loading state
      refreshing: false, // Refreshing state
      countdown: 60, // Countdown timer in seconds
      refreshInterval: null, // Store the interval ID
      countdownInterval: null, // Store the countdown interval ID
    };
  },
  methods: {
    getChartUrl(ticker) {
      return `http://localhost:8080/candlestick_chart.html?ticker=${ticker}&timestamp=${new Date().getTime()}`;
    },
    updateChart() {
      this.loading = true; // Set loading to true while fetching data
      console.log(`Fetching data for ticker: ${this.ticker}`); // Debug log
      
      // Delay the chart update by 2 seconds
      setTimeout(async () => {
        try {
          const response = await fetch(`http://localhost:5000/generate_chart?ticker=${this.ticker}`);
          const data = await response.json();

          console.log("Response data:", data); // Log the entire response data

          if (data.success) {
            this.chartUrl = this.getChartUrl(this.ticker); // Refresh the chart
            this.stockName = data.stockName;
            this.stockCode = data.stockCode; // Update the stock code from the response
            this.marketCap = data.marketCap; // Update the market cap from the response
            this.percentChange = data.percentChange; // Update the percent change from the response
            this.volume = data.volume;

            console.log(`Chart updated for ticker: ${this.ticker}`); // Debug log
          } else {
            console.error('Error with data response:', data.message); // Log error message
            this.stockName = 'Error: Invalid ticker';
            this.stockCode = 'Error'; // Set stock code to error
            this.marketCap = 'Error'; // Set market cap to error
            this.percentChange = 'Error'; // Set percent change to error
            this.volume = 'Error: No volume found';
          }
        } catch (error) {
          console.error('Error fetching chart data:', error);
          this.stockName = 'Error';
          this.stockCode = 'Error'; // Set stock code to error
          this.marketCap = 'Error'; // Set market cap to error
          this.percentChange = 'Error'; // Set percent change to error
          this.volume = 'Error';
        } finally {
          this.loading = false; // Set loading to false after fetching
        }
      }, 2000); // 2000 milliseconds delay
    },
    startAutoRefresh() {
      this.refreshing = true; // Set refreshing state
      this.refreshInterval = setInterval(() => {
        this.updateChart(); // Call updateChart every 60 seconds
      }, 60000); // 60 seconds in milliseconds

      // Countdown timer setup
      this.countdown = 60; // Reset countdown
      this.countdownInterval = setInterval(() => {
        this.countdown -= 1; // Decrease countdown
        if (this.countdown <= 0) {
          this.countdown = 60; // Reset countdown
        }
      }, 1000); // Update countdown every second
    },
    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
        this.refreshInterval = null;
      }
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
      }
      this.refreshing = false; // Reset refreshing state
    },
  },
  mounted() {
    this.startAutoRefresh(); // Start auto-refresh when the component is mounted
  },
  beforeDestroy() {
    this.stopAutoRefresh(); // Stop auto-refresh when the component is destroyed
  },
  computed: {
    containerStyle() {
      return {
        backgroundColor: 'rgba(32, 52, 68, 1.0)',
        padding: '20px',
        borderRadius: '10px',
        position: 'relative', // Required for absolute positioning of the timer
      };
    }
  }
};
</script>

<style scoped>
iframe {
  margin: 0; /* Remove any margin */
  padding: 0; /* Remove any padding */
  width: 100%;
  height: 600px; /* Set height to maintain space */
  border: none;
  position: relative; /* Ensure proper positioning */
  margin-top: 70px;
  margin-bottom: -20PX;
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

/* Styling for the loading indicator */
.loading-indicator {
  color: white;
  font-size: 40px; /* Increase font size for the loading text */
  text-align: center;
  height: 600px; /* Match height of the iframe */
  display: flex; /* Center the text */
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  margin-top: 70px; /* Ensure it's below the iframe */
  margin-bottom: -20px
}

/* Styling for the refresh timer */
.refresh-timer {
  position: absolute; /* Use absolute positioning */
  bottom: 20px; /* Position from the bottom */
  right: 20px; /* Position from the right */
  background-color: rgba(0, 0, 0, 0.5); /* Optional: Add a semi-transparent background */
  padding: 10px; /* Padding around the text */
  color: white; /* Text color */
  font-size: 15px; /* Font size */
}
</style>
