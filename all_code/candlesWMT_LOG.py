# -*- coding: utf-8 -*-
"""
Sapient Dataportal
@author: tom
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def custom_log_scale(min_val, max_val):
    lower = max(0.2, np.floor(min_val * 2) / 2)
    upper = np.ceil(max_val * 2) / 2
    
    base = 2
    start = np.log(lower) / np.log(base)
    stop = np.log(upper) / np.log(base)
    ticks = np.logspace(start, stop, num=8, base=base)
    
    ticks[0] = lower
    return lower, upper, ticks

# Read the CSV file
df = pd.read_csv('~/.spyder-py3/WMT.csv', parse_dates=['date'], index_col='date')

# Ensure the index is sorted
df = df.sort_index()

# Calculate y-axis bounds
y_min = df[['low']].min().min()
y_max = df[['high']].max().max()
y_lower, y_upper, y_ticks = custom_log_scale(y_min, y_max)

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# Plot candlesticks
ax1.set_yscale('log')
ax1.set_ylim(y_lower, y_upper)

for i in range(len(df)):
    date = df.index[i]
    open, high, low, close = df.iloc[i][['open', 'high', 'low', 'close']]
    color = 'g' if close >= open else 'r'
    
    # Plot the wick
    ax1.plot([date, date], [low, high], color=color)
    
    # Plot the body
    body_bottom = min(open, close)
    body_top = max(open, close)
    body_height = body_top - body_bottom
    ax1.bar(date, body_height, bottom=body_bottom, width=0.6, color=color, align='center')

# Create a custom colormap for volume
volume_cmap = LinearSegmentedColormap.from_list("volume_cmap", ["red", "gray", "green"])

# Calculate volume color based on price change
volume_colors = np.where(df['close'] >= df['open'], 1, -1)  # 1 for green (up), -1 for red (down)

# Plot volume with color-coding
volumes = df['volume'].values
normalized_volumes = (volumes - volumes.min()) / (volumes.max() - volumes.min())
ax2.bar(df.index, df['volume'], color=volume_cmap(normalized_volumes), alpha=0.7, width=1)

# Set labels and title
ax1.set_title('WMT Token Price (ADA) and Volume', fontsize=16)
ax1.set_ylabel('ADA Price (log scale)', fontsize=12)
ax2.set_ylabel('Volume', fontsize=12)

# Set y-axis ticks and labels for price chart
ax1.set_yticks(y_ticks)
ax1.set_yticklabels([f'{x:.2f}' for x in y_ticks])

# Format date on x-axis
locator = AutoDateLocator()
ax2.xaxis.set_major_locator(locator)
ax2.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()  # Rotate and align the tick labels

# Set x-axis limits to match the exact data range
ax1.set_xlim(df.index[0], df.index[-1])

# Adjust layout and display the plot
plt.tight_layout()
plt.show()

# Print debugging information
print(f"\nDate range: {df.index[0]} to {df.index[-1]}")
print(f"Price range: {y_lower:.2f} to {y_upper:.2f}")
print(f"Y-axis ticks: {', '.join([f'{x:.2f}' for x in y_ticks])}")
print(f"\nFirst few rows of data:\n{df.head()}")
print(f"\nLast few rows of data:\n{df.tail()}")