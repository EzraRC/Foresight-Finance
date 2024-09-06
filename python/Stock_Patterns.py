import numpy as np

def detect_ascending_triangle(prices, lookback=20):
    
    highs = prices.rolling(window=lookback).max()
    lows = prices.rolling(window=lookback).min()
    
    # Check if the highs are relatively flat and lows are increasing (ascending triangle)
    if np.isclose(highs[-1], highs[-lookback]) and lows[-1] > lows[-lookback]:
        return True
    return False