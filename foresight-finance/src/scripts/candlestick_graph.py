import yfinance as yf
import plotly.graph_objects as go
import os
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Function to filter data based on trading hours (9:30 AM to 4:00 PM, Monday to Friday)
def filter_trading_hours(df):
    # Filter out weekends (Monday=0, Sunday=6)
    df = df[df.index.weekday < 5]
    
    # Filter out times outside of trading hours (9:30 AM to 4:00 PM)
    df = df.between_time('09:30', '16:00')
    
    return df

@app.route('/generate_chart', methods=['GET'])
def generate_chart():
    ticker = request.args.get('ticker', default='NVDA', type=str)  # Default to NVDA if no ticker provided
    print(f"Requested ticker: {ticker}")  # Log the requested ticker

    # Fetch stock data
    data = yf.download(tickers=ticker, period='5d', interval='1m')

    if data.empty:
        print("No data found for the ticker.")  # Log if no data found
        return jsonify({"success": False, "message": "No data found for the ticker."}), 404

    # Filter data to include only trading hours
    data = filter_trading_hours(data)

    # Create a candlestick chart
    try:
        fig = go.Figure(data=[go.Candlestick(x=data.index.strftime('%m/%d\n%H:%M'),
                                              open=data['Open'],
                                              high=data['High'],
                                              low=data['Low'],
                                              close=data['Close'])])

        # Update layout for dark mode and consecutive data (no gaps)
        fig.update_layout(
            plot_bgcolor='black',  # black background
            paper_bgcolor='rgba(32, 52, 68, 1.0)',  # Navy blue
            font_color='white',
            xaxis=dict(
                showgrid=True, 
                gridcolor='lightgray',
                type='category',  # Treat x-axis as category to remove gaps
                tickmode='auto',  # Automatically adjust ticks
                nticks=10,  # Control how many ticks are visible when fully zoomed out
                ticks="outside",
                ticklen=8,  # Length of the tick marks
            ),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            margin=dict(l=10, r=10, t=10, b=10),
        )

        # Save the chart as an HTML file
        output_directory = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_directory, "candlestick_chart.html")
        fig.write_html(output_file)
        print(f"Chart for {ticker} saved to: {output_file}")

    except Exception as e:
        print(f"Error creating chart: {e}")  # Log any errors during chart creation
        return jsonify({"success": False, "message": "Error creating chart."}), 500

    # Get additional stock information
    volume = f"{data['Volume'].sum():,}"
    average_volume = f"{data['Volume'].mean():,.0f}"

    return jsonify({
        "success": True,
        "stockName": ticker,
        "volume": volume,
        "averageVolume": average_volume
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
