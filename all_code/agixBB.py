
"""
Created on Thu Aug 21 08:30:23 2024

@author: tom

Bollinger Band Strategy with Candlestick Charts and Bollinger Band Plots
This script implements a trading strategy based on Bollinger Bands, runs backtests for various parameter combinations,
and creates both candlestick charts with Bollinger Bands and 3D surface plots to visualize the results.
"""

import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.dates import DateFormatter, AutoDateLocator
from matplotlib.colors import LinearSegmentedColormap

# Bollinger Band Indicator
class BollingerBandIndicator(bt.Indicator):
    lines = ('mid', 'top', 'bot')
    params = (('period', 20), ('devfactor', 2),)

    def __init__(self):
        self.data_close = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(self.data_close, period=self.params.period)
        self.stddev = bt.indicators.StandardDeviation(self.data_close, period=self.params.period)
        self.lines.mid = self.sma
        self.lines.top = self.sma + self.stddev * self.params.devfactor
        self.lines.bot = self.sma - self.stddev * self.params.devfactor

# Bollinger Band Strategy
class BollingerBandStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2))

    def __init__(self):
        self.bollinger = BollingerBandIndicator(self.data, period=self.params.period, devfactor=self.params.devfactor)
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data.close[0] < self.bollinger.bot[0]:
                self.order = self.buy()
        else:
            if self.data.close[0] > self.bollinger.top[0]:
                self.order = self.sell()

    def stop(self):
        self.final_value = self.broker.getvalue()

# Function to run a single backtest with given parameters
def run_backtest(data, period, devfactor):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(BollingerBandStrategy, period=period, devfactor=devfactor)

    initial_cash = 100000.0
    cerebro.broker.setcash(initial_cash)

    print(f'Starting Portfolio Value: {initial_cash:.2f}')
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(f'Final Portfolio Value: {final_value:.2f}')
    
    return (final_value - initial_cash) / initial_cash

# Function to create candlestick chart with Bollinger Bands
def plot_candlestick_with_bb(data, period=20, devfactor=2):
    # Calculate Bollinger Bands
    data['SMA'] = data['Close'].rolling(window=period).mean()
    data['STDDEV'] = data['Close'].rolling(window=period).std()
    data['Upper'] = data['SMA'] + (data['STDDEV'] * devfactor)
    data['Lower'] = data['SMA'] - (data['STDDEV'] * devfactor)

    # Create the candlestick chart with Bollinger Bands
    apds = [mpf.make_addplot(data[['Upper', 'SMA', 'Lower']])]
    mpf.plot(data, type='candle', style='yahoo', addplot=apds, 
             title='AGIX Candlestick Chart with Bollinger Bands',
             ylabel='Price (ADA)',
             volume=True,
             figsize=(12, 8))

# Main script
if __name__ == '__main__':
    # Load data
    data = pd.read_csv('AGIX.csv', parse_dates=['date'], index_col='date')
    data = data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})

    # Plot candlestick chart with Bollinger Bands
    plot_candlestick_with_bb(data)

    # Define parameter ranges for optimization
    periods = range(10, 31, 5)  # 10, 15, 20, 25, 30
    devfactors = [1.5, 2.0, 2.5, 3.0]

    # Initialize 2D array to store results
    results = np.zeros((len(periods), len(devfactors)))

    print("Running backtests...")
    total_combinations = len(periods) * len(devfactors)
    completed_combinations = 0

    # Run backtests for all parameter combinations
    for i, period in enumerate(periods):
        for j, devfactor in enumerate(devfactors):
            print(f"\nRunning backtest for Period: {period}, Deviation Factor: {devfactor:.2f}")
            return_value = run_backtest(data, period, devfactor)
            results[i, j] = return_value
            
            completed_combinations += 1
            progress = completed_combinations / total_combinations * 100
            print(f"Progress: {progress:.2f}%")

    print("Backtests completed.")

    # Create custom colormap for plotting
    colors = ['darkred', 'red', 'orange', 'yellow', 'lightgrey', 'lightgreen', 'darkgreen']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

    # Create surface plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(devfactors, periods)
    surf = ax.plot_surface(X, Y, results, cmap=cmap, edgecolor='none', alpha=0.8)

    ax.set_xlabel('Deviation Factor')
    ax.set_ylabel('Period')
    ax.set_zlabel('Return')
    ax.set_title('Bollinger Band Strategy Returns')

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.tight_layout()
    plt.show()

    # Print sample results
    print("\nSample Results:")
    print("Period, Deviation Factor, Return")
    for i in range(len(periods)):
        for j in range(len(devfactors)):
            print(f"{periods[i]}, {devfactors[j]:.2f}, {results[i,j]:.4f}")

    # Save results to a file
    np.save('bollinger_band_strategy_results.npy', results)
    print("\nResults saved to 'bollinger_band_strategy_results.npy'")