import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import Stock_Patterns as sp
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go


# Download historical stock data
ticker = 'AAPL' 
data = yf.download(ticker, period='5d', interval='1m')

# Visualize the data
# Create a candlestick chart
fig = go.Figure(data=[go.Candlestick(x=data.index,
                                       open=data['Open'],
                                       high=data['High'],
                                       low=data['Low'],
                                       close=data['Close'])])

# Add titles and labels
fig.update_layout(title=f'{ticker} Candlestick Chart',
                  xaxis_title='Time',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=False)

# Show the chart
fig.show()

# Use High and Low prices for pattern detection
prices = data[['High', 'Low']]

lookbackPeriods = [30, 50, 70, 100]


def detectPattern(high_low_data, pattern_fn):
    highs = high_low_data['High']
    lows = high_low_data['Low']
    
    for lookback in lookbackPeriods:
        if pattern_fn(highs, lows, lookback):  # Pass both highs and lows
            return True
    return False

def labelPatterns(data):
    data['ascending_triangle'] = prices['High'].rolling(100).apply(lambda x: detectPattern(pd.DataFrame({'High': x, 'Low': prices['Low'].iloc[x.index]}), sp.ascendingTriangle))
    return data

data = labelPatterns(data)

# Train model (if needed)
def train_model(data):
    # Prepare the dataset with detected patterns
    data = data.dropna(subset=['ascending_triangle'])

    # Combine pattern labels into a single target for classification
    data['target'] = data['ascending_triangle'].astype(int)

    # Remove rows where no pattern is detected (target is 0)
    data = data[data['target'] > 0]

    X = data[['ascending_triangle']].fillna(0) 
    y = data['target']

    # Train-test split (80% training, 20% testing)
    split_index = int(0.8 * len(data))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Train a Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    return model

# Optionally train the model (if there are enough detected patterns)
if data['ascending_triangle'].sum() > 0:
    model = train_model(data)
