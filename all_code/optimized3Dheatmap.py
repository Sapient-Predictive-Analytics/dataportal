# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 08:30:23 2024

@author: tom

3D Optimization for Bullish Hammer Strategy:
1. Entry: Enter a long position when a Bullish Hammer candlestick pattern is detected in a downtrend.
2. Exit: Exit the position after the specified holding period.
3. Optimize: Find the best combination of wick ratio, tail ratio, and holding period.
"""

import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import griddata
from tabulate import tabulate


class BullishHammerIndicator(bt.Indicator):
    lines = ('bullish_hammer',)
    params = (
        ('body_ratio', 0.3),
        ('wick_ratio', 2.0),
        ('tail_ratio', 2.0),
        ('trend_period', 14)
    )

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        candle = self.data
        body = abs(candle.close[0] - candle.open[0])
        wick = candle.high[0] - max(candle.open[0], candle.close[0])
        tail = min(candle.open[0], candle.close[0]) - candle.low[0]
        
        is_hammer = (body <= (candle.high[0] - candle.low[0]) * self.p.body_ratio and
                     tail >= body * self.p.tail_ratio and
                     wick <= body * self.p.wick_ratio)
        
        is_downtrend = candle.close[0] < self.trend[0] and self.trend[0] < self.trend[-1]
        
        self.lines.bullish_hammer[0] = int(is_hammer and is_downtrend and candle.close[0] > candle.open[0])

class BullishHammerStrategy(bt.Strategy):
    params = (
        ('wick_ratio', 2.0),
        ('tail_ratio', 2.0),
        ('holding_period', 7),
        ('trading_fee', 0.001),  # 0.1% trading fee
    )

    def __init__(self):
        self.bullish_hammer = BullishHammerIndicator(self.data, wick_ratio=self.params.wick_ratio, tail_ratio=self.params.tail_ratio)
        self.order = None
        self.entry_date = None
        self.entry_price = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.bullish_hammer[0]:
                available_cash = self.broker.getcash()
                max_size = int(available_cash / (self.data.close[0] * (1 + self.params.trading_fee)))
                self.order = self.buy(size=max_size)
                self.entry_date = len(self)
                self.entry_price = self.data.close[0]
        elif (len(self) - self.entry_date) >= self.params.holding_period - 1:
            self.order = self.close()

def run_backtest(data, wick_ratio, tail_ratio, holding_period):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(BullishHammerStrategy, 
                        wick_ratio=wick_ratio, 
                        tail_ratio=tail_ratio, 
                        holding_period=holding_period)
    cerebro.broker.setcash(100000.0)
    
    initial_value = cerebro.broker.getvalue()
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    
    return (final_value - initial_value) / initial_value

# Main script
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

# Define parameter ranges
wick_ratios = [0.5, 1.0, 1.5, 2.0, 2.5]
tail_ratios = [1.5, 2.0, 2.5, 3.0, 3.5]
holding_periods = [3, 5, 7, 10, 14, 20]  # Added 20-day holding period

# Run backtests for different parameter combinations
returns = np.zeros((len(wick_ratios), len(tail_ratios), len(holding_periods)))
for i, wick_ratio in enumerate(wick_ratios):
    for j, tail_ratio in enumerate(tail_ratios):
        for k, holding_period in enumerate(holding_periods):
            returns[i, j, k] = run_backtest(data, wick_ratio, tail_ratio, holding_period)

# Find best performing combination
best_indices = np.unravel_index(np.argmax(returns), returns.shape)
best_wick_ratio = wick_ratios[best_indices[0]]
best_tail_ratio = tail_ratios[best_indices[1]]
best_holding_period = holding_periods[best_indices[2]]
best_return = returns[best_indices]

print(f"\nBest performing parameter combination:")
print(f"Wick Ratio: {best_wick_ratio}")
print(f"Tail Ratio: {best_tail_ratio}")
print(f"Holding Period: {best_holding_period} days")
print(f"Return: {best_return:.2%}")

# Create custom colormap
colors = ['darkred', 'red', 'orange', 'yellow', 'lightgrey', 'lightgreen', 'darkgreen']
n_bins = 100
cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

# Create surface plots
fig = plt.figure(figsize=(20, 15))

for idx, holding_period in enumerate(holding_periods):
    ax = fig.add_subplot(2, 3, idx+1, projection='3d')
    
    X, Y = np.meshgrid(tail_ratios, wick_ratios)
    Z = returns[:, :, idx]
    
    # Create a finer mesh for smoother plot
    X_fine, Y_fine = np.meshgrid(np.linspace(min(tail_ratios), max(tail_ratios), 100),
                                 np.linspace(min(wick_ratios), max(wick_ratios), 100))
    
    # Interpolate the data on the finer mesh
    Z_fine = griddata((X.ravel(), Y.ravel()), Z.ravel(), (X_fine, Y_fine), method='cubic')
    
    # Plot the surface
    surf = ax.plot_surface(X_fine, Y_fine, Z_fine, cmap=cmap, edgecolor='none', alpha=0.8)
    
    ax.set_xlabel('Tail Ratio')
    ax.set_ylabel('Wick Ratio')
    ax.set_zlabel('Return')
    ax.set_title(f'Holding Period: {holding_period} days')
    
    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.tight_layout()
plt.suptitle('3D Surface Plots of Bullish Hammer Strategy Returns for WMT Token', fontsize=28, y=1.02)
plt.show()

# Run backtest with best parameters for detailed results
cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(BullishHammerStrategy, 
                    wick_ratio=best_wick_ratio, 
                    tail_ratio=best_tail_ratio, 
                    holding_period=best_holding_period)

initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)

results = cerebro.run()
strategy = results[0]

final_value = cerebro.broker.getvalue()
total_pnl = final_value - initial_cash
total_return = (final_value - initial_cash) / initial_cash

print(f'\nDetailed Results for Best Parameters:')
print(f'Initial Portfolio Value: ${initial_cash:.2f}')
print(f'Final Portfolio Value: ${final_value:.2f}')
print(f'Total Profit/Loss: ${total_pnl:.2f}')
print(f'Total Return: {total_return:.2%}')