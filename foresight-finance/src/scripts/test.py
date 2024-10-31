import yfinance as yf
import plotly.graph_objects as go
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def homepage():
    return '''
    <h1>Welcome to the Stock Data App</h1>
    <p>Use <a href="/generate_chart?ticker=NVDA">/generate_chart</a> to generate a candlestick chart.</p>
    '''

# Route for generating candlestick chart
@app.route('/generate_chart', methods=['GET'])
def generate_chart():
    ticker = request.args.get('ticker', default='NVDA', type=str)

    # Fetch stock data using yFinance
    data = yf.download(tickers=ticker, period='5d', interval='1m')
    
    # Check if data is available
    if data.empty:
        return f"No data found for {ticker}."

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index.strftime('%m/%d\n%H:%M'),  # Formatting the time on the x-axis
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    # Update layout for the chart (optional styling)
    fig.update_layout(
        title=f"Candlestick Chart for {ticker}",
        plot_bgcolor='black',
        paper_bgcolor='rgba(32, 52, 68, 1.0)',  # Navy blue background
        font_color='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            type='category',  # Treat x-axis as categorical to avoid gaps
        ),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
    )

    # Save the chart as an HTML file
    output_file = f"{ticker}_candlestick_chart.html"
    output_path = os.path.join(os.getcwd(), output_file)  # Get the full path
    fig.write_html(output_path)

    return f"Candlestick chart for {ticker} saved as {output_file}."

if __name__ == '__main__':
    app.run(port=5000, debug=True)
