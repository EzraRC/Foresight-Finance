import numpy as np
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, jsonify

app = Flask(__name__)

# Function to convert the dataframe into a format for plotting
def plot_candlestick_chart(df):
    df['time'] = df['time'].astype(str)  # Convert datetime to string if needed
    df['open'] = df['open'].tolist()
    df['high'] = df['high'].tolist()
    df['low'] = df['low'].tolist()
    df['close'] = df['close'].tolist()

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])

    # Update layout for better appearance
    fig.update_layout(
        title='Candlestick Chart',
        xaxis_title='Time',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

    # Convert figure to dict
    return fig.to_dict()

# Utility function to make chart data JSON-serializable
def make_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(elem) for elem in obj]
    else:
        return obj

@app.route('/chart')
def chart():
    # Simulate fetching some stock data
    data = {
        'time': pd.date_range(start='2024-09-01', periods=100, freq='H'),
        'open': np.random.randn(100),
        'high': np.random.randn(100),
        'low': np.random.randn(100),
        'close': np.random.randn(100)
    }
    df = pd.DataFrame(data)

    # Generate the chart data
    chart_data = plot_candlestick_chart(df)

    # Make sure the data is serializable
    serializable_chart_data = make_serializable(chart_data)

    # Return JSON response
    return jsonify(serializable_chart_data)

if __name__ == '__main__':
    app.run(debug=True)