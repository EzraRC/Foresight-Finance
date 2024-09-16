from flask import Flask, render_template, send_file
import io
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

app = Flask(__name__)

def fetch_data_from_db():
    conn = psycopg2.connect(
        dbname="test",  
        user="postgres",
        password="mysecretpassword",  
        host="localhost",
        port="5432"
    )
    query = "SELECT time, open, high, low, close FROM candlestick_data ORDER BY time ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def plot_candlestick_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['time'] = pd.to_datetime(df['time'])

    def get_candlestick_color(open_val, close_val):
        return 'green' if close_val >= open_val else 'red'

    for i in range(len(df)):
        row = df.iloc[i]
        color = get_candlestick_color(row['open'], row['close'])
        ax.plot([row['time'], row['time']], [row['low'], row['high']], color='black')
        ax.plot([row['time'], row['time']], [row['open'], row['close']], color=color, linewidth=4)

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Candlestick Chart')
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

@app.route('/chart')
def chart():
    df = fetch_data_from_db()
    img = plot_candlestick_chart(df)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
