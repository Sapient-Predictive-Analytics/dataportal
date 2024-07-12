# Introduction to Backtesting Trading Strategies with Python open source libraries Backtrader and Zipline

Backtesting is a crucial step in developing and validating trading strategies. It allows traders and investors to simulate how their strategies would have performed in the past using historical data. This process helps in identifying potential flaws and strengths in the strategy before risking real money. With the rise of algorithmic trading, backtesting has become indispensable for traders who want to ensure their strategies are robust and profitable.

In this guide, we will explore the fundamentals of backtesting, particularly focusing on using Backtrader and Zipline. Although our primary interest is in investing in Cardano native tokens, the principles discussed here apply to any tradable asset and can be tested in more liquid markets like ADA/USD where an investment edge is less likely but more data and much lower cost of trading and slippage exist to validate our setup and tools. Following from our [casestudy](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/casestudy) we use World Mobile Token WMT data where possible.

Getting started is easiest with Backtrader which is the simpler of the two libraries and because it started out as an open source project, is less dependent on external support or APIs. Backtesting can be challenging due to its dependencies and outdated or community maintained documentation, as the investment community has an obvious interest to not level the playing field. We try to cover several options and local environment and container usage to provide an easy to follow step-by-step guide to set up and run a simple backtest using our own native token [CSV timeseries](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/tokens) data.

Let's start with the most obvious question.

## Why Bother with Backtesting Trading Strategies in the first place?

Backtesting offers several benefits that make it an essential practice for both novice and experienced traders:

1. **Validation of Strategies**: By testing a strategy against historical data, traders can validate its effectiveness. This helps in understanding how the strategy would have performed under various market conditions.
2. **Risk Management**: Backtesting can reveal potential risks and drawdowns in a strategy. This information is crucial for risk management and helps in adjusting the strategy to minimize potential losses.
3. **Performance Metrics**: Traders can derive various performance metrics such as Sharpe ratio, maximum drawdown, and total return from backtesting results. These metrics provide insights into the risk-adjusted returns of the strategy.
4. **Improvement and Optimization**: Backtesting allows for continuous improvement and optimization of trading strategies. Traders can tweak and refine their strategies based on backtesting results to enhance performance.
5. **Confidence Building**: By seeing a strategy perform well historically, traders gain confidence in deploying it in live markets. This psychological benefit is particularly important in trading, where discipline and confidence play significant roles.

## Benefits for Different Types of Investors

Backtesting is not just for day traders. Long-term investors can also reap significant benefits from backtesting:

- **Day Traders**: For day traders, backtesting helps in fine-tuning short-term strategies and identifying profitable entry and exit points.
- **Swing Traders**: Swing traders can use backtesting to develop strategies that capitalize on medium-term price movements, optimizing trade timing and risk management.
- **Long-Term Investors**: Long-term investors can backtest strategies that involve holding assets for extended periods. This helps in understanding the potential long-term performance and risk of the strategy.

## Setting Up the Environment

### Set up a virtual environment: 
First, create a new directory for your project and set up a virtual environment:
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

## Getting coding

Let's build the program from scratch, step by step with a really simple strategy: the 20 day moving average. When the price of WMT token is above, we hold a position, and if it is below, we don't. 

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
data = pd.read_csv('AGIX.csv', parse_dates=['date'])
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


## Conclusion
Backtesting is a powerful tool that can significantly improve trading and investment strategies. By simulating trades on historical data, you can identify strengths and weaknesses in your approach, manage risk more effectively, and optimize performance. Whether you are a day trader or a long-term investor, backtesting provides valuable insights that can enhance your decision-making process.

Using Python's Zipline library, you can easily implement and test your strategies. With the proper setup through Anaconda or Miniconda, you will have a robust environment to develop and refine your trading algorithms.
