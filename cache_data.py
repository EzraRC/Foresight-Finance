import psycopg2
import yfinance as yf
import time

# Connect to the database
conn = psycopg2.connect(
    dbname="test",
    user="postgres",
    password="mysecretpassword",  # Use the password you set for the database
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Define function to fetch and cache data
def fetch_and_cache_data(symbol):
    data = yf.download(symbol, period='1d', interval='1m')  # Fetch 1-minute data for today
    for index, row in data.iterrows():
        # Convert NumPy data types to Python native types
        open_price = float(row['Open'])
        high_price = float(row['High'])
        low_price = float(row['Low'])
        close_price = float(row['Close'])
        volume = float(row['Volume'])

        # Insert data into the database
        cur.execute("""
            INSERT INTO candlestick_data (time, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (index, symbol, open_price, high_price, low_price, close_price, volume))

        # Print the data being inserted
        print(f"Time: {index}, Symbol: {symbol}, Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}, Volume: {volume}")

    conn.commit()

# Loop to auto-pull data every X seconds
symbol = 'NVDA'  # Fetch NVIDIA stock data
pull_interval = 60  # Set your interval in seconds (e.g., 60 seconds)

# Display information on console for testing
try:
    while True:
        print(f"\nFetching data for {symbol} at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
        fetch_and_cache_data(symbol)
        print(f"Data fetched and inserted. Waiting {pull_interval} seconds before the next pull...\n")
        time.sleep(pull_interval)  # Wait for the specified interval before pulling again

except KeyboardInterrupt:
    print("Script interrupted. Closing database connection.")
    cur.close()
    conn.close()
