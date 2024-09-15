import psycopg2
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

# Function to fetch data from PostgreSQL (TimescaleDB)
def fetch_data_from_db():
    conn = psycopg2.connect(
        dbname="test",  
        user="postgres",
        password="mysecretpassword",  # Replace with your actual password
        host="localhost",
        port="5432"
    )
    query = "SELECT time, open, high, low, close FROM candlestick_data ORDER BY time ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to plot candlestick chart using Plotly and display it locally
def plot_candlestick_chart(df):
    # Create the candlestick chart using Plotly
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

    # Show the chart locally in the default web browser
    pio.show(fig)

if __name__ == "__main__":
    # Fetch data from the database
    df = fetch_data_from_db()
    
    # Plot and display the candlestick chart locally
    plot_candlestick_chart(df)
