import yfinance as yf
import plotly.graph_objects as go
import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from flask_cors import CORS
import numpy as np
import patterns as pr

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return '''
    <h1>Welcome to the Stock Data App</h1>
    <p>Use <a href="/generate_chart?ticker=NVDA">/generate_chart</a> to generate a candlestick chart.</p>
    '''

@app.route('/generate_chart', methods=['GET'])
def generate_chart():
    ticker = request.args.get('ticker', default='NVDA', type=str)  # Default to NVDA if no ticker provided
    print(f"Requested ticker: {ticker}")  # Log the requested ticker

    # Fetch stock data
    data = yf.download(tickers=ticker, period='5d', interval='1m')

    if data.empty:
        print("No data found for the ticker.")  # Log if no data found
        return jsonify({"success": False, "message": "No data found for the ticker."}), 404

    print("Pre filter")
    # Filter data to include only trading hours
    data = filter_trading_hours(data)

    df = data.reset_index()  # Reset index of stock data for the recognition
    df, prices, dates = df, df['Close'], df['Datetime']  # Separate for easier use

    print("Indexing")
    prices.index = np.linspace(1, len(prices), len(prices))  # Set index from 1 for kernel regression
    dates.index = np.linspace(1, len(dates), len(dates))

    print("find max min")
    try:
        smooth_prices, smooth_prices_max_indices, smooth_prices_min_indices, \
        price_max_indices, price_min_indices, max_min, max_min_types = pr.find_max_min(prices)  # Find max and min prices
        print("patterns")
        patterns = pr.find_patterns(max_min, max_min_types)  # Find patterns

    except Exception as e:
        print(f"Error in pattern recognition: {e}")  # Log any errors in pattern recognition
        patterns = {}  # Set patterns to an empty dictionary if an error occurs

    # Create a candlestick chart
    try:
        fig = go.Figure(data=[go.Candlestick(
            x=data.index.strftime('%m/%d\n%H:%M'),  # Format datetime index here
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])

        # Update layout for dark mode and aesthetics
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='rgba(32, 52, 68, 1.0)',
            font_color='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                type='category',
                tickmode='auto',
                nticks=10,
                ticks="outside",
                ticklen=8,
            ),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            margin=dict(l=10, r=10, t=10, b=10),
            #title=f"Candlestick Chart with Patterns for {ticker}",
        )

        # Define marker styles and colors for each pattern type
        marker_styles = {
            'HS': {'symbol': 'circle', 'color': 'cyan'},
            'IHS': {'symbol': 'triangle-up', 'color': 'orange'},
            'BTOP': {'symbol': 'square', 'color': 'pink'},
            'BBOT': {'symbol': 'star', 'color': 'yellow'},
            'TTOP': {'symbol': 'x', 'color': 'magenta'},
            'TBOT': {'symbol': 'diamond', 'color': 'lime'},
            'RTOP': {'symbol': 'pentagon', 'color': 'brown'},
            'RBOT': {'symbol': 'triangle-down', 'color': 'black'},
            'PN': {'symbol': 'hexagon', 'color': 'blue'},
            'DTRI': {'symbol': 'hexagon', 'color': 'black'},
            'ATRI': {'symbol': 'hexagon', 'color': 'blue'}
        }

        # Loop through each pattern to add markers and bounding boxes
        for pattern_name, pattern_instances in patterns.items():
            for start_idx, end_idx in pattern_instances:
                # Ensure indices are integers
                start_idx = int(start_idx)
                end_idx = int(end_idx)
                midpoint = int((start_idx + end_idx) // 2)

                # Use formatted datetime for markers
                midpoint_date = data.index[midpoint].strftime('%m/%d\n%H:%M')
                midpoint_price = data['Close'].iloc[midpoint]

                # Add marker for the pattern midpoint
                fig.add_trace(go.Scatter(
                    x=[midpoint_date],  # Use formatted datetime for x
                    y=[midpoint_price],  # Use actual close price for y
                    mode='markers',
                    marker=dict(
                        symbol=marker_styles[pattern_name]['symbol'],
                        color=marker_styles[pattern_name]['color'],
                        size=10,
                    ),
                    name=pattern_name
                ))

                # Add bounding boxes for the patterns
                start_date = data.index[start_idx].strftime('%m/%d\n%H:%M')
                end_date = data.index[end_idx].strftime('%m/%d\n%H:%M')
                min_price = data['Low'].iloc[start_idx:end_idx + 1].min()
                max_price = data['High'].iloc[start_idx:end_idx + 1].max()

                fig.add_shape(
                    type="rect",
                    x0=start_date,  # Use formatted datetime for bounding box
                    x1=end_date,    # Use formatted datetime for bounding box
                    y0=min_price,
                    y1=max_price,
                    line=dict(
                        color=marker_styles[pattern_name]['color'],
                        width=2
                    ),
                    fillcolor=marker_styles[pattern_name]['color'],
                    opacity=0.5,
                )

        # Save the chart as an HTML file
        output_directory = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_directory, "candlestick_chart.html")
        fig.write_html(output_file)
        print(f"Chart for {ticker} saved to: {output_file}")

        #fig.show()
        
    except Exception as e:
        print(f"Error creating chart: {e}")  # Log any errors during chart creation
        return jsonify({"success": False, "message": "Error creating chart."}), 500

    # Get additional stock information
    try:
        info = yf.Ticker(ticker).info

        # Calculate total volume
        volume = f"{data['Volume'].sum():,}"

        # Ensure market_cap is formatted correctly
        market_cap = info.get('marketCap')
        if market_cap is not None:
            market_cap = f"{market_cap:,}"  # Format as string with commas
        else:
            market_cap = 'N/A'

        # Calculate percent change based on the last closing price and the first closing price
        if not data.empty:
            last_close = data['Close'].iloc[-1]
            first_close = data['Close'].iloc[0]

            if first_close > 0:
                percent_change = ((last_close - first_close) / first_close) * 100
                percent_change = f"{percent_change:.2f}%"  # Format as percentage
            else:
                percent_change = 'N/A'  # If the opening price is zero or no data
        else:
            percent_change = 'N/A'

        return jsonify({
            "success": True,
            "longName": info.get('longName', ticker),
            "symbol": info.get('symbol', ticker),
            "volume": volume,
            "marketCap": market_cap,
            "percentChange": percent_change,
            "currentPrice": info.get('currentPrice', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
        })

    except Exception as e:
        print(f"Error fetching stock info: {e}")
        return jsonify({
            "success": False,
            "longName": 'N/A',
            "symbol": ticker,
            "volume": 'N/A',
            "marketCap": 'N/A',
            "percentChange": 'N/A',
        })

# Route to serve the stock_data.txt file
@app.route('/src/static/stock_data.txt', methods=['GET'])
def serve_stock_data():
    try:
        return send_from_directory('static', 'stock_data.txt')
    except Exception as e:
        return jsonify({"success": False, "message": "File not found."}), 404

# Function to filter data based on trading hours (9:30 AM to 4:00 PM, Monday to Friday)
def filter_trading_hours(df):
    # Filter out weekends (Monday=0, Sunday=6)
    df = df[df.index.weekday < 5]
    
    # Filter out times outside of trading hours (9:30 AM to 4:00 PM)
    df = df.between_time('09:30', '16:00')
    
    return df

if __name__ == '__main__':
    app.run(port=5000, debug=True)
