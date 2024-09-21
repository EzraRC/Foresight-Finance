import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import Stock_Patterns as sp
import threading
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Download historical stock data
ticker = 'AAPL' 
data = yf.download(ticker, period='5d', interval='1m')
data2 = yf.download('LMT', period='5d', interval='1m')

# Visualize the data
data['Close'].plot(figsize=(10, 6))
plt.title(f"{ticker} Stock Price")
plt.show()

prices = data['Close']
prices2 = data2['Close']


lookbackPeriods = [30, 50, 70, 100]

# Detect patterns across multiple lookback periods
def detectPattern(prices, pattern_fn):
    for lookback in lookbackPeriods:
        if pattern_fn(prices, lookback):
            return True  # If the pattern is found in any lookback window, return True
    return False

def labelPatterns(data):
    data['ascending_triangle'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.ascendingTriangle))
    data['descending_triangle'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.descendingTriangle))
    data['symmetrical_triangle'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.symmetricalTriangle))
    data['pennant'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.pennant))
    data['flag'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.flag))
    data['wedge'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.wedge))
    data['double_bottom'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.doubleBottom))
    data['double_top'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.doubleTop))
    data['head_and_shoulders'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.headShoulders))
    data['rounding_top'] = data['Close'].rolling(100).apply(lambda x:detectPattern(x,sp.roundingTop))
    data['rounding_bottom'] = data['Close'].rolling(100).apply(lambda x: detectPattern(x,sp.roundingBottom))
    data['cup_and_handle'] = data['Close'].rolling(100).apply(lambda x:detectPattern(x,sp.cupAndHandle))
    return data

data = labelPatterns(data)
data2 = labelPatterns(data2)

from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_model(data):
    # Prepare the dataset with detected patterns
    patterns = ['ascending_triangle', 'descending_triangle', 'symmetrical_triangle', 'pennant', 'flag', 'wedge',
                'double_bottom', 'double_top', 'head_and_shoulders', 'rounding_top', 'rounding_bottom', 'cup_and_handle']

    data = data.dropna(subset=patterns)

    # Combine multiple pattern labels into a single target for multi-class classification
    data['target'] = (data['ascending_triangle'] * 1 +
                      data['descending_triangle'] * 2 +
                      data['symmetrical_triangle'] * 3 +
                      data['pennant'] * 4 +
                      data['flag'] * 5 +
                      data['wedge'] * 6 +
                      data['double_bottom'] * 7 +
                      data['double_top'] * 8 +
                      data['head_and_shoulders'] * 9 +
                      data['rounding_top'] * 10 +
                      data['rounding_bottom'] * 11 +
                      data['cup_and_handle'] * 12)

    # Remove rows where no pattern is detected (target is 0)
    data = data[data['target'] > 0]

    X = data[patterns].fillna(0) 

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


model = train_model(data)

