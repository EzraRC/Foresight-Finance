<template>
  <div :style="containerStyle">
    <!-- Iframe displaying the candlestick chart -->
    <iframe :src="chartUrl" frameborder="0" v-if="!loading"></iframe>
    
    <!-- Loading indicator -->
    <div v-if="loading" class="loading-indicator">
      <img :src="require('@/assets/3d-models/gif-animations/loading.gif')" alt="Loading..." />
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
        
        <!-- Search button -->
        <button class="search-button" @click="updateChart">
          <span>🔍</span>
        </button>

        <!-- Hyperlink to open modal with stock symbols -->
        <a href="javascript:void(0)" @click="openModal" class="trending-link">Click here for a list of stock symbols!</a>

        <!-- Hyperlink to open key with pattern explanation -->
        <a href="javascript:void(0)" @click="openAcronymModal" class="trending-link">
          Need help with the patterns? Click here!
        </a>

        <!-- Modal for displaying acronyms and their explanations -->
        <div v-if="isAcronymModalOpen" class="modal-overlay" @click.self="closeAcronymModal">
          <div class="modal-content">
            <!-- Title for the modal, centered and fixed -->
            <h2>Pattern Explanations</h2>

            <!-- Scrollable list of acronyms and descriptions -->
            <div class="acronym-list-container">
              <ul>
                <li v-for="(acronym, index) in acronymList" :key="index" class="acronym-item">
                  <!-- Pattern term with color -->
                  <p>
                    <span class="acronym-term" :style="{ color: acronym.color.toLowerCase() }">
                      <strong>{{ acronym.term }}</strong> - {{ acronym.color }}
                    </span>:
                  </p>
                  <!-- Description text in white -->
                  <p class="acronym-description">{{ acronym.description }}</p>
                </li>
              </ul>
            </div>

            <!-- Close button fixed at the bottom -->
            <button @click="closeModal">Close</button>
          </div>
        </div>


      </div>

      <!-- Stock information -->
      <div class="stock-info">
        <div style="display: grid; grid-template-columns: repeat(4, 2fr); gap: 10px; column-gap: 150px; margin-left: 10px;">
          <p style="color: white;">Symbol: <span>{{ stockCode }}</span></p>
          <p style="color: white;">Company Name: <span>{{ stockName }}</span></p>
          <p style="color: white;">Current Price: <span>{{ currentPrice }}</span></p>
          <p style="color: white;">Market Cap: <span>{{ marketCap }}</span></p>

          <p style="color: white;">% Change: <span>{{ percentChange }}</span></p>
          <p style="color: white;">Volume: <span>{{ volume }}</span></p>
          <p style="color: white;">Industry: <span>{{ industry }}</span></p>
          <p style="color: white;">Sector: <span>{{ sector }}</span></p>
      </div>
      </div>
    </div>

    <!-- Countdown timer for refreshing the graph -->
    <div class="refresh-timer" v-if="refreshing">
      <p style="color: white;">Refreshing graph in: {{ countdown }}s</p>
    </div>

    <!-- Modal for displaying stock symbols i got it from https://gretlcycu.wordpress.com/wp-content/uploads/2013/08/quick-ticker-symbol-list.pdf -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Stock Symbols & Company Names</h2>
        <ul>
      <li v-for="(company, index) in stockSymbols" :key="index">
        <a 
          href="javascript:void(0)" 
          @click="selectSymbol(company.symbol)"
        >
          {{ company.symbol }}
        </a>
        - {{ company?.name || 'Unknown Company' }}
      </li>
    </ul>
        <button @click="closeModal">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      ticker: '',
      chartUrl: this.getChartUrl(''),
      loading: false,
      refreshing: false,
      countdown: 200,
      refreshInterval: null,
      countdownInterval: null,
      isModalOpen: false,
      stockData: '', // Holds stock data from the file
      stockSymbols: [],
      acronymKey: '', // Holds the content of the acronym key file
      isAcronymModalOpen: false, // Controls the acronym key modal
    };
  },
  created() {
    this.fetchStockSymbols(); // Fetch symbols when component is created
  },
  methods: {  
    async fetchAcronymKey() {
  try {
    const response = await fetch('http://127.0.0.1:5000/src/static/acronym_key.txt');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.text();

    console.log('Raw fetched data:', data); // Debugging output

    this.acronymList = data
      .split('+') // Split entries by the '+' delimiter
      .map(entry => {
        const cleanedEntry = entry.trim();
        if (!cleanedEntry) return null; // Skip empty entries

        // Split each entry into term-color and description
        const [termColor, description] = cleanedEntry.split(': ');
        if (!termColor || !description) {
          console.error('Parsing failed for entry:', cleanedEntry);
          return null;
        }

        // Split the termColor part into term and color
        const [term, color] = termColor.split(' - ');
        return {
          term: term?.trim() || 'Unknown',
          color: color?.trim() || 'Unknown',
          description: description.trim()
        };
      })
      .filter(entry => entry); // Remove null or invalid entries

    console.log('Parsed acronym list:', this.acronymList); // Debugging output
    this.isAcronymModalOpen = true; // Open modal on successful fetch
  } catch (error) {
    console.error('Error fetching acronym key:', error);
  }
},

  openAcronymModal() {
    this.isAcronymModalOpen = true;
    this.fetchAcronymKey();
  },

  async fetchStockSymbols() {
    try {
      const response = await fetch('http://127.0.0.1:5000/src/static/stock_data.txt');
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.text();
      this.stockSymbols = data
        .split('\n')
        .map(line => {
          const [symbol, ...nameParts] = line.trim().split(' ');
          const name = nameParts.join(' ');
          return symbol ? { symbol, name: name || 'Unknown' } : null;
        })
        .filter(entry => entry); // Remove null or invalid entries
    } catch (error) {
      console.error('Error fetching stock symbols:', error);
    }
  },

    selectSymbol(symbol) {
      this.ticker = symbol; // Set the selected symbol in the search bar
      this.updateChart(); // Trigger chart update
      this.closeModal(); // Close the modal
    },

    getChartUrl(ticker) {
      return `http://localhost:8080/candlestick_chart.html?ticker=${ticker}&timestamp=${new Date().getTime()}`;
    },
    updateChart() {
    if (this.ticker.trim() === '') {
      return; // Exit the method if ticker is empty
    }
    
    // Proceed with fetching the chart
    this.chartUrl = this.getChartUrl(this.ticker);
    this.loading = true; // Show loading indicator

    // Fetch the chart data
    console.log(`Fetching data for ticker: ${this.ticker}`);

      setTimeout(async () => {
        try {
          const response = await fetch(`http://localhost:5000/generate_chart?ticker=${this.ticker}`);
          const data = await response.json();

          console.log("Response data:", data);
          if (data.success) {
          this.chartUrl = this.getChartUrl(this.ticker);
          this.stockName = data.longName;
          this.stockCode = data.symbol;
          this.marketCap = data.marketCap;
          this.percentChange = data.percentChange;
          this.volume = data.volume;
          this.industry = data.industry; 
          this.sector = data.sector;
          this.currentPrice = data.currentPrice;

          console.log(`Chart updated for ticker: ${this.ticker}`);
        } else {
            console.error('Error with data response:', data.message);
            this.clearStockInfo();
          }
        } catch (error) {
          console.error('Error fetching chart data:', error);
        } finally {
          this.loading = false;
        }
      }, 2000);
    },
    clearStockInfo() {
      this.stockCode = 'Error: Invalid ticker';
      this.stockName = this.currentPrice = this.marketCap = '';
      this.percentChange = this.volume = this.industry = this.sector = '';
    },
    openModal() {
      this.isModalOpen = true; // Open modal without fetching from a file
    },
    closeModal() {
      this.isModalOpen = this.isAcronymModalOpen = false;
    },
    startAutoRefresh() {
      this.refreshing = true;
      this.refreshInterval = setInterval(() => {
        this.updateChart();
      }, 200000);

      this.countdown = 200;
      this.countdownInterval = setInterval(() => {
        this.countdown -= 1;
        if (this.countdown <= 0) {
          this.countdown = 200;
        }
      }, 1000);
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
      this.refreshing = false;
    },
  },
  mounted() {
    this.startAutoRefresh();
  },
  beforeDestroy() {
    this.stopAutoRefresh();
  },
  computed: {
    containerStyle() {
      return {
        backgroundColor: '#183243',
        padding: '30px',
        borderRadius: '10px',
        position: 'relative',
      };
    }
  }
};
</script>

<style scoped>

iframe {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 600px;
  border: none;
  position: relative;
  margin-top: 70px;
  margin-bottom: -20px;
}

.search-info-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  width: 150px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-bar button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #f9c802;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;

}

.trending-link {
  color: #f9c802;
  margin-left: 15px;
  font-size: 16px;
  text-decoration: underline;
}

.trending-link:hover {
  text-decoration: none;
  color: #c6a200;
}

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
}

.refresh-timer {
  position: absolute;
  height: 55px;
  bottom: 20px;
  right: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  color: white;
  font-size: 15px;
  margin-bottom: 90px;
}

/* List styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #f9c802;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  text-align: center;
  margin: auto;   /* Center modal */
}

.modal-content h2 {
  margin-bottom: 10px;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
  text-align: left;
  max-height: 300px;
  overflow-y: auto;
}

.modal-content button {
  margin-top: 10px;
  padding: 10px;
}

/* Scrollable container for acronyms and descriptions */
.acronym-list-container {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  max-width: 1000px;
}

/* Styling for each acronym entry */
.acronym-item {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #333;
  border-radius: 5px;
  background-color: #222;
  max-width: 500px;
}

/* Styling for the pattern term (e.g., 'HS (Head and Shoulders) - Cyan') */
.acronym-term {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
}

/* Styling for the description text */
.acronym-description {
  color: white;
  font-size: 1em;
  line-height: 1.5;
}

/* Close button */
button {
  background-color: #000000;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  align-self: center;
  margin-top: 10px;
}

/* Button hover effect */
button:hover {
  background-color: #666;
}
</style>
