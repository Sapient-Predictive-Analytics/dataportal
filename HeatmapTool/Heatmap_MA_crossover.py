# -*- coding: utf-8 -*-
import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as datetime
import seaborn as sns
from tabulate import tabulate

class MACrossoverStrategy(bt.Strategy):
    params = (
        ('short_period', 10),
        ('long_period', 30),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)
        
        self.order = None
        self.trade_log = []
        self.portfolio_value = []

    def next(self):
        self.portfolio_value.append(self.broker.getvalue())

        if self.order:
            return

        if not self.position:
            if self.crossover > 0:  # Short MA crosses above Long MA
                available_cash = self.broker.getcash()
                max_size = int(available_cash / self.data.close[0])
                self.order = self.buy(size=max_size)
        else:
            if self.crossover < 0:  # Short MA crosses below Long MA
                self.order = self.sell(size=self.position.size)

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log_trade("BUY", order.executed.size, order.executed.price)
            elif order.issell():
                self.log_trade("SELL", order.executed.size, order.executed.price)
        self.order = None

    def log_trade(self, order_type, size, price):
        self.trade_log.append({
            'date': self.data.datetime.date(0),
            'type': order_type,
            'price': price,
            'size': size,
            'portfolio_value': self.portfolio_value[-1],
            'position': self.position.size
        })

def run_backtest(data, short_period, long_period):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(MACrossoverStrategy, short_period=short_period, long_period=long_period)
    cerebro.broker.setcash(100000.0)
    
    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    
    return (final_value - initial_value) / initial_value

# Main script
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

# Define SMA ranges
short_range = [6, 7, 8, 9, 10, 11, 12, 13, 14]
long_range = [22, 24, 26, 28, 30, 32, 34, 36, 38]

# Run backtests for different SMA combinations
returns = np.zeros((len(short_range), len(long_range)))
for i, short_period in enumerate(short_range):
    for j, long_period in enumerate(long_range):
        returns[i, j] = run_backtest(data, short_period, long_period)

# Create 2D heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(returns, cmap="Greens", annot=True, fmt=".2%", 
            xticklabels=long_range, yticklabels=short_range)
plt.title("MA Crossover Strategy Returns Heatmap")
plt.xlabel("Long-term MA Period")
plt.ylabel("Short-term MA Period")
plt.tight_layout()
plt.show()

# Find best performing combination
best_short, best_long = np.unravel_index(np.argmax(returns), returns.shape)
best_return = returns[best_short, best_long]

print(f"\nBest performing MA combination:")
print(f"Short-term MA: {short_range[best_short]} days")
print(f"Long-term MA: {long_range[best_long]} days")
print(f"Return: {best_return:.2%}")

# Run backtest with best parameters for detailed results
cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(MACrossoverStrategy, short_period=short_range[best_short], long_period=long_range[best_long])

initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)

results = cerebro.run()
strategy = results[0]

print("\nTrade Summary Table:")
table_data = [
    [trade['date'], trade['type'], f"${trade['price']:.2f}", trade['size'],
     f"${trade['portfolio_value']:.2f}", trade['position']]
    for trade in strategy.trade_log
]
headers = ["Date", "Type", "Price", "Size", "Portfolio Value", "Position"]
print(tabulate(table_data, headers=headers, tablefmt="grid"))

final_value = strategy.portfolio_value[-1] if strategy.portfolio_value else initial_cash
total_pnl = final_value - initial_cash
total_return = (final_value - initial_cash) / initial_cash

print(f'\nInitial Portfolio Value: ${initial_cash:.2f}')
print(f'Final Portfolio Value: ${final_value:.2f}')
print(f'Total Profit/Loss: ${total_pnl:.2f}')
print(f'Total Return: {total_return:.2%}')