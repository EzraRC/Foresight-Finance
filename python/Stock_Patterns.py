import numpy as np

# Detect Ascending Triangle
def ascendingTriangle(highs, lows, lookback=20):
    high_max = highs.rolling(window=lookback).max()
    low_min = lows.rolling(window=lookback).min()
    
    # Check for flat high and increasing lows
    if np.isclose(high_max[-1], high_max[-lookback]) and low_min[-1] > low_min[-lookback]:
        return True
    return False

# Detect Descending Triangle
def descendingTriangle(prices, lookback=20):
    high = prices.rolling(window=lookback).max()
    low = prices.rolling(window=lookback).min()

    # Check for flat lows and decreasing high
    if np.isclose(low[-1], low[-lookback]) and high[-1] < high[-lookback]:
        return True
    return False

# Detect Symmetrical Triangle
def symmetricalTriangle(prices, lookback=20):
    high = prices.rolling(window=lookback).max()
    low = prices.rolling(window=lookback).min()

    # Check for highs and lows meeting
    if high[-1] < high[-lookback] and low[-1] > low[-lookback]:
        return True
    return False

# Detect Pennant
def pennant(prices, lookback=20):
    high = prices.rolling(window=lookback).max()
    low = prices.rolling(window=lookback).min()
    
    # Pennant follows a strong price movement (flagpole) with converging price action (Best description I could find)
    recent_range = high[-lookback:].max() - low[-lookback:].min()
    if recent_range < 0.05 * prices[-lookback:].mean():  # Price tightens
        return True
    return False

# Detect Flag
def flag(prices, lookback=20):
    high = prices.rolling(window=lookback).max()
    low = prices.rolling(window=lookback).min()

    # Flag has a strong trend followed by oscilation 
    if np.abs(high[-1] - low[-1]) < 0.05 * prices[-lookback:].mean():
        return True
    return False

# Detect Wedge
def wedge(prices, lookback=20):
    high = prices.rolling(window=lookback).max()
    low = prices.rolling(window=lookback).min()

    # Wedge has converging high and lows, but with a slant 
    if high[-1] < high[-lookback] and low[-1] > low[-lookback]:
        return True
    return False

# Detect Double Bottom
def doubleBottom(prices, lookback=50):
    recent_min = prices.rolling(window=lookback).min()
    
    # Check for two significant drops at close levels
    if np.isclose(prices[-1], recent_min[-1], atol=0.05 * prices[-1]) and \
       np.isclose(prices[-lookback//2], recent_min[-1], atol=0.05 * prices[-1]):
        return True
    return False

# Detect Double Top
def doubleTop(prices, lookback=50):
    recent_max = prices.rolling(window=lookback).max()
    
    # Check for two significant peaks at close levels
    if np.isclose(prices[-1], recent_max[-1], atol=0.05 * prices[-1]) and \
       np.isclose(prices[-lookback//2], recent_max[-1], atol=0.05 * prices[-1]):
        return True
    return False

# Detect Head and Shoulders
def headShoulders(prices, lookback=50):
    if len(prices) < lookback:
        return False
    
    # Divide price into three segments for shoulders and head
    left_shoulder = prices[-lookback:-lookback//3]
    head = prices[-lookback//3:-lookback//6]
    right_shoulder = prices[-lookback//6:]

    # Conditions for head and shoulders
    if left_shoulder.mean() < head.mean() > right_shoulder.mean():
        return True
    return False

# Detect Rounding Top
def roundingTop(prices, lookback=50):
    mid_point = lookback // 2
    first_half = prices[:mid_point]
    second_half = prices[mid_point:]
    
    # Prices rise and gradually fall
    if first_half.mean() < prices[mid_point] > second_half.mean():
        return True
    return False

# Detect Rounding Bottom
def roundingBottom(prices, lookback=50):
    mid_point = lookback // 2
    first_half = prices[:mid_point]
    second_half = prices[mid_point:]
    
    # Prices fall and gradually rise
    if first_half.mean() > prices[mid_point] < second_half.mean():
        return True
    return False

# Detect Cup and Handle
def cupAndHandle(prices, lookback=50):
    mid_point = lookback // 2
    first_half = prices[:mid_point]
    second_half = prices[mid_point:]
    
    #  prices form a U-shape followed by a small consolidation (handle)
    if np.isclose(first_half.mean(), second_half.mean(), atol=0.05 * prices[-1]):
        return True
    return False
