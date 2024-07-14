# Introduction to Backtesting Trading Strategies with Python Open Source Libraries Backtrader and Zipline

Backtesting is a crucial step in developing and validating trading strategies. It allows traders and investors to simulate how their strategies would have performed in the past using historical data. This process helps in identifying potential flaws and strengths in the strategy before risking real money. With the rise of algorithmic trading, backtesting has become indispensable for traders who want to ensure their strategies are robust and profitable.

In this guide, we will explore the fundamentals of backtesting, particularly focusing on using Backtrader and Zipline. Although our primary interest is in investing in Cardano native tokens, the principles discussed here apply to any tradable asset and can be tested in more liquid markets like ADA/USD where an investment edge is less likely but more data and much lower cost of trading and slippage exist to validate our setup and tools. Following from our [casestudy](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/casestudy) we use World Mobile Token WMT data where possible.

Getting started is easiest with Backtrader which is the simpler of the two libraries and because it started out as an open source project, is less dependent on external support or APIs. Backtesting can be challenging due to its dependencies and outdated or community maintained documentation, as the investment community has an obvious interest to not level the playing field. We try to cover several options and local environment and container usage to provide an easy to follow step-by-step guide to set up and run a simple backtest using our own native token [CSV timeseries](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/tokens) data.

Let's start with the most obvious question.

## Why bother with backtesting trading strategies in the first place?

Backtesting offers several benefits that make it an essential practice for both novice and experienced traders:

1. **Validation of Strategies**: By testing a strategy against historical data, traders can validate its effectiveness. This helps in understanding how the strategy would have performed under various market conditions.
2. **Risk Management**: Backtesting can reveal potential risks and drawdowns in a strategy. This information is crucial for risk management and helps in adjusting the strategy to minimize potential losses.
3. **Performance Metrics**: Traders can derive various performance metrics such as Sharpe ratio, maximum drawdown, and total return from backtesting results. These metrics provide insights into the risk-adjusted returns of the strategy.
4. **Improvement and Optimization**: Backtesting allows for continuous improvement and optimization of trading strategies. Traders can tweak and refine their strategies based on backtesting results to enhance performance.
5. **Confidence Building**: By seeing a strategy perform well historically, traders gain confidence in deploying it in live markets. This psychological benefit is particularly important in trading, where discipline and confidence play significant roles.

## Benefits for different types of token holders

Backtesting is not just for day traders. HODLers can also reap significant benefits from backtesting:

- **Day Traders**: For day traders, backtesting helps in fine-tuning short-term strategies and identifying profitable entry and exit points.
- **Swing Traders**: Swing traders can use backtesting to develop strategies that capitalize on medium-term price movements, optimizing trade timing and risk management.
- **Long-Term Investors**: Long-term investors can backtest strategies that involve holding assets for extended periods. This helps in understanding the potential long-term performance and risk of the strategy.

## Setting up the environment

### Set up a virtual environment: 
As a first step, it is often advisable to create a new directory for the backtesting project and set up a virtual environment. This allows sharing requirements.txt files and specifying versions of packages that may be required. As per our previous casestudy, we stick to Python 3.8. for example, whereas in our dayjobs we may be using 3.12. at the moment.

```bash
   mkdir backtest_project
   cd backtest_project
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Using Anaconda or Miniconda

To begin backtesting with Python and Backtrader, we need to set up a Python environment. Anaconda and Miniconda are popular choices for managing Python environments due to their ease of use and robust package management. Backtrader is currently not available on Anaconda natively, but we can add it through pip.

### Installing Anaconda

1. **Download Anaconda**: Visit the [Anaconda website](https://www.anaconda.com/products/distribution) and download the installer for your operating system.
2. **Install Anaconda**: Follow the installation instructions provided on the website. This process will install Anaconda Navigator, a graphical interface for managing your Python environments and packages.

### Installing Miniconda

Miniconda is a lightweight alternative to Anaconda that includes only the conda package manager and Python. It is ideal for users who prefer a minimal installation.

1. **Download Miniconda**: Visit the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and download the installer for your operating system.
2. **Install Miniconda**: Follow the installation instructions provided on the website.

### Setting Up Backtrader

**Activate base environment**

```
conda activate base
```

Install Backtrader using pip
```
pip install backtrader
```

Verify installation
```
python -c "import backtrader; print(backtrader.__version__)"
```

## How Backtrader works under the hood
Developed in 2015 by Daniel Rodriguez, Backtrader has a large and active community of individual traders, there are several banks and trading houses that use
backtrader to prototype and test new strategies. Backtrader is an entirely open source, community run project that has great documentation. You can refer to its [homepage](https://www.backtrader.com/docu/) or [Github](https://github.com/backtrader/backtrader).

It leverages Python's object oriented programming and creates a "Cerebro" (Spanish for brain) class that has backtesting functionalities as its methods.

![Cerebro infrastructure](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/cerebro.jpg)

The key components of any backtesting workflow is represented as Python objects. These objects interact with one another to facilitate processing input data and trading logic computation.  We can incorporate market factors, formulate and execute a strategy, receive and execute orders, and track and measure performance. A Cerebro instance
coordinates the overall process from collecting inputs, executing the backtest bar by bar, and providing results. The simulation supports different order types, checking a submitted order cash requirements against current cash, keeping track of cash and value for each iteration of cerebro and keeping the current position on different data. Data Feeds are provided member variables to the strategy in the form of an array and shortcuts to the array positions. Broker does not necessarily mean intermediary here but manages the financial account, like a ficticious 100,000 ADA account that is subjected to profit and loss as well as commissions and slippage from the strategy we like to test over historical data.

## Code for a simple backtest

Let's build the program from scratch, step by step with a really simple strategy: the 20 day moving average. When the price of WMT token is above, we hold a position, and if it is below, we don't. Initially, we only hold 1 WMT, so our 100,000 account will not feel much impact no matter how well the strategy performs. Later, we refine this by buying the maximum amount of tokens so the account reflects the success or failure of our strategy.

~~~
import backtrader as bt
import pandas as pd

class SimpleStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

# Create a Cerebro instance
cerebro = bt.Cerebro()
~~~

The Strategy has no methods and only initializes. Pandas is imported so we can use our own data and later run tests or portfolio analysis on it.

~~~
# Load data from CSV
data = pd.read_csv('WMT.csv', parse_dates=['date'])
data.set_index('date', inplace=True)
data.sort_index(inplace=True)  # Ensure the data is sorted by date

# Create a bt.feeds.PandasData feed
feed = bt.feeds.PandasData(
    dataname=data,
    datetime=None,  # None because we set the date as index
    open=0,  # Column position for 'open' data
    high=1,  # Column position for 'high' data
    low=2,   # Column position for 'low' data
    close=3, # Column position for 'close' data
    volume=4,# Column position for 'volume' data
    openinterest=-1  # -1 or None if no open interest data
)

# Add data feed to Cerebro
cerebro.adddata(feed)

# Add strategy to Cerebro
cerebro.addstrategy(SimpleStrategy)
~~~

Data Feeds are usually the biggest challenge for backtesting, and errors in the format or the data are most common obstacles to producing realistic trading results. In the next part of our program, we add play money of 100,000 ADA to the simulation, and run the backtest based on the definition of trading strategy. This will be refined later.

~~~
# Set initial cash
cerebro.broker.setcash(100000.0)

# Run the backtest
results = cerebro.run()

# Print final portfolio value
print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
~~~

## A more refined simple backtest

~~~
import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Helper functions
def get_indicator_data(indicator):
    """Extract indicator data as a pandas Series."""
    return pd.Series(indicator.array, index=indicator.data.datetime.datetime)

def get_backtest_data(cerebro, strategy_class):
    """Extract price data and strategy results from a backtest."""
    strategy = cerebro.runstrategy(strategy_class)[0]
    data = strategy.data0
    
    df = pd.DataFrame({
        'open': data.open.array,
        'high': data.high.array,
        'low': data.low.array,
        'close': data.close.array,
        'volume': data.volume.array
    }, index=data.datetime.datetime)
    
    df['sma'] = get_indicator_data(strategy.sma)
    df['portfolio_value'] = strategy.portfolio_value
    
    buys = pd.DataFrame(strategy.buys, columns=['date', 'price'])
    sells = pd.DataFrame(strategy.sells, columns=['date', 'price'])
    
    return df, buys, sells

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

    def next(self):
        self.portfolio_value.append(self.broker.getvalue())
        
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.order = self.buy()
                self.buys.append((self.data.datetime.date(0), self.data.close[0]))
        else:
            if self.data.close[0] < self.sma[0]:
                self.order = self.sell()
                self.sells.append((self.data.datetime.date(0), self.data.close[0]))

# Load data
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

# Create a Cerebro instance
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(bt.feeds.PandasData(dataname=data))

# Add strategy to Cerebro
cerebro.addstrategy(SimpleStrategy)

# Set initial cash
initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)

# Extract data and results
df, buys, sells = get_backtest_data(cerebro, SimpleStrategy)

# Print final portfolio value
final_value = df['portfolio_value'].iloc[-1]
print(f'Final Portfolio Value: ${final_value:.2f}')
print(f'Total Return: {(final_value - initial_cash) / initial_cash:.2%}')
~~~

## Adding plotting
Now we add Matplotlib and plot the results.
New code:
~~~
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tabulate import tabulate
~~~

These are the imports.

~~~
# Create plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

# Top subplot: WMT price and SMA
ax1.plot(df.index, df['close'], label='Close Price')
ax1.plot(df.index, df['sma'], label='SMA20')
ax1.set_title('WMT Price and Trading Signal')
ax1.set_ylabel('Price (ADA)')
ax1.grid(True)
ax1.legend()

# Bottom subplot: Account value, trades, and profit/loss
ax2.plot(df.index, df['portfolio_value'], label='Account Value', color='blue')
ax2.plot(df.index, df['pnl'], label='Profit/Loss', color='green')
ax2.set_title('Account Performance')
ax2.set_ylabel('Value (ADA)')
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
~~~

And voila, with this we can visualize whether the strategy has potential, as it shows more than just the final Profit and Loss and provides lots of clues if the variability of results, drawdown, number of trading signals and so on show promise for further refinement or we better move on and ideate on new rules for entry and exit.

![Backtest Result](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/WMT_simple_backtest.png)

## Investing the maximum
Holding and squaring 1 WMT token is obviously not going to produce meaningful results (especially when factoring in costs) so we refine the code to invest the entire account balance whenever we have a long signal. These changes are made via the *next* method which controls position flow (next meaning from first to nth signal).

~~~
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
~~~

These changes will make the strategy invest all available cash into WMT when it buys, and sell the entire position when it sells. This will equate the accout balance to the portfolio balance and produces the most meaningful results - if we want a portfolio, we can simply combine strategies. For the purpose of a single asset backtest, except when for fine tuning sizing strategies, this should lead to the most meaningful results.

When plotting, this shows a surprise: our "highly profitable" strategy no longer looks so great.

![Performance when fully invested](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/WMT_full_invest.png)

This is caused by the [*path dependence*](https://wilmott.com/path-dependence-and-volatility/) problem of Backtesting: as the first few signals are loss-making, our portfolio runs down so much that the almost 3x profit from the 2024 rally in WMT is enjoyed by a much diminished account. Had we limited our input data to the last 1 year or only have access to that much data, the strategy would look great again. The point is therefore not so much to find a "great" strategy that makes the most out of the simulated ADA account, but by having the most reliable expected profit. We will deal with this in much more detail later.

## Tracking trades and account performance
Next, we add a logging method to our Cerebro class and tabulate results using the [Tabulate](https://pypi.org/project/tabulate/) library. This is crucial to later compare and evaluate strategies quantitatively as the human eye glancing over plots only yields a certain amount of intuitive assessment.

~~~
def log_trade(self, order_type, value, size):
        self.trade_log.append({
            'date': self.data.datetime.date(0),
            'type': order_type,
            'price': self.data.close[0],
            'size': size,
            'portfolio_value': value,
            'position': self.position.size if self.position else 0
        })
~~~

And we then log and tabulate.

~~~
from tabulate import tabulate

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
~~~

## IPython notebook and video walkthrough.
This IPython notebook provides a comprehensive, step by step guide with the above program how to implement our SMA20 trading strategy as a placeholder for more sophisticated trading strategies. It is organized in 3 steps with more coding intensive tasks like Plotting added later. You can download this file together with WMT.csv for interactive use and modification.

[IPython Notebook also linked here](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/WMT%20Backtrader%20with%20Plotting.ipynb)


## Upgrading to Zipline
Backtrader and Zipline are both popular Python libraries for backtesting trading strategies, but Zipline has an arguably larger community and more professional users mainly due to its origin in Quantopian crowdsourced hedge fund that later migrated to Nasdaq Data for the API and Robinhood for the trading elements. 

There are some key differences. For data handling, Backtrader is more flexible with data inputs, while Zipline uses a specific data bundle system that benefits from "ingesting" API data. Therefore, before our API is fully production ready, Backtrader is the more lightweight and less error-prone choice.

Zipline is generally faster for large datasets due to its use of Pandas and has a larger ecosystem due to its Quantopian heritage described above.Backtrader is considered easier to learn for beginners. If you want to try out Zipline, the community page maintained by [ML4Trading](https://zipline.ml4trading.io/) is a great place to start.

Code snippets for installing and using Zipline:
~~~
pip install zipline-reloaded #conda install zipline-reloaded for Anaconda/Miniconda
~~~

The commands differ greatly from Backtrader as it does not use an object-oriented approach and runs all functions directly inside our program.

~~~
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from zipline.api import order, record, symbol
from zipline.finance import commission, slippage
from zipline import run_algorithm
from datetime import datetime
from pandas.tseries.offsets import BDay

def initialize(context):
    context.asset = symbol('WMT')
    context.sma_period = 20
    context.in_position = False
    context.portfolio_value = []

def handle_data(context, data):
    current_price = data.current(context.asset, 'price')
    historical_data = data.history(context.asset, 'close', context.sma_period, '1d')
    sma = historical_data.mean()
    
    cash = context.portfolio.cash
    position = context.portfolio.positions[context.asset].amount
    market_value = position * current_price
    portfolio_value = cash + market_value
    context.portfolio_value.append(portfolio_value)

    if not context.in_position and current_price > sma:
        shares_to_buy = int(cash / current_price)
        order(context.asset, shares_to_buy)
        context.in_position = True
    elif context.in_position and current_price < sma:
        order(context.asset, -position)
        context.in_position = False

    record(price=current_price, sma=sma, portfolio_value=portfolio_value)

def analyze(context, perf):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

    perf.index = perf.index.tz_localize(None)
    ax1.plot(perf.index, perf.price, label='Close Price')
    ax1.plot(perf.index, perf.sma, label='SMA')
    ax1.set_title('Asset Price and Trading Signal')
    ax1.set_ylabel('Price')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(perf.index, perf.portfolio_value, label='Portfolio Value', color='green')
    ax2.set_title('Portfolio Value')
    ax2.set_ylabel('Value ($)')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

    initial_value = perf.portfolio_value.iloc[0]
    final_value = perf.portfolio_value.iloc[-1]
    total_return = (final_value - initial_value) / initial_value

    print(f'Initial Portfolio Value: ${initial_value:.2f}')
    print(f'Final Portfolio Value: ${final_value:.2f}')
    print(f'Total Return: {total_return:.2%}')

def run_zipline_backtest(start_date, end_date, capital_base):
    return run_algorithm(
        start=start_date,
        end=end_date,
        initialize=initialize,
        handle_data=handle_data,
        analyze=analyze,
        capital_base=capital_base,
        bundle='csvdir',
        data_frequency='daily'
    )

if __name__ == '__main__':
    start = datetime(2022, 1, 1)
    end = datetime(2024, 6, 30)
    initial_capital = 100000.0

    results = run_zipline_backtest(start, end, initial_capital)
~~~

## More sophisticated trading strategies: candlesticks example
Coming in August 2024.

## Adding a second degree of freedom and our Heatmap tool
Currently, we are using a single factor model to decide whether to be in the market or not. This is obviously as simple as it gets, but useful to fine-tune our model later and get familiar with the different backtesting, plotting and portfolio management packages. What would happen if we used a 15-day or 25-day moving average instead of 20? Would we make more or less money? Completely by chance, the 20-day SMA that was chosen as a dummy happens to be the best game in town for World Mobile Token. How to visualize these tweaks, discussion of introducing bias and stresstesting models with simulation, and our Heatmap tool can be continued in another chapter of the Dataportal here: [HeatmapTool](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md)

A preview of how the Heatmap works and how lucky we were with the 20-day pick can be seen in this plot:
![Plot](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Heatmap1D.png)

## Summing it up
Backtesting is a powerful tool that can significantly improve trading and investment strategies. By simulating trades on historical data, we can identify strengths and weaknesses in our approach, manage risk more effectively, and optimize performance. Whether you are a day trader or a long-term investor, backtesting provides valuable insights that can enhance your decision-making process. Backtrader is an easy to use, out of the box and fully community run tool that works well on our own data. Zipline is more powerful and provides a better composable functional approach, but is harder to learn and more finnicky because of its reliance on data bundling. With Python's large selection of open source data science libraries, we have a lot of supporting tools like Matplotlib, Seaborn, Tabulate etc. at our disposal and can visualize and tweak any strategy we are curious about, or use to analyze and risk-manage native tokens. Data mining and hindsight bias lurk everywhere though, so with illiquid, relatively new or highly volatile assets like some native tokens, we need to tread carefully and only deploy ADA after we have run simulations, checked our assumptions and data and verified the integrity of the project and trading venue we choose to explore.
