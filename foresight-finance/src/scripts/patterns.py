#Code taken from medium
#https://medium.com/@redeaddiscolll/identifying-stock-patterns-using-deep-learning-379f2cb42011

from collections import defaultdict


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from statsmodels.nonparametric.kernel_regression import KernelReg
from yahoofinancials import YahooFinancials
import yfinance as yf
import matplotlib.patches as patches

"""
def preprocess_data(start_date, end_date, stock_code):
    stock_data = YahooFinancials(stock_code).get_historical_price_data(start_date, end_date, 'daily')
    #stock_data = yf.download(tickers = stock_code, start=start_date, end=end_date)
    price_data = stock_data[stock_code]['prices']
    columns = ['formatted_date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']
    new_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    df = pd.DataFrame(data=price_data)[columns] # order dataframe columns
    df = df.rename(index=str, columns=dict(zip(columns, new_columns))) # rename dataframe columns
    return df, df['Close'], df['Date']
"""

"""
def preprocess_data(start_date, end_date, stock_code):
    # Fetch the stock data
    stock_data = YahooFinancials(stock_code).get_historical_price_data(start_date, end_date, 'daily')
    price_data = stock_data[stock_code]['prices']
    columns = ['formatted_date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']
    new_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    # Create the dataframe and select columns
    df = pd.DataFrame(price_data)[columns]
    # Rename the columns
    df.columns = new_columns
    # Return dataframe and specific columns
    return df, df['Close'], df['Date']
"""
'''
#Yahoo finance for daily data
def preprocess_data(start_date, end_date, stock_code):
    # Download stock data using yfinance
    df = yf.download(stock_code, start=start_date, end=end_date, interval='1d')
    df = df.rename(columns={
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Adj Close': 'Adj Close',
        'Volume': 'Volume'
    })
    # Reset the index to get 'Date' as a column
    df = df.reset_index()
    return df, df['Close'], df['Date']
'''
    
#yahoo finance for minute data
def preprocess_data(stock_code):
    # Download stock data for the past 5 days with 1-minute intervals using yfinance
    df = yf.download(tickers=stock_code, period='5d', interval='1m')

    # Reset the index to get 'Datetime' as a column
    df = df.reset_index()

    # Return dataframe, Close prices, and Datetime column
    return df, df['Close'], df['Datetime']



# https://onlinelibrary.wiley.com/doi/full/10.1111/0022-1082.00265
# reference: https://www.quantopian.com/posts/an-empirical-algorithmic-evaluation-of-technical-analysis
def find_max_min(prices):
    model = KernelReg(prices.values, prices.index.values, var_type='c', bw="cv_ls")
    smooth_prices = pd.Series(data=model.fit([prices.index.values])[0], index=prices.index)

    smooth_prices_max_indices = argrelextrema(smooth_prices.values, np.greater, order=1)[0]
    smooth_prices_min_indices = argrelextrema(smooth_prices.values, np.less, order=1)[0]

    price_max_indices = []
    for i in smooth_prices_max_indices:
        if 1 < i < len(prices)-1:
            price_max_indices.append(prices.iloc[i-2:i+2].idxmax())

    price_min_indices = []
    for i in smooth_prices_min_indices:
        if 1 < i < len(prices)-1:
            price_min_indices.append(prices.iloc[i-2:i+2].idxmin())

    price_max = prices.loc[price_max_indices]
    price_min = prices.loc[price_min_indices]
    max_min = pd.concat([price_max, price_min]).sort_index()
    max_min = max_min[~max_min.duplicated()]  # Remove duplicates

    # Assign types
    max_min_types = pd.Series(data=['max']*len(price_max_indices) + ['min']*len(price_min_indices), 
                             index=price_max_indices + price_min_indices)
    max_min_types = max_min_types.sort_index()

    return smooth_prices, smooth_prices_max_indices, smooth_prices_min_indices, \
           price_max_indices, price_min_indices, max_min, max_min_types




