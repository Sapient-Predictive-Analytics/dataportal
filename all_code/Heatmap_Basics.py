# -*- coding: utf-8 -*-

import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from tabulate import tabulate

class SimpleStrategy(bt.Strategy):
    params = (
        ('sma_period', 20),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)
        self.order = None
        self.trade_log = []
        self.portfolio_value = []

    def next(self):
        market_value = self.position.size * self.data.close[0] if self.position else 0
        self.portfolio_value.append(self.broker.getcash() + market_value)

        if self.order:
            return

        if not self.position:
            if self.data.close[0] > self.sma[0]:
                available_cash = self.broker.getcash()
                max_size = int(available_cash / self.data.close[0])
                self.order = self.buy(size=max_size)
        else:
            if self.data.close[0] < self.sma[0]:
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

def run_backtest(data, sma_period):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(SimpleStrategy, sma_period=sma_period)
    cerebro.broker.setcash(100000.0)
    
    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    
    return (final_value - initial_value) / initial_value

def plot_results(data, strategy):
    # [The plot_results function remains unchanged]
    ...

# Main script
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

# Run backtests for different SMA periods
sma_range = range(13, 28)
returns = [run_backtest(data, sma) for sma in sma_range]

# Create heatmap
plt.figure(figsize=(12, 3))
sns.heatmap([returns], 
            cmap="RdYlGn", 
            center=0, 
            annot=True, 
            fmt=".2%", 
            cbar_kws={'label': 'Return'},
            xticklabels=sma_range,
            yticklabels=False)
plt.title("SMA Strategy Returns Heatmap")
plt.xlabel("SMA Period")
plt.tight_layout()
plt.show()

# Run the backtest with SMA 20 for detailed results
cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(SimpleStrategy)

initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)

results = cerebro.run()
strategy = results[0]

plot_results(data=data, strategy=strategy)

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

# Print the best performing SMA period
best_sma = sma_range[np.argmax(returns)]
best_return = max(returns)
print(f"\nBest performing SMA period: {best_sma}")
print(f"Best return: {best_return:.2%}")