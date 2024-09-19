import yfinance as yf
import plotly.graph_objects as go
import os

# Fetch stock data
data = yf.download(tickers='NVDA', period='1d', interval='1m')

# Create a candlestick chart
fig = go.Figure(data=[go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'])])

# Define the output path
output_directory = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_directory, "candlestick_chart.html")

# Save the chart as an HTML file
fig.write_html(output_file)

print(f"Chart saved to: {output_file}")
