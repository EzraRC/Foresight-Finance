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
        <a href="javascript:void(0)" @click="openAcronymModal" class="trending-link" style="margin-right: 10px;">
          Need help with the patterns? Click here!
        </a>

        <!-- Hyperlink to open modal with favorites list -->
        <a href="javascript:void(0)" @click="openFavoritesModal" class="trending-link" style="margin-right: 20px;">
          Click here for your favorites list!
        </a>


        <!-- Toggle checkbox for pattern recognition -->
        <div class="pattern-recognition-bubble">
          <label for="toggle" class="pattern-label">Enable pattern recognition</label>
          <div class="toggle-wrapper">
                  <input type="checkbox" id="toggle" v-model="enablePatternRecognition" @change="togglePatternRecognition"/>
                  <label for="toggle"></label>
                </div>
        </div>

        <!-- Modal for displaying the favorites list -->
        <div v-if="isFavoritesModalOpen" class="modal-overlay" @click.self="closeFavoritesModal">
          <div class="modal-content">
            <h2>Favorites List</h2>
            <div v-if="isUserLoggedIn">
              <ul v-if="favoritesList.length > 0">
                <li v-for="(favorite, index) in favoritesList" :key="index">{{ favorite }}</li>
              </ul>
              <div v-else>No stocks in your watchlist yet.</div>
            </div>
            <div v-else>
              Oops! It appears that you are not logged in on Foresight Finance.
              <a :href="loginUrl" style="color: #4ea1f3; text-decoration: underline;">
                Click here to login to access the favorites list
              </a>
            </div>
            <button @click="closeFavoritesModal">Close</button>
          </div>
        </div>



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
                    <span class="acronym-term" :style="{ color: acronym.color.toLowerCase(), textShadow: '-1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black, 2px 2px 0 black' }">
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
        <div style="display: grid; grid-template-columns: repeat(4, 2fr); gap: 7px; column-gap: 150px; margin-left: 10px;">
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
    <div v-if="!enablePatternRecognition" class="refresh-timer">
      Refreshing in: {{ countdown }} seconds
    </div>


    <!-- Modal for displaying stock symbols i got it from https://gretlcycu.wordpress.com/wp-content/uploads/2013/08/quick-ticker-symbol-list.pdf -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
  <div class="modal-content">
    <h2>Stock Symbols & Company Names</h2>
    <ul>
      <li v-for="(company, index) in stockSymbols" :key="index">
        <!-- Heart button for marking favorites -->
        <button
          class="heart-button"
          :style="{ color: watchList.includes(company.symbol) ? 'navy' : 'gray' }"
          @click="toggleFavorite(company.symbol)"
        >
          ❤
        </button>

        <!-- Stock symbol and company name -->
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
//imports
import { getAuth } from 'firebase/auth';
import { getFirestore, collection, getDocs, query, where, doc, getDoc, setDoc, updateDoc  } from 'firebase/firestore';
import { auth, db } from '@/firebase';

export default {
  name: 'AIPatternRecognizerView',
  data() {
    return {
      ticker: '',
      chartUrl: this.getChartUrl(''),
      patternChartUrl: '',
      enablePatternRecognition: false,
      loading: false,
      refreshing: false,
      countdown: 60,
      refreshInterval: null,
      stockData: '',
      stockSymbols: [],
      acronymKey: '',
      isModalOpen: false,
      isAcronymModalOpen: false,
      isFavoritesModalOpen: false,
      watchList: [],
      isUserLoggedIn: false,
      loginUrl: '',
      user: null,
    };
  },
  created() {
    this.fetchStockSymbols(); // Fetch symbols when component is created
    this.fetchAcronymKey();
    this.fetchWatchlist();
  },
  methods: {  

    async fetchWatchlist() {
  const user = auth.currentUser;

  // Check if the user is logged in
  if (user) {
    this.isUserLoggedIn = true;
    try {
      // Reference to the users collection
      const usersRef = collection(db, 'users');
      const q = query(usersRef, where('UID', '==', user.uid));
      const querySnapshot = await getDocs(q);

      // Check if a matching document was found
      if (!querySnapshot.empty) {
        const userDoc = querySnapshot.docs[0];
        const userData = userDoc.data();

        // Access the watchList array if it exists
        this.favoritesList = userData.watchList || [];
      } else {
        console.warn("No user document found for UID:", user.uid);
        this.favoritesList = [];
      }
    } catch (error) {
      console.error('Error fetching watchlist:', error);
    }
  } else {
    this.isUserLoggedIn = false;
    this.loginUrl = "http://localhost:8081/#/LoginSignUp";
  }
},
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
  } catch (error) {
    console.error('Error fetching acronym key:', error);
  }
},

  openAcronymModal() {
    this.isAcronymModalOpen = true;
    this.fetchAcronymKey();
  },

  async openFavoritesModal() {
      this.isFavoritesModalOpen = true; // Set the "Favorites List" modal to open

      const user = auth.currentUser;

      if (user) {
        try {
          // Fetch user's watch list
          const usersRef = collection(db, 'users');
          const q = query(usersRef, where('UID', '==', user.uid));
          const querySnapshot = await getDocs(q);

          if (!querySnapshot.empty) {
            const userDoc = querySnapshot.docs[0];
            this.watchList = userDoc.data().watchList || []; // Populate watch list
          }
        } catch (error) {
          console.error('Error opening favorites modal:', error);
        }
      } else {
        console.error('Please log in to view your favorites.');
      }
    },

