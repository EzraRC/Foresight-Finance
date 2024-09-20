import yfinance as yf
import plotly.graph_objects as go
import os

# Fetch stock data
data = yf.download(tickers='NVDA', period='1d', interval='1m')

# Create a candlestick chart with dark mode
fig = go.Figure(data=[go.Candlestick(x=data.index,
                                       open=data['Open'],
                                       high=data['High'],
                                       low=data['Low'],
                                       close=data['Close'])])

# Update layout for dark mode
fig.update_layout(
    plot_bgcolor='rgba(249, 200, 2, 0.3)',  # Make the plot area to the gold
    paper_bgcolor='rgba(32, 52, 68, 1.0)',            # Set the background color to the navy blue
    font_color='white',               # Set font color to white
    xaxis=dict(showgrid=True, gridcolor='black'),  # Set grid color for x-axis
    yaxis=dict(showgrid=True, gridcolor='black'),  # Set grid color for y-axis
)

# Define the output path
output_directory = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(output_directory, "candlestick_chart.html")

# Save the chart as an HTML file
fig.write_html(output_file)

print(f"Chart saved to: {output_file}")
