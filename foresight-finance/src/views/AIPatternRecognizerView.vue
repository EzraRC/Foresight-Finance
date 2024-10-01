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

        <!-- Hyperlink to open modal with stock symbols -->
        <a href="javascript:void(0)" @click="openModal" class="trending-link">Click here for a list of stock symbols!</a>
      </div>

      <!-- Stock information -->
      <div class="stock-info">
        <p style="color: white;">Symbol: <span>{{ stockCode }}</span></p>
        <p style="color: white;">Company Name: <span>{{ stockName }}</span></p>
        <p style="color: white;">Market Cap: <span>{{ marketCap }}</span></p>
        <p style="color: white;">% Change: <span>{{ percentChange }}</span></p>
        <p style="color: white;">Volume: <span>{{ volume }}</span></p>
      </div>
    </div>

    <!-- Countdown timer for refreshing the graph -->
    <div class="refresh-timer" v-if="refreshing">
      <p style="color: white;">Refreshing graph in: {{ countdown }}s</p>
    </div>

    <!-- Modal for displaying stock symbols https://gretlcycu.wordpress.com/wp-content/uploads/2013/08/quick-ticker-symbol-list.pdf -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Stock Symbols & Company Names</h2>
        <ul>
          <li v-for="symbol in stockSymbols" :key="symbol">{{ symbol }}</li>
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
      stockName: '...',
      stockCode: '...',
      marketCap: '...',
      percentChange: '...',
      volume: '...',
      loading: false,
      refreshing: false,
      countdown: 120,
      refreshInterval: null,
      countdownInterval: null,
      isModalOpen: false, // Control the modal state
      stockData: '', // Holds stock data from the file
      // Hardcoded list of stock symbols
      stockSymbols: [
        'AAPL - Apple Inc.', 'GOOGL - Alphabet Inc.',  'MSFT - Microsoft Corp.',  'AMZN - Amazon.com Inc.',  'TSLA - Tesla Inc.',  'FB - Meta Platforms Inc.',  'NFLX - Netflix Inc.',  'NVDA - NVIDIA Corp.',  'BRK.B - Berkshire Hathaway Inc.',  'JPM - JPMorgan Chase & Co.',  'ABT - Abbott Laboratories',  'ANF - Abercrombie & Fitch Co.',  'ABGX - Abgenix Inc.',  'ADPT - Adaptec Inc',  'ADBE - Adobe Systems Inc.',  'ADIC - Advanced Digital Information',  'AMD - Advanced Micro Devices',  'ADVS - Advent Software Inc.',  'ARXX - Aeroflex Inc.',  'AES - AES Corp',  'AET - Aetna Inc.',  'AFFX - Affymetrix Inc.',  'AFL - AFLAC Inc',  'A - Agilent Technologies Inc.',  'APD - Air Products & Chem',  'AKAM - Akamai Technologies Inc.',  'ACV - Alberto-Culver Cl\'B\'',  'ABS - Albertson\'s, Inc',  'AL - Alcan Aluminium Ltd',  'AA - Alcoa Inc.',  'ATI - Allegheny Technologies',  'AGN - Allergan, Inc',  'AW - Allied Waste Ind',  'ALL - Allstate Corp',  'AT - Alltel Corp',  'ALTR - Altera Corp',  'AMZN - Amazon.com Inc.',  'AEP - Amer Electric Pwr',  'AM - Amer Greetings Cl\'A\'',  'AIG - Amer Intl Group',  'APCC - Amer Power Conversion',  'AHC - Amerada Hess',  'AEE - Ameren Corp',  'AEOS - American Eagle Outfitters Inc.',  'AXP - American Express Company',  'AMTD - Ameritrade Holding Corp.',  'AMGN - Amgen Inc',  'AMR - AMR Corp',  'ASO - AmSouth Bancorp',  'APC - Anadarko Petroleum',  'ADI - Analog Devices Inc.',  'ANDW - Andrew Corp',  'ADRX - Andrx Corporation',  'BUD - Anheuser-Busch Cos',  'TWX - AOL Time Warner',  'AOC - Aon Corp',  'APA - Apache Corp',  'AAPL - Apple Computer Inc.',  'APPB - Applebees International Inc.',  'AMAT - Applied Materials Inc.',  'AMCC - Applied Micro Circuits Corp',  'ADM - Archer-Daniels-Midland',  'ARIA - Ariad Pharmaceuticals Inc.',  'ARBA - Ariba Inc.',  'ARW - Arrow Electronics Inc.',  'ASH - Ashland Inc',  'ASKJ - Ask Jeeves Inc.',  'T - AT&T Corp',  'AWE - AT&T Wireless Corp',  'ADSK - Autodesk, Inc',  'ADP - Automatic Data Proc',  'AZO - AutoZone Inc',  'AVY - Avery Dennison Corp',  'AVA - Avista Corp',  'AVP - Avon Products Inc.',  'BHI - Baker Hughes Inc',  'BLL - Ball Corp',  'BAC - Bank of America',  'BK - Bank of New York Inc.',  'ONE - Bank One Corp',  'BCR - Bard (C.R.)',  'BKS - Barnes & Noble Inc.', 'ABX - Barrick Gold',  'BOL - Bausch & Lomb Inc.',  'BAX - Baxter International',  'BBT - BB&T Corp',  'BCE - BCE Inc.',  'BEAS - BEA Systems Inc.',  'BSC - Bear Stearns Cos',  'BDX - Becton, Dickinson',  'BBBY - Bed Bath & Beyond Inc.',  'BLS - BellSouth Corp',  'BMS - Bemis Co',  'BBY - Best Buy Co. Inc',  'BLI - Big Lots Inc.',  'BMET - Biomet, Inc',  'BBH - Biotch Holders Trust',  'BDK - Black & Decker Corp',  'HRB - Block H & R Inc.',  'BBI - Blockbuster Inc.',  'BMC - BMC Software',  'BA - Boeing Co.',  'BCC - Boise Cascade',  'BSX - Boston Scientific',  'BP - BP Plc',  'BGG - Briggs & Stratton',  'BMY - Bristol-Myers Squibb',  'BSY - British Sky Broadcasting',  'BTY - British Telecommunications',  'BRCM - Broadcom Corp\'A\'',  'BRCD - Brocade Comm. Systems',  'BC - Brunswick Corp',  'BNI - Burlington Northn Santa Fe',  'BR - Burlington Resources',  'CPN - Calpine Corp',  'CPB - Campbell Soup Co.',  'COF - Capital One Financial',  'CAH - Cardinal Health',  'CCL - Carnival Corp',  'CAT - Caterpillar Inc.',  'CRA - Celera Genomics',  'CELG - Celgene Corporation',  'CD - Cendant Corp',  'CTX - Centex Corp',  'CTL - CenturyTel Inc',  'CEN - Ceridian Corp',  'CF - Charter One Finl',  'CHKP - Checkpoint Software',  'CVX - ChevronTexaco Corp',  'CHL - China Telecommunications',  'CHINA - China.com Corp',  'CHIR - Chiron Corp',  'CB - Chubb Corp',  'CI - CIGNA Corp',  'CINF - Cincinnati Financial',  'CIN - CINergy Corp',  'CC - Circuit City Strs-CrctCtyGrp',  'CSCO - Cisco Systems Inc.',  'C - Citigroup Inc.',  'CTXS - Citrix Systems Inc.',  'CCU - Clear Channel Comm.',  'CLX - Clorox Co.',  'CMGI - CMG Information Services Inc.',  'CMS - CMS Energy',  'CNET - CNET Inc.',  'COKE - Coca-Cola Bottling Co.',  'KO - Coca-Cola Co',  'CCE - Coca-Cola Enterprises',  'CL - Colgate-Palmolive Co.',  'CMCSK - Comcast Cl\'A\'Spl(non-vtg)',  'CMA - Comerica Inc',  'CMRC - Commerce One Inc.',  'CA - Computer Assoc Intl',  'CSC - Computer Sciences',  'CPWR - Compuware Corp',  'CMVT - Comverse Technology',  'CAG - ConAgra Inc',  'ED - Consolidated Edison',  'CEG - Constellation Energy Group',  'CAL - Continental Airlines',  'CVG - Convergys Corp',  'CBE - Cooper Indus',  'CTB - Cooper Tire & Rubber',  'RKY - Coors (Adolph)Cl\'B\'',  'GLW - Corning Inc.',  'COST - Costco Wholesale',  'COX - Cox Communications Inc.',  'CR - Crane Co',  'CREE - Cree Research Inc.',  'CCK - Crown Cork & Seal',  'CSX - CSX Corp',  'CRGN - Curagen Corp',  'CVS - CVS Corporation',  'CYTO - Cytogen Corp',  'DCX - Daimler Benz & Chrysler',  'DCN - Dana Corp',  'DHR - Danaher Corp',  'DRI - Darden Restaurants',  'DE - Deere & Co.',  'DELL - Dell Computer Corp', 'DPH - Delphi Automotive Systems', 'DAL - Delta Air Lines Inc.',  'DEL - Deltic Timber Corp.',  'DLX - Deluxe Corp',  'DIA - Diamonds Trust',  'DDS - Dillard\'s Inc\'A\'',  'DIS - Disney Walt Co.',  'DVSA - Diversa Corp',  'DG - Dollar General',  'DLTR - Dollar Tree Stores Inc.',  'D - Dominion Resources',  'DCLK - Doubleclick Inc.',  'DOV - Dover Corp',  'DOW - Dow Chemical Co.',  'DJ - Dow Jones Company Inc.',  'DRYR - Dreyers Grand Ice Cream Inc.',  'DTE - DTE Energy',  'DUK - Duke Energy Corporation',  'DNB - Dun & Bradstreet',  'DD - DuPont de Nemours EI & Co.',  'DPMI - DuPont Photomasks Inc.',  'ELNK - Earthlink Network Inc.',  'EMN - Eastman Chemical',  'EK - Eastman Kodak Co.',  'ETN - Eaton Corp',  'EBAY - Ebay Inc.',  'ELON - Echelon Corp.',  'DISH - Echostar Communications',  'ECL - Ecolab Inc',  'EIX - Edison Intl',  'ERTS - Electronic Arts Inc.',  'EDS - Electronic Data Systems',  'EMC - EMC Corporation',  'EMR - Emerson Electric',  'EC - Engelhard Corp',  'ETR - Entergy Corp',  'ENZ - Enzo Biochem Inc.',  'EQR - Equity Residential',  'EQIX - Equinix Inc.',  'ESV - Ensco plc',  'EQT - EQT Corporation',  'ES - Entergy',  'EXC - Exelon Corporation',  'XRX - Xerox Corp',  'F - Ford Motor Co.',  'FTI - FMC Technologies',  'FOE - Ferro Corp',  'FDX - FedEx Corp',  'FNM - Fannie Mae',  'FRE - Freddie Mac',  'FDS - FactSet Research',  'FMC - FMC Corp',  'FNF - Fidelity National Financial',  'FISV - Fiserv Inc.',  'FLEX - Flextronics International',  'FLIR - FLIR Systems Inc.',  'FOSL - Fossil Inc.',  'F - Ford Motor Company',  'FOXA - Fox Entertainment Group',  'GILD - Gilead Sciences',  'GE - General Electric',  'GGP - General Growth Properties',  'GM - General Motors',  'GWW - Grainger (W.W.)',  'GRMN - Garmin Ltd.',  'GDI - GDI Corp.',  'GPC - Genuine Parts Co.',  'GIS - General Mills Inc.',  'GL - Genesee & Wyoming',  'GT - Goodyear Tire & Rubber',  'GIL - Gildan Activewear Inc.',  'GLW - Glass & Glazing',  'HIG - Hartford Financial Svcs',  'HAS - Hasbro Inc',  'HOG - Harley-Davidson Inc.',  'HAR - Harris Corporation',  'HSY - Hershey Foods Corp',  'HIG - Hartford Financial',  'HST - Host Marriott Corp.',  'HUN - Huntsman Corporation',  'HES - Hess Corp',  'HCBK - Hudson City Bancorp Inc.',  'HUM - Humana Inc.',  'IT - I.T.T. Corp',  'HMSY - HMS Holdings Corp',  'IBM - International Business Machines',  'IDXX - IDEXX Laboratories Inc.',  'IGT - International Game Technology',  'INTC - Intel Corporation',  'ICE - Intercontinental Exchange',  'IR - Ingersoll-Rand Co.',  'JCI - Johnson Controls',  'JPM - JPMorgan Chase & Co.',  'JNJ - Johnson & Johnson',  'KO - Coca-Cola Co.',  'KMB - Kimberly-Clark',  'KMX - CarMax Inc.',  'KHC - Kraft Heinz Co.',  'KSS - Kohl\'s Corp',  'K - Kellogg Company',  'KEY - KeyCorp',  'KSS - Kohl\'s Corp',  'KMI - Kinder Morgan Inc.',  'LB - L Brands, Inc.',  'LEN - Lennar Corp',  'LNT - Lincoln National',  'LLY - Eli Lilly and Company',  'LMT - Lockheed Martin',  'LOW - Lowe\'s Cos Inc.',  'LYG - Lloyds Banking Group',  'MAR - Marriott International', 'MCO - Moody\'s Corporation',  'MCHP - Microchip Technology',  'MSI - Motorola Solutions, Inc.',  'MDT - Medtronic, Inc.',  'MDP - Meredith Corp',  'MET - MetLife Inc',  'MGM - MGM Mirage',  'MSFT - Microsoft Corp',  'MMM - 3M Company',  'MU - Micron Technology Inc.',  'NEM - Newmont Mining Corp.',  'NKE - Nike Inc.',  'NFLX - Netflix, Inc.',  'NWL - Newell Rubbermaid',  'NVDA - NVIDIA Corporation',  'NVS - Novartis AG',  'NTRS - Northern Trust',  'NKE - Nike Inc.',  'NWL - Newell Rubbermaid', 'ORCL - Oracle Corp',  'PEP - PepsiCo, Inc.',  'PFE - Pfizer Inc.',  'PM - Philip Morris International',  'PMTC - PMC-Sierra',  'QCOM - Qualcomm',  'RCL - Royal Caribbean Cruises',  'RL - Ralph Lauren Corp', 'TX - Raytheon Technologies',  'SBUX - Starbucks Corporation',  'SHW - Sherwin-Williams Co.',  'SYY - Sysco Corporation',  'TGT - Target Corp.',  'TWTR - Twitter Inc.',  'TXN - Texas Instruments',  'USB - U.S. Bancorp',  'V - Visa Inc.',  'VZ - Verizon Communications',  'WBA - Walgreens Boots Alliance',  'WMT - Walmart Inc.',  'WAT - Waters Corp',  'XRX - Xerox Corp',  'ZM - Zoom Video Communications, Inc.',  'ZTS - Zoetis Inc.'  // Add more symbols as needed
      ],
    };
  },
  methods: {
    getChartUrl(ticker) {
      return `http://localhost:8080/candlestick_chart.html?ticker=${ticker}&timestamp=${new Date().getTime()}`;
    },
    updateChart() {
      this.loading = true;
      console.log(`Fetching data for ticker: ${this.ticker}`);
      
      setTimeout(async () => {
        try {
          const response = await fetch(`http://localhost:5000/generate_chart?ticker=${this.ticker}`);
          const data = await response.json();

          console.log("Response data:", data);

          if (data.success) {
            this.chartUrl = this.getChartUrl(this.ticker);
            this.stockName = data.stockName;
            this.stockCode = data.stockCode;
            this.marketCap = data.marketCap;
            this.percentChange = data.percentChange;
            this.volume = data.volume;

            console.log(`Chart updated for ticker: ${this.ticker}`);
          } else {
            console.error('Error with data response:', data.message);
            this.stockName = 'Error: Invalid ticker';
            this.stockCode = 'Error';
            this.marketCap = 'Error';
            this.percentChange = 'Error';
            this.volume = 'Error: No volume found';
          }
        } catch (error) {
          console.error('Error fetching chart data:', error);
          this.stockName = 'Error';
          this.stockCode = 'Error';
          this.marketCap = 'Error';
          this.percentChange = 'Error';
          this.volume = 'Error';
        } finally {
          this.loading = false;
        }
      }, 2000);
    },
    openModal() {
      this.isModalOpen = true; // Open modal without fetching from a file
    },
    closeModal() {
      this.isModalOpen = false;
    },
    startAutoRefresh() {
      this.refreshing = true;
      this.refreshInterval = setInterval(() => {
        this.updateChart();
      }, 120000);

      this.countdown = 120;
      this.countdownInterval = setInterval(() => {
        this.countdown -= 1;
        if (this.countdown <= 0) {
          this.countdown = 120;
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
        backgroundColor: 'rgba(32, 52, 68, 1.0)',
        padding: '20px',
        borderRadius: '10px',
        position: 'relative',
      };
    }
  }
};
</script>

<style scoped>
/* Existing styles */
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
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

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
  bottom: 20px;
  right: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  color: white;
  font-size: 15px;
}

/* Modal styles */
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
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  text-align: center;
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
</style>
