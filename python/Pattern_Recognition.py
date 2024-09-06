import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import Stock_Patterns as sp

# Download historical stock data
ticker = 'AAPL'  #Uses Apple Stock
data = yf.download(ticker, start='2020-01-01', end='2024-09-05', interval='1d')

# Visualize the data
data['Close'].plot(figsize=(10, 6))
plt.title(f"{ticker} Stock Price")
plt.show()

def label_patterns(data):
    data['ascending_triangle'] = data['Close'].rolling(50).apply(sp.detect_ascending_triangle)
    return data

data = label_patterns(data)

print(data)
print("Cookie")