def plot_window(dates, prices, smooth_prices, 
                smooth_prices_max_indices, smooth_prices_min_indices,
                price_max_indices, price_min_indices, 
                start, end, ax=None):
    if ax is None: fig, ax = plt.subplots(figsize=(20,10), dpi=200)

    ax.plot(dates.loc[start:end], prices.loc[start:end], label='Prices')
    ax.plot(dates.loc[start:end], smooth_prices.loc[start:end], label='Smoothed Prices', linestyle='dashed')
    ax.set_xticks(np.linspace(0, len(dates.loc[start:end]), 10))
    ax.tick_params(axis='x', rotation=45)

    smooth_prices_max = smooth_prices.loc[smooth_prices_max_indices].loc[start:end]
    smooth_prices_min = smooth_prices.loc[smooth_prices_min_indices].loc[start:end]
    price_max = prices.loc[price_max_indices].loc[start:end]
    price_min = prices.loc[price_min_indices].loc[start:end]

    ax.scatter(dates.loc[smooth_prices_max.index], smooth_prices_max.values, s=20, color='red', label='Smoothed Prices Maxima')
    ax.scatter(dates.loc[smooth_prices_min.index], smooth_prices_min.values, s=20, color='purple', label='Smoothed Prices Minima')

    ax.scatter(dates.loc[price_max.index], price_max.values, s=50, color='green', label='Prices Maxima')
    ax.scatter(dates.loc[price_min.index], price_min.values, s=50, color='blue', label='Prices Minima')
    ax.legend(fontsize='small')
    ax.grid()



