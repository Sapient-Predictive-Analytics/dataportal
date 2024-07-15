# -*- coding: utf-8 -*-
"""
Sapient Dataportal
@author: tom
"""
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator

# Read the CSV file
df = pd.read_csv('IAG.csv', parse_dates=['date'], index_col='date')

# Ensure the index is sorted
df = df.sort_index()

# Rename columns to match mplfinance requirements
df = df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})

# Define custom style
mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)

# Create the candlestick chart with volume
fig, axes = mpf.plot(df, type='candle', style=s, volume=True, figsize=(16, 10),
                     title='IAG Toekn Price (ADA) and Volume',
                     ylabel='Price (ADA)',
                     ylabel_lower='Volume',
                     returnfig=True)

ax1, ax2 = axes  # ax1 is the price axis, ax2 is the volume axis

# Format date on x-axis
locator = AutoDateLocator()
ax2.xaxis.set_major_locator(locator)
ax2.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()  # Rotate and align the tick labels

# Set x-axis limits to match the data range
ax1.set_xlim(df.index[0], df.index[-1])

# Adjust layout and display the plot
plt.tight_layout()
plt.show()

# Print the first few rows and data types for debugging
print(df.head())
print(df.dtypes)
print(f"Date range: {df.index[0]} to {df.index[-1]}")