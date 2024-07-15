# Our Heatmap Tool for Strategy Factor Optimization

![Barracuda](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/zHero.png)

**Introduction**

The Heatmap Tool is a visualization technique we use to fine-tune and optimize our trading strategies. It provides a color-coded grid representation of strategy performance across various parameter combinations, allowing traders and analysts to quickly identify optimal settings and understand the strategy's sensitivity to different parameters. More importantly, it allows the identification of *safe areas* where the change of one or several indicators does not affect the results much, and areas that are highly likely to produce data mining bias and spurious simulation results where we have a maximum simulation profit, very close to much worse performance. This kind of tweaking has to be avoided at all costs, as it will not lead to reproducible market edge.

## How It Works

1. **Parameter Space Definition**: Define the ranges of parameters you want to test for your strategy.
2. **Backtesting**: Run the trading strategy multiple times, each with a different combination of parameters.
3. **Performance Calculation**: Calculate a performance metric (e.g., total return, Sharpe ratio) for each parameter combination.
4. **Visualization**: Create a heatmap where each cell represents a parameter combination, and the color intensity represents the performance metric.

## Using the Heatmap Tool to Fine-tune Trading Strategies

1. **Parameter Sensitivity Analysis**: 
   - Observe how changes in parameters affect strategy performance.
   - Identify which parameters have the most significant impact on results.

2. **Optimal Parameter Selection**:
   - Quickly spot the best-performing parameter combinations.
   - Understand the trade-offs between different parameter settings.

3. **Robustness Testing**:
   - Assess how sensitive the strategy is to small changes in parameters.
   - Identify stable regions where performance is consistently good across nearby parameter values.

4. **Multi-dimensional Optimization**:
   - Visualize the interplay between two or more strategy parameters simultaneously.
   - Understand complex relationships that may not be apparent from one-dimensional analysis.

5. **Strategy Comparison**:
   - Compare multiple strategies by creating heatmaps for each and analyzing their performance landscapes.

6. **Overfitting Detection**:
   - Identify suspiciously small areas of high performance, which may indicate overfitting.

7. **Time-based Analysis**:
   - Create multiple heatmaps for different time periods to assess strategy consistency.

## Why Seaborn is Ideal for Heatmap Visualization
Seaborn, a statistical data visualization library built on top of matplotlib, is particularly well-suited for creating heatmaps in trading strategy analysis:

1. **Ease of Use**: 
   - Seaborn provides a high-level interface for creating complex visualizations with minimal code.
   - It integrates seamlessly with pandas DataFrames, making it easy to work with financial data.

2. **Aesthetic Appeal**:
   - Seaborn's default styles are visually appealing and publication-quality.
   - It offers a variety of color palettes optimized for different types of data and perceptual tasks.

3. **Flexibility**:
   - Supports various data structures and can easily handle both 2D and higher-dimensional data.
   - Allows for customization of almost every aspect of the plot.

4. **Statistical Functionality**:
   - Built-in support for visualizing statistical relationships, which is crucial for financial data analysis.

5. **Color Mapping**:
   - Offers advanced color mapping capabilities, allowing for intuitive representation of complex data.
   - Supports diverging color maps, which are useful for representing both positive and negative returns.

6. **Annotation Options**:
   - Easy to add value annotations to each cell in the heatmap, enhancing readability.

7. **Integration with Matplotlib**:
   - Being built on matplotlib, it allows for further customization when needed.

Website and Installation
[**Seaborn**](https://seaborn.pydata.org)
Seaborn is a Python data visualization library based on Matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics. It is particularly useful for making complex visualizations from data in pandas DataFrames. Seaborn arguably looks better and requires less code than Matplotlib, but lacks some cutomization features of its older sibling. When DataFrames are used instead of spreadsheets for Fund data, plotting with Seaborn would be particularly easy and attractive.

`Installation:`
~~~~
pip install seaborn
~~~~

Open Source Status: BSD-3-Clause license.

[Seaborn GitHub](https://github.com/mwaskom/seaborn)

`Example of a scatterplot:`

![Seaborn Plots](https://seaborn.pydata.org/_images/scatterplot_sizes.png)

***

## Adding Heatmap to our WMT Backtest
For the backtesting previously done for a SMA20 strategy, we can implement it as a primitive to establish how the tool work. Note that for 1-dimensional strategies it is relatively pointness. Nevertheless, it shows from scratch how the setup is done.

1. It keeps the original SimpleStrategy class intact.
2. It adds a run_backtest function to run the strategy for a single SMA period and return the performance.
3. It runs the backtest for SMA periods from 13 to 27 and creates a heatmap of the returns.
4. After the heatmap, it runs a detailed backtest with SMA 20 (as in the original script) and provides the detailed output and visualization.
5. Finally, it prints the best performing SMA period based on the heatmap results.

This is the additional code:

~~~
import seaborn as sns

# Main script
data = pd.read_csv('AGIX.csv', parse_dates=['date'], index_col='date')

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

# Print the best performing SMA period
best_sma = sma_range[np.argmax(returns)]
best_return = max(returns)
print(f"\nBest performing SMA period: {best_sma}")
print(f"Best return: {best_return:.2%}")
~~~

This produces the following 1D-heatmap for WMT.

![Plot](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Heatmap1D.png)

To show more meaningful features of the Heatmap, traders usually use trading strategies that have 2 or 3 degrees of freedom where factors can be plotted over a 2D area or 3D space that is easy to process for the human brain but possesses enough complexity to justify use of such a tool. Let's refine the earlier SMA20 single factor trading signal to now be a Moving Average Crossover of the 10 and 30 day moving averages, so there are 2 factors to optimize in relation to one another that we can plot as 2-Dimensions.

The new script needs to:

1. Implements a MACrossoverStrategy class that uses two moving averages for generating buy/sell signals.
2. Runs backtests for all combinations of short-term and long-term moving averages as specified.
3. Creates a 2D heatmap showing the returns for each combination.
4. Identifies the best performing combination of short-term and long-term moving averages.
5. Runs a detailed backtest using the best performing parameters.
6. Prints out a trade summary table and overall performance metrics for the best strategy.

[IPython Notebook for the 2 Factor Strategy and Heatmap](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/MAcrossOver.ipynb)

The heatmap will show 81 unique values (9x9 grid) with varying shades of green representing the returns for each combination of short-term and long-term moving averages.
This approach allows you to visualize the performance across different parameter combinations and then dive into the details of the best-performing strategy. You can easily modify the short_range and long_range lists if you want to experiment with different moving average periods.

This is how the plot looks like now, tweaking two factors instead of one on a Seaborn Heatmap.

![Plot](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Heatmap2D.png)

Also refer to our section on [Backtesting](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/backtesting.md) for the Python scripts we use for the WMT strategies and plotting.

~~~
import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
~~~

![Swarm](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/sns_barr.jpg)