def find_patterns(max_min, max_min_types):
    patterns = defaultdict(list)
    last_pattern_end = None  # Track the end of the last detected pattern

    for i in range(10, len(max_min)):  # Using a window size of 10
        window = max_min.iloc[i-10:i]
        window_types = max_min_types.iloc[i-10:i]

        # Exclude overlapping patterns
        if last_pattern_end and window.index[0] <= last_pattern_end + 10:
            continue

        # Ensure the pattern occurs within a specified time frame
        if window.index[-1] - window.index[0] > 35:
            continue

        # Extract the first five points in the window
        e1, e2, e3, e4, e5 = window.iloc[:5]
        e1_type, e2_type, e3_type, e4_type, e5_type = window_types.iloc[:5]
        rtop_g1 = np.mean([e1, e3, e5])
        rtop_g2 = np.mean([e2, e4])

        # Existing Patterns
        # Head and Shoulders
        if (e1 > e2) and (e3 > e1) and (e3 > e5) and \
           (abs(e1 - e5) <= 0.03 * np.mean([e1, e5])) and \
           (abs(e2 - e4) <= 0.03 * np.mean([e1, e5])):
            patterns['HS'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Inverse Head and Shoulders
        elif (e1 < e2) and (e3 < e1) and (e3 < e5) and \
             (abs(e1 - e5) <= 0.03 * np.mean([e1, e5])) and \
             (abs(e2 - e4) <= 0.03 * np.mean([e1, e5])):
            patterns['IHS'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Broadening Top
        elif (e1 > e2) and (e1 < e3) and (e3 < e5) and (e2 > e4):
            patterns['BTOP'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Broadening Bottom
        elif (e1 < e2) and (e1 > e3) and (e3 > e5) and (e2 < e4):
            patterns['BBOT'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Triangle Top
        elif (e1 > e2) and (e1 > e3) and (e3 > e5) and (e2 < e4):
            patterns['TTOP'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Triangle Bottom
        elif (e1 < e2) and (e1 < e3) and (e3 < e5) and (e2 > e4):
            patterns['TBOT'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Rectangle Top
        elif (e1 > e2) and (abs(e1 - rtop_g1)/rtop_g1 < 0.0075) and \
             (abs(e3 - rtop_g1)/rtop_g1 < 0.0075) and (abs(e5 - rtop_g1)/rtop_g1 < 0.0075) and \
             (abs(e2 - rtop_g2)/rtop_g2 < 0.0075) and (abs(e4 - rtop_g2)/rtop_g2 < 0.0075) and \
             (min(e1, e3, e5) > max(e2, e4)):
            patterns['RTOP'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Rectangle Bottom
        elif (e1 < e2) and (abs(e1 - rtop_g1)/rtop_g1 < 0.0075) and \
             (abs(e3 - rtop_g1)/rtop_g1 < 0.0075) and (abs(e5 - rtop_g1)/rtop_g1 < 0.0075) and \
             (abs(e2 - rtop_g2)/rtop_g2 < 0.0075) and (abs(e4 - rtop_g2)/rtop_g2 < 0.0075) and \
             (max(e1, e3, e5) > min(e2, e4)):
            patterns['RBOT'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Ascending Triangle
        elif (abs(e1 - e3) / rtop_g1 < 0.03) and (abs(e3 - e5) / rtop_g1 < 0.03) and (e2 < e4):
            patterns['ATRI'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Descending Triangle
        elif (abs(e2 - e4) / rtop_g1 < 0.03) and (e1 > e3) and (e3 > e5):
            patterns['DTRI'].append((window.index[0], window.index[-1]))
            last_pattern_end = window.index[-1]

        # Pennant
        elif (e1 > e3 > e5) and (e2 < e4):
            slope_highs = (e5 - e1) / (window.index[-1] - window.index[0])
            slope_lows = (e4 - e2) / (window.index[-1] - window.index[0])

            # Check if slopes are converging (similar magnitude but opposite signs)
            if abs(slope_highs) > 0.001 and abs(slope_lows) > 0.001 and \
               abs(abs(slope_highs) - abs(slope_lows)) < 0.005:
                patterns['PN'].append((window.index[0], window.index[-1]))
                last_pattern_end = window.index[-1]


    return patterns


def visualize_patterns(dates, prices, smooth_prices, 
                       smooth_prices_max_indices, smooth_prices_min_indices, 
                       price_max_indices, price_min_indices, 
                       patterns):
    for name, end_day_nums in patterns.items():
        print('Pattern Identified: {} \nNumber of Observations: {}'.format(name, len(end_day_nums)))
        rows = int(np.ceil(len(end_day_nums)/2))
        fig, axes = plt.subplots(rows, 2, figsize=(20,5*rows), dpi=200)
        fig.subplots_adjust(hspace=0.5)
        axes = axes.flatten()
        i = 0
        for start_date, end_date in end_day_nums:
            plot_window(dates, prices, smooth_prices, 
                smooth_prices_max_indices, smooth_prices_min_indices,
                price_max_indices, price_min_indices, 
                start=start_date-1, end=end_date+1, ax=axes[i])
            i += 1
        plt.show()

#print("VISUALIZING PATTERNS")
#visualize_patterns(dates, prices, smooth_prices, 
                       #smooth_prices_max_indices, smooth_prices_min_indices, 
                       #price_max_indices, price_min_indices, 
                       #patterns)


def visualize_all_patterns(dates, prices, patterns):
    fig, ax = plt.subplots(figsize=(20, 10), dpi=200)

    # Plot the prices
    ax.plot(dates, prices, label='Prices', color='black', linewidth=1)
    ax.set_xticks(np.arange(0, len(dates), 120))  # Adjusting xticks for minute data
    ax.tick_params(axis='x', rotation=45)

    # Define marker styles for each pattern type, including the new ones
    markers = {
        'HS': 'o', 'IHS': '^', 'BTOP': 's', 'BBOT': 'P', 
        'TTOP': 'X', 'TBOT': 'D', 'RTOP': '*', 'RBOT': 'v',
        'PN': '8'  # New markers for Pennant
    }

    colors = {
        'HS': 'cyan', 'IHS': 'orange', 'BTOP': 'pink', 'BBOT': 'yellow', 
        'TTOP': 'magenta', 'TBOT': 'lime', 'RTOP': 'brown', 'RBOT': 'black',
        'PN': 'blue', # New colors for Pennant 
    }

    # To keep track of which labels have been added to the legend
    added_labels = set()

    # Loop through patterns and plot markers and bounding boxes
    for pattern_name, pattern_instances in patterns.items():
        for start_idx, end_idx in pattern_instances:
            # Calculate the midpoint for marker placement
            midpoint = (start_idx + end_idx) // 2

            # Plot the marker
            ax.scatter(
                dates.loc[midpoint], prices.loc[midpoint], 
                s=100, marker=markers.get(pattern_name, 'x'), 
                color=colors.get(pattern_name, 'grey'), 
                label=pattern_name if pattern_name not in added_labels else None
            )
            if pattern_name not in added_labels:
                added_labels.add(pattern_name)

            # Determine the window for the bounding box
            window_dates = dates.loc[start_idx:end_idx]
            window_prices = prices.loc[start_idx:end_idx]

            # Get the min and max prices within the window
            min_price = window_prices.min()
            max_price = window_prices.max()

            # Define the rectangle parameters
            start_date = window_dates.iloc[0]
            end_date_val = window_dates.iloc[-1]

            # Create a rectangle patch
            rect = patches.Rectangle(
                (start_date, min_price),  # (x,y)
                end_date_val - start_date,  # width
                max_price - min_price,      # height
                linewidth=2,
                edgecolor=colors.get(pattern_name, 'grey'),
                facecolor=colors.get(pattern_name, 'grey'),
                alpha=0.2  # Transparency
            )

            # Add the rectangle to the plot
            ax.add_patch(rect)

    # Create a custom legend to avoid duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='upper left', fontsize='small')

    ax.grid()
    plt.show()



if __name__ == "__main__":
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    stock_code = 'AAPL' # e.g. AMZN, GOOG, FB, NVDA
    print("PROCESSING DATA")

    #df, prices, dates = preprocess_data(start_date, end_date, stock_code)

    df, prices, dates = preprocess_data(stock_code)

    print("SETTING PRICE INDEXES")
    # set the index from 1 for Nadaraya-Watson kernel regression
    prices.index = np.linspace(1, len(prices), len(prices))
    dates.index = np.linspace(1, len(dates), len(dates))

    print("FINDING MAX AND MIN OF PRICES")
    smooth_prices, smooth_prices_max_indices, smooth_prices_min_indices, \
    price_max_indices, price_min_indices, max_min, max_min_types = find_max_min(prices)

    fig, ax = plt.subplots(figsize=(20,10), dpi=200)

    ax.plot(dates, prices, label='Prices')
    ax.plot(dates, smooth_prices, label='Smoothed Prices', linestyle='dashed')
    ax.set_xticks(np.arange(0, len(dates), 30))
        
    smooth_prices_max = smooth_prices.loc[smooth_prices_max_indices]
    smooth_prices_min = smooth_prices.loc[smooth_prices_min_indices]
    price_max = prices.loc[price_max_indices]
    price_min = prices.loc[price_min_indices]

    ax.scatter(dates.loc[smooth_prices_max.index], smooth_prices_max.values, s=20, color='red', label='Smoothed Prices Maxima')
    ax.scatter(dates.loc[smooth_prices_min.index], smooth_prices_min.values, s=20, color='purple', label='Smoothed Prices Minima')

    ax.scatter(dates.loc[price_max.index], price_max.values, s=50, color='green', label='Prices Maxima')
    ax.scatter(dates.loc[price_min.index], price_min.values, s=50, color='blue', label='Prices Minima')
    ax.legend(loc='upper left')
    ax.grid()

    plot_window(dates, prices, smooth_prices, 
            smooth_prices_max_indices, smooth_prices_min_indices,
            price_max_indices, price_min_indices, 
            start=18, end=34, ax=None)
    
    print("FINDING PATTERNS")
    patterns = find_patterns(max_min, max_min_types)
    patterns

    print("VISAULZING ALL PATTERNS")
    visualize_all_patterns(dates, prices, patterns)