async openSymbolsModal() {
      this.isModalOpen = true; // Set the "Stock Symbols" modal to open
      this.stockSymbols = []; // Clear any existing data

      const user = auth.currentUser;

      if (user) {
        try {
          // Fetch user data from Firebase
          const usersRef = collection(db, 'users');
          const q = query(usersRef, where('UID', '==', user.uid));
          const querySnapshot = await getDocs(q);

          if (!querySnapshot.empty) {
            const userDoc = querySnapshot.docs[0];
            this.watchList = userDoc.data().watchList || []; // Load existing watchlist from Firebase

            // Mock: Replace with actual fetch logic for stock symbols
            this.stockSymbols = await fetchStockSymbols(); // Fetch stock symbols
          }
        } catch (error) {
          console.error('Error fetching stock symbols or user data:', error);
        }
      } else {
        alert('Please log in to view stock symbols.');
      }
    },

    async toggleFavorite(symbol) {
    const auth = getAuth();
    const user = auth.currentUser;

    if (!user) {
        console.error("No user is logged in.");
        return;
    }

    const uid = user.uid;

    try {
        // Query the users collection to find the document with the matching UID field
        const usersQuery = query(collection(db, "users"), where("UID", "==", uid));
        const querySnapshot = await getDocs(usersQuery);

        if (!querySnapshot.empty) {
            // Assume there's only one document per UID
            const userDoc = querySnapshot.docs[0];
            const userRef = doc(db, "users", userDoc.id); // Use the document ID for updates
            const data = userDoc.data();
            const watchList = data.watchList || [];

            if (watchList.includes(symbol)) {
                // Remove the symbol from the watchlist
                const updatedWatchList = watchList.filter(item => item !== symbol);
                await updateDoc(userRef, {
                    watchList: updatedWatchList
                });
                console.log(`Removed ${symbol} from watchlist.`);
            } else {
                // Add the symbol to the watchlist
                const updatedWatchList = [...watchList, symbol];
                await updateDoc(userRef, {
                    watchList: updatedWatchList
                });
                console.log(`Added ${symbol} to watchlist.`);
            }
        } else {
            // No document found for the user, create a new one
            const newUserRef = doc(collection(db, "users"));
            await setDoc(newUserRef, {
                UID: uid,
                watchList: [symbol]
            });
            console.log(`Created new user document and added ${symbol} to watchlist.`);
        }
    } catch (error) {
        console.error("Error updating watchlist:", error);
    }
},

  closeFavoritesModal() {
    this.isFavoritesModalOpen = false;
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

    getPatternChartUrl(ticker) {
      return `http://localhost:8080/candlestick_chart_patterns.html?ticker=${ticker}&timestamp=${new Date().getTime()}`;
    },

        async updateChart() {
      if (this.ticker.trim() === '') return;

      // Set loading to true to show the indicator
      this.loading = true;
      this.chartUrl = this.getChartUrl(this.ticker);

      //Reset the countdown
      this.countdown = 60;

      console.log(`Fetching data for ticker: ${this.ticker}`);

      // Fetch stock data
      try {
        const response = await fetch(`http://localhost:5000/generate_chart?ticker=${this.ticker}`);
        const data = await response.json();

        if (data.success) {
          this.stockName = data.longName;
          this.stockCode = data.symbol;
          this.marketCap = data.marketCap;
          this.percentChange = data.percentChange;
          this.volume = data.volume;
          this.industry = data.industry;
          this.sector = data.sector;
          this.currentPrice = data.currentPrice;

          // After fetching stock data, check if pattern recognition is enabled
          if (this.enablePatternRecognition) {
            await this.fetchPatternChart();
          }
        } else {
          console.error('Error with data response:', data.message);
          this.clearStockInfo();
        }
      } catch (error) {
        console.error('Error fetching chart data:', error);
      } finally {
        this.loading = false;
      }
    },
    async fetchPatternChart() {
      console.log('Fetching pattern chart for ticker:', this.ticker);

      // Fetch the pattern-recognized chart
      try {
        const response = await fetch(`http://localhost:5000/generate_chart_with_patterns?ticker=${this.ticker}`);
        const data = await response.json();

        if (data.success) {
          this.patternChartUrl = this.getPatternChartUrl(this.ticker);
          console.log('Pattern chart updated for ticker:', this.ticker);
        } else {
          console.error('Error with pattern chart response:', data.message);
        }
      } catch (error) {
        console.error('Error fetching pattern chart:', error);
      }
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
  // Only start auto-refresh if pattern recognition is disabled
  if (!this.enablePatternRecognition && !this.refreshInterval) {
    this.countdown = 60; // Ensure countdown is reset when starting
    this.refreshInterval = setInterval(() => {
      if (this.countdown > 0) {
        this.countdown--;
      } else {
        this.countdown = 60; // Reset countdown after refreshing
      }
    }, 1000); // Countdown decreases every second
  }
},

stopAutoRefresh() {
  if (this.refreshInterval) {
    clearInterval(this.refreshInterval);
    this.refreshInterval = null;
  }
  this.countdown = null;
},

togglePatternRecognition() {
  if (this.enablePatternRecognition) {
    // If enabling pattern recognition, stop the auto-refresh
    this.updateChart();
    this.stopAutoRefresh();
    this.fetchPatternChart();
  } else {
    // If disabling pattern recognition, restart the auto-refresh
    this.countdown = 60;
    this.updateChart();
    this.startAutoRefresh();
  }
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
        backgroundColor: '#1F3644',
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
  background-color: rgb(31, 54, 68);
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
  margin-bottom: 100px;
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

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.symbol-entry {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.heart-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  margin-right: 10px;
}

.modal-content {
  background-color: #f9c802;
  padding: 20px;
  border-radius: 8px;
  width: 600px;
  text-align: center;
  margin: auto;   /* Center modal */
}

.modal-content h2 {
  margin-bottom: 10px;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
  text-align: justify;
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
  padding: 15px;
  border: 1px solid #000000;
  border-radius: 5px;
  background-color: #1832439a;
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

.heart-button {
  border: none;
  background: none;
  font-size: 1.2rem;
  cursor: pointer;
  margin-right: 10px;
}

.heart-button:hover {
  transform: scale(1.5);
  transition: transform 0.25s ease;  
}

/* Button hover effect */
button:hover {
  background-color: #66666600;
}

.pattern-recognition-bubble {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  background-color: #f9c802; 
  color: black;
  border-radius: 10px;
  padding: 10px 10px; /* Padding inside the bubble */
}

.pattern-label {
  font-size: 16px;
  margin-right: 10px; /* Adds some space between the label and the toggle */
}

.toggle-wrapper {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.toggle-wrapper input[type="checkbox"] {
  display: none;
}

.toggle-wrapper label {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #600000;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.toggle-wrapper label:before {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 30px;
  height: 30px;
  background-color: #fff;
  border-radius: 50%;
  transition: transform 0.2s ease-in-out;
}

.toggle-wrapper input[type="checkbox"]:checked + label {
  background-color: rgb(24, 121, 0);
}

.toggle-wrapper input[type="checkbox"]:checked + label:before {
  transform: translateX(28px);
}

</style>