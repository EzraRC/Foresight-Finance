import yfinance as yf
import plotly.graph_objects as go
import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from flask_cors import CORS
import numpy as np
import patterns as pr


def generate_chart():
    ticker = 'NVDA'  # Default to NVDA if no ticker provided
    print(f"Requested ticker: {ticker}")  # Log the requested ticker

    # Fetch stock data
    data = yf.download(tickers=ticker, period='5d', interval='1m')

    if data.empty:
        print("No data found for the ticker.")  # Log if no data found
        return jsonify({"success": False, "message": "No data found for the ticker."}), 404

    print("Pre filter")
    # Filter data to include only trading hours
    data = filter_trading_hours(data)

    df = data.reset_index() #Reset index of stock data for the recognition
    df, prices, dates = df, df['Close'], df['Datetime'] #Seperatingit for easier use

    print("Indexing")
    prices.index = np.linspace(1, len(prices), len(prices)) #set the index from 1 for Nadaraya-Watson kernel regression
    dates.index = np.linspace(1, len(dates), len(dates))

    print("find max min")
    smooth_prices, smooth_prices_max_indices, smooth_prices_min_indices, \
    price_max_indices, price_min_indices, max_min, max_min_types = pr.find_max_min(prices) #FInd max and min of prices to smooth it
    
    print("patterns")
    patterns = pr.find_patterns(max_min, max_min_types) #Find Patterns

    # Create a candlestick chart
    try:
        fig = go.Figure(data=[go.Candlestick(
            x=data.index.strftime('%m/%d\n%H:%M'),
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
            title=f"Candlestick Chart with Patterns for {ticker}",
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

                # Add marker for the pattern midpoint
                fig.add_trace(go.Scatter(
                    x=[data.index[midpoint]],
                    y=[data['Close'].iloc[midpoint]],
                    mode='markers',
                    marker=dict(
                        symbol=marker_styles[pattern_name]['symbol'],
                        color=marker_styles[pattern_name]['color'],
                        size=10,
                    ),
                    name=pattern_name
                ))

                # Add bounding boxes for the patterns
                start_date = data.index[start_idx]
                end_date = data.index[end_idx]
                min_price = data['Low'].iloc[start_idx:end_idx + 1].min()
                max_price = data['High'].iloc[start_idx:end_idx + 1].max()

                fig.add_shape(
                    type="rect",
                    x0=start_date,
                    x1=end_date,
                    y0=min_price,
                    y1=max_price,
                    line=dict(
                        color=marker_styles[pattern_name]['color'],
                        width=2
                    ),
                    fillcolor=marker_styles[pattern_name]['color'],
                    opacity=0.2,
                )
        fig.show()

    except Exception as e:
        print(f"Error creating chart: {e}")  # Log any errors during chart creation

    


# Function to filter data based on trading hours (9:30 AM to 4:00 PM, Monday to Friday)
def filter_trading_hours(df):
    # Filter out weekends (Monday=0, Sunday=6)
    
    df = df[df.index.weekday < 5]
    
    # Filter out times outside of trading hours (9:30 AM to 4:00 PM)
    df = df.between_time('09:30', '16:00')
    
    return df

print("Got to the end")
generate_chart()