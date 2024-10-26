# import data tools
import talib
import pandas as pd
import numpy as np
# import plotting tools
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
# import finance data tools
import yfinance as yf


# download of stock data
start, end ,ticker = '2019-01-01', '2024-07-05', "^GDAXI"
prices = yf.download(tickers=ticker, start=start, end=end)
     
# showing all availble candle sticks
candle_names = talib.get_function_groups()['Pattern Recognition']
print(candle_names)
print(len(candle_names))

# pattern detction
harami = talib.CDLHARAMI(prices['Open'], prices['High'], prices['Low'], prices['Close'])

# data preparation for plotting
bull_harami_plot = np.where(harami>0, prices.Close,np.nan)
bear_harami_plot = np.where(harami<0, prices.Close,np.nan)


# PLotting of Data
title = f'DAX between {start} and {end}'

# plotting
fig = go.Figure()
fig.add_trace(go.Candlestick(x=prices.index, open=prices['Open'], high=prices['High'],
                             low=prices['Low'], close=prices['Close']))
fig.add_trace(go.Scatter(x=prices.index, y=bull_harami_plot, mode='markers',
                         name='bull_harami', marker_symbol='triangle-up', marker_color='yellow', marker_size=15))
fig.add_trace(go.Scatter(x=prices.index, y=bear_harami_plot, mode='markers',
                         name='bear_harami', marker_symbol='triangle-down', marker_color='lightskyblue', marker_size=15))

fig.update_layout(template='plotly_dark', autosize=False, width=1100, height=600)
fig.update_layout(title=title, xaxis_title='date', yaxis_title='prices')
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()
     
