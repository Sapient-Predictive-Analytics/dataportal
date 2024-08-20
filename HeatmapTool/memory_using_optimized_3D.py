# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 19:30:23 2024

@author: tom

Heatmap Simulation across 3 Dimensions: find best combination for P&L surfaces of
 - holding period
 - wick ratio
 - body ratio
 
Detailed Bullish Hammer Strategy with Independent Backtests and Visualizations
Trading Strategy:
1. Entry: Enter a long position when a Bullish Hammer candlestick pattern is detected in a downtrend.
2. Exit: Exit the position after 7 days (including the entry day).
3. Cooldown: Do not enter a new position if another Bullish Hammer occurs within x days of the last entry.
4. Position Sizing: Invest all available cash in each trade, accounting for trading fees.
"""

import backtrader as bt
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class BullishHammerIndicator(bt.Indicator):
    lines = ('bullish_hammer',)
    params = (('body_ratio', 0.3), ('wick_ratio', 2.0), ('tail_ratio', 2.0), ('trend_period', 14))

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        candle = self.data
        body = abs(candle.close[0] - candle.open[0])
        wick = candle.high[0] - max(candle.open[0], candle.close[0])
        tail = min(candle.open[0], candle.close[0]) - candle.low[0]
        total_range = candle.high[0] - candle.low[0]

        if total_range == 0:
            self.lines.bullish_hammer[0] = 0
            return

        is_hammer = (body <= total_range * self.p.body_ratio and
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
        self.bullish_hammer = BullishHammerIndicator(self.data, 
                                                     wick_ratio=self.params.wick_ratio, 
                                                     tail_ratio=self.params.tail_ratio)
        self.order = None
        self.entry_date = None
        self.exit_date = None
        self.trades = []

    def next(self):
        # Log daily values
        self.log(f'Close: {self.data.close[0]:.2f}, Portfolio Value: {self.broker.getvalue():.2f}')

        if self.order:
            return

        if not self.position:
            if self.bullish_hammer[0]:
                self.entry_date = self.data.datetime.date(0)
                self.exit_date = self.entry_date + datetime.timedelta(days=self.params.holding_period)
                
                available_cash = self.broker.getcash()
                size = int(available_cash / (self.data.open[1] * (1 + self.params.trading_fee)))
                self.order = self.buy(size=size, exectype=bt.Order.Market)
                
                self.log(f'BUY CREATE, {self.data.open[1]:.2f}')
        else:
            if self.data.datetime.date(0) >= self.exit_date:
                self.order = self.close()
                self.log(f'SELL CREATE, {self.data.close[0]:.2f}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
                
            self.trades.append({
                'entry_date': self.entry_date,
                'exit_date': self.data.datetime.date(0),
                'entry_price': self.position.price,
                'exit_price': order.executed.price,
                'profit': order.executed.pnl
            })

        self.order = None

    def stop(self):
        self.log(f'Final Portfolio Value: {self.broker.getvalue():.2f}')
        self.final_value = self.broker.getvalue()

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

def run_backtest(data, wick_ratio, tail_ratio, holding_period):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(BullishHammerStrategy, 
                        wick_ratio=wick_ratio, 
                        tail_ratio=tail_ratio, 
                        holding_period=holding_period)

    initial_cash = 100000.0
    cerebro.broker.setcash(initial_cash)

    print(f'Starting Portfolio Value: {initial_cash:.2f}')
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(f'Final Portfolio Value: {final_value:.2f}')
    
    return (final_value - initial_cash) / initial_cash

# Main script
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

# Define parameter ranges
wick_ratios = np.linspace(0.5, 3.0, 5)
tail_ratios = np.linspace(1.0, 4.0, 5)
holding_periods = [3, 5, 7, 10, 14, 20]

# Initialize 3D array to store results
results = np.zeros((len(holding_periods), len(wick_ratios), len(tail_ratios)))

print("Running backtests...")
total_combinations = len(holding_periods) * len(wick_ratios) * len(tail_ratios)
completed_combinations = 0

for i, holding_period in enumerate(holding_periods):
    for j, wick_ratio in enumerate(wick_ratios):
        for k, tail_ratio in enumerate(tail_ratios):
            print(f"\nRunning backtest for Holding Period: {holding_period}, Wick Ratio: {wick_ratio:.2f}, Tail Ratio: {tail_ratio:.2f}")
            return_value = run_backtest(data, wick_ratio, tail_ratio, holding_period)
            results[i, j, k] = return_value
            
            completed_combinations += 1
            progress = completed_combinations / total_combinations * 100
            print(f"Progress: {progress:.2f}%")

print("Backtests completed.")

# Create custom colormap
colors = ['darkred', 'red', 'orange', 'yellow', 'lightgrey', 'lightgreen', 'darkgreen']
n_bins = 100
cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

# Find overall min and max returns for consistent color scaling
overall_min_return = np.min(results)
overall_max_return = np.max(results)

# Create surface plots
fig = plt.figure(figsize=(20, 15))

for idx, holding_period in enumerate(holding_periods):
    ax = fig.add_subplot(2, 3, idx+1, projection='3d')
    
    X, Y = np.meshgrid(tail_ratios, wick_ratios)
    Z = results[idx]
    
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor='none', alpha=0.8)
    
    ax.set_xlabel('Tail Ratio')
    ax.set_ylabel('Wick Ratio')
    ax.set_zlabel('Return')
    
    ax.set_title(f'Holding Period: {holding_period} days')
    
    # Set consistent color scale
    surf.set_clim(overall_min_return, overall_max_return)
    
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.tight_layout()
plt.suptitle('WMT Token Bullish Hammer Strategy Returns Across Parameters', fontsize=28, y=1.02)
plt.show()

# Print sample results
print("\nSample Results:")
for i, holding_period in enumerate(holding_periods):
    print(f"\nHolding Period: {holding_period} days")
    print("Wick Ratio, Tail Ratio, Return")
    for j in range(2):
        for k in range(2):
            print(f"{wick_ratios[j]:.2f}, {tail_ratios[k]:.2f}, {results[i,j,k]:.4f}")

# Save results to a file
np.save('hammer_strategy_results.npy', results)
print("\nResults saved to 'hammer_strategy_results.npy'")