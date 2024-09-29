import yfinance as yf
import plotly.graph_objects as go
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_chart', methods=['GET'])
def generate_chart():
    ticker = request.args.get('ticker', default='NVDA', type=str)  # Default to NVDA if no ticker provided

    # Fetch stock data
    data = yf.download(tickers=ticker, period='1d', interval='1m')

    if data.empty:
        return jsonify({"success": False, "message": "No data found for the ticker."}), 404

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])

    # Update layout for dark mode
    fig.update_layout(
        plot_bgcolor='rgba(249, 200, 2, 0.3)',  # Gold background
        paper_bgcolor='rgba(32, 52, 68, 1.0)',  # Navy blue
        font_color='white',
        xaxis=dict(showgrid=True, gridcolor='black'),
        yaxis=dict(showgrid=True, gridcolor='black'),
    )

    # Define the output path
    output_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_directory, "candlestick_chart.html")

    # Save the chart as an HTML file
    fig.write_html(output_file)

    print(f"Chart for {ticker} saved to: {output_file}")

    # Get additional stock information (for example purposes)
    volume = f"{data['Volume'].sum():,}"
    average_volume = f"{data['Volume'].mean():,.0f}"

    # Send response to the frontend
    return jsonify({
        "success": True,
        "stockName": ticker,
        "volume": volume,
        "averageVolume": average_volume
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
