# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 07:05:15 2024

@author: tom
"""

import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tabulate import tabulate

# Helper Functions to prepare our data
def align_data(df, values):
    """Align values with the dataframe and fill missing values."""
    series = pd.Series(values, index=df.index[-len(values):])
    series = series.reindex(df.index, method='ffill')
    series.fillna(method='bfill', inplace=True)
    return series

def get_backtest_data(cerebro, strategy_class):
    """Extract price data and strategy results from a backtest."""
    results = cerebro.run()
    if not results:
        print("Error: Backtest didn't produce any results.")
        return None, None, None
    
    strategy = results[0]
    data = strategy.datas[0]
    
    df = pd.DataFrame({
        'open': data.open.array,
        'high': data.high.array,
        'low': data.low.array,
        'close': data.close.array,
        'volume': data.volume.array
    }, index=pd.to_datetime([bt.num2date(x) for x in data.datetime.array]))
    
    if hasattr(strategy, 'sma'):
        df['sma'] = align_data(df, strategy.sma.array)
    else:
        print("Warning: Strategy doesn't have 'sma' attribute.")
    
    if hasattr(strategy, 'portfolio_value'):
        df['portfolio_value'] = align_data(df, strategy.portfolio_value)
    else:
        print("Warning: Strategy doesn't have 'portfolio_value' attribute.")
        df['portfolio_value'] = cerebro.broker.getvalue()
    
    # Calculate profit/loss
    df['pnl'] = df['portfolio_value'] - df['portfolio_value'].iloc[0]
    
    buys = pd.DataFrame(getattr(strategy, 'buys', []), columns=['date', 'price'])
    sells = pd.DataFrame(getattr(strategy, 'sells', []), columns=['date', 'price'])
    
    return df, buys, sells

# Cerebro instance containing Trading Strategy
class SimpleStrategy(bt.Strategy):
    params = (
        ('sma_period', 20),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)
        self.order = None
        self.buys = []
        self.sells = []
        self.portfolio_value = [self.broker.getvalue()]
        self.trade_log = []

    def next(self):
        current_value = self.broker.getvalue()
        self.portfolio_value.append(current_value)
        
        if self.order:
            return  # We have a pending order, don't do anything
        
        if not self.position:  # We don't have a position
            if self.data.close[0] > self.sma[0]:
                available_cash = self.broker.getcash()
                max_size = int(available_cash / self.data.close[0])
                self.order = self.buy(size=max_size)
                self.buys.append((self.data.datetime.date(0), self.data.close[0]))
                self.log_trade("BUY", current_value, max_size)
        else:  # We have an active position
            if self.data.close[0] < self.sma[0]:
                self.order = self.sell(size=self.position.size)
                self.sells.append((self.data.datetime.date(0), self.data.close[0]))
                self.log_trade("SELL", current_value, self.position.size)

    def log_trade(self, order_type, value, size):
        self.trade_log.append({
            'date': self.data.datetime.date(0),
            'type': order_type,
            'price': self.data.close[0],
            'size': size,
            'portfolio_value': value,
            'position': self.position.size if self.position else 0
        })
        
# Load data and Cerebro setup
try:
    data = pd.read_csv('AGIX.csv', parse_dates=['date'], index_col='date')
except FileNotFoundError:
    print("Error: AGIX.csv file not found. Please ensure the file is in the correct directory.")
    exit(1)

# Create a Cerebro instance
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(bt.feeds.PandasData(dataname=data))

# Add strategy to Cerebro
cerebro.addstrategy(SimpleStrategy)

# Set initial cash
initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)
    
# Run the backtest
results = cerebro.run()
strategy = results[0]

# Extract data and results
df, buys, sells = get_backtest_data(cerebro, SimpleStrategy)

if df is None:
    print("Error: Failed to extract backtest data. Exiting.")
    exit(1)

# Print debug information
print("DataFrame shape:", df.shape)
print("DataFrame columns:", df.columns)
print("Number of buy signals:", len(buys))
print("Number of sell signals:", len(sells))

# Create plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

# Top subplot: AGIX price and SMA
ax1.plot(df.index, df['close'], label='Close Price')
ax1.plot(df.index, df['sma'], label='SMA20')
ax1.set_title('AGIX Price and Trading Signal')
ax1.set_ylabel('Price (ADA)')
ax1.grid(True)
ax1.legend()

# Bottom subplot: Account value, trades, and profit/loss
ax2.plot(df.index, df['portfolio_value'], label='Profit and Loss', color='blue')
#ax2.plot(df.index, df['pnl'], label='Profit/Loss', color='green')
ax2.set_title('Account Performance')
ax2.set_ylabel('Account balance (ADA)')
ax2.grid(True)
ax2.legend(loc='upper left')

# Add buy/sell markers to both subplots
for ax in [ax1, ax2]:
    if not buys.empty:
        ax.scatter(buys['date'], buys['price'], marker='^', color='g', s=100, label='Buy')
    if not sells.empty:
        ax.scatter(sells['date'], sells['price'], marker='v', color='r', s=100, label='Sell')

# Adjust y-axis limits for the bottom subplot
portfolio_min = df['portfolio_value'].min()
portfolio_max = df['portfolio_value'].max()
y_range = portfolio_max - portfolio_min
y_padding = y_range * 0.1  # Add 10% padding
ax2.set_ylim(portfolio_min - y_padding, portfolio_max + y_padding)

# Add horizontal line for initial cash in bottom subplot
ax2.axhline(y=initial_cash, color='r', linestyle='--', label='Initial Cash')

# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()  # Rotation

# Adjust layout and display the plot
plt.tight_layout()
plt.show()

# Print trade log
print("\nDetailed Trade Log:")
for trade in strategy.trade_log:
    print(f"Date: {trade['date']}, Type: {trade['type']}, Price: ${trade['price']:.2f}, "
          f"Size: {trade['size']}, Portfolio Value: ${trade['portfolio_value']:.2f}, "
          f"Position: {trade['position']}")

# Create and print summary table
print("\nTrade Summary Table:")
table_data = [
    [trade['date'], trade['type'], f"${trade['price']:.2f}", trade['size'],
     f"${trade['portfolio_value']:.2f}", trade['position']]
    for trade in strategy.trade_log
]
headers = ["Date", "Type", "Price", "Size", "Portfolio Value", "Position"]
print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Print final results
final_value = df['portfolio_value'].iloc[-1]
total_pnl = df['pnl'].iloc[-1]
print(f'\nFinal Portfolio Value: ${final_value:.2f}')
print(f'Total Profit/Loss: ${total_pnl:.2f}')
print(f'Total Return: {(final_value - initial_cash) / initial_cash:.2%}')