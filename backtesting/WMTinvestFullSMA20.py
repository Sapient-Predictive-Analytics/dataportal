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

# Helper Functions to prepare the data
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

def plot_results(data, strategy):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

    portfolio_values = strategy.portfolio_value
    
    # Ensure portfolio_values has the same length as data
    if len(portfolio_values) < len(data):
        portfolio_values = [portfolio_values[0]] * (len(data) - len(portfolio_values)) + portfolio_values
    elif len(portfolio_values) > len(data):
        portfolio_values = portfolio_values[-len(data):]

    ax1.plot(data.index, data['close'], label='Close Price')
    
    # SMA20 Signal plotting
    sma_values = strategy.sma.array  # Use .array to get the SMA values
    ax1.plot(data.index, sma_values, label='SMA20')
    
    ax1.set_title('Asset Price and Trading Signal')
    ax1.set_ylabel('Price (ADA)')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(data.index, portfolio_values, label='Portfolio Value', color='green')
    ax2.set_title('Portfolio Value')
    ax2.set_ylabel('Value (ADA)')
    ax2.grid(True)
    ax2.legend()

    for trade in strategy.trade_log:
        if trade['type'] == 'BUY':
            ax1.scatter(trade['date'], trade['price'], marker='^', color='g', s=100)
            ax2.scatter(trade['date'], trade['portfolio_value'], marker='^', color='g', s=100)
        else:  # SELL
            ax1.scatter(trade['date'], trade['price'], marker='v', color='r', s=100)
            ax2.scatter(trade['date'], trade['portfolio_value'], marker='v', color='r', s=100)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
    
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
        self.trade_log = []
        self.portfolio_value = []

    def next(self):
        # Record portfolio value for each bar
        self.portfolio_value.append(self.broker.getvalue())

        # Cancel any existing order
        if self.order:
            self.cancel(self.order)

        if not self.position:  # We don't have a position
            if self.data.close[0] > self.sma[0]:
                available_cash = self.broker.getcash()
                max_size = int(available_cash / self.data.close[0])
                self.order = self.buy(size=max_size)
                self.log_trade("BUY", max_size)
        else:  # We have an active position
            if self.data.close[0] < self.sma[0]:
                self.order = self.sell(size=self.position.size)
                self.log_trade("SELL", self.position.size)

    def log_trade(self, order_type, size):
        self.trade_log.append({
            'date': self.data.datetime.date(0),
            'type': order_type,
            'price': self.data.close[0],
            'size': size,
            'portfolio_value': self.broker.getvalue(),
            'position': self.position.size if self.position else 0
        })
        
# Load data and Cerebro setup
try:
    data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')
except FileNotFoundError:
    print("Error: WMT.csv file not found. Please ensure the file is in the correct directory.")
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
# Call the plot_results function here
plot_results(data=data, strategy=strategy)

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