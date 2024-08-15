# Refining our backtesting toolkit

So far, we have bought WMT token whenever the price was above the SMA20 line, and stayed out of the market if it wasn't. This has historically worked really well, and the heatmap looks promising insofar as changing the average period slightly does not dramatically alter trading results, a sure hallmark of spurious data mining results.

However, we need to up our game to trade other tokens, deploy money in the real world where fees and **slippage** can eat away profits, and take into account other risk factors we may encounter. This section and the separate chapter on [Risk](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md) will cover those aspect.

## Gradually refining our approach
It is important to move gradually with your programs to spot inconsistencies, biases and bugs. First, we need to add trading fees to realistically penalize strategies that enter and exit the market a lot and take advantage of small opportunities that are unlikely to survive **poor liquidity** or minimum **batcher fees**.

Right now, the Preprod [WingRider DEX](https://app.preprod.wingriders.com/swap) testnet assumes for an order of 10,000 ADA that 36 ADA fees will be paid and the price impact is 1.101%. So first of all, we adjust our equity to be a portfolio of 10,000 ADA that is far more realistically deployable in the native tokens universe than the previous 100,000 simulation. The total cost of getting into the position is 1.37% Traders who are used to paying 0.1 to 0.2% on Kraken or Binance exchanges for ADA, ETH or BTC may find this outrageous, but if you are trading a native token of a smaller project these currently trade only a few 1000 ADA a day on the more active DEXes. Surely, 1% slippage / market impact is a fairly optimistic assumption that only applies to the most liquid tokens like WMT, AGIX or SNEK.

To realize this basic improvement, we follow the following simple steps to our earlier Backtrader programs:
* adding a *trading_fee* parameter to the *MACrossoverStrategy* class
* modifying the *next* method (signal logic) to account for fees when calculating the maximum buy size
* adding fee calculation and logging in the *notify_order* method (or function if using zipline)
* including a *total_fees* attribute to track the total fees paid
* updating the *run_backtest* function to subtract the total fees from the final return calculation and adding a "Fee" column to the trade summary table

**Strategy Parameters**
It is fairly straight-forward to add complexity to a Backtrader program. This is done via adding strategy classes, and a large amount of classes can work together as the next method iterated over our historical data and the memory usage for each step is small.

For simplicity's sake, let us assume that we believe in the predictive power of candlestick patterns. This is unlikely to work for token data, as there are no end of day breaks that surely had a crucial psychological importance in rice markets when the indicator was conceived. Adjusting token data for illiquid "night" period and allowing gaps and differences between open and close prices could restore this predictive power, but that is up to the reader to pursue. We use candlesticks as they are clearly verifiable and well known patterns that have varying levels of complexity and can be combined and optimized easily - a perfect learning example for our Backtrader tool.

~~~
class BullishHammerIndicator(bt.Indicator):
    lines = ('bullish_hammer',)
    params = (('body_ratio', 0.3), ('wick_ratio', 2.0), ('trend_period', 14))

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        open, high, low, close = self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0]
        body = abs(close - open)
        wick = high - max(open, close)
        tail = min(open, close) - low
        
        is_hammer = (body <= (high - low) * self.p.body_ratio and
                     tail >= body * self.p.wick_ratio and
                     wick <= body * 0.1)
        
        is_downtrend = close < self.trend[0] and self.trend[0] < self.trend[-1]
        
        self.lines.bullish_hammer[0] = int(is_hammer and is_downtrend and close > open)
~~~

**Trading Logic**
Combining these classes is also easy. In the functions of the main program, we simply scan for all signals or write logic that makes use of them.

~~~
def flag_all_patterns(data):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(AdvancedDualEntryStrategy)
    results = cerebro.run()
    strategy = results[0]

    dragonfly_dojis = [data.index[i] for i, v in enumerate(strategy.dragonfly_doji.array) if v]
    bullish_hammers = [data.index[i] for i, v in enumerate(strategy.bullish_hammer.array) if v]
    bearish_hanging_men = [data.index[i] for i, v in enumerate(strategy.bearish_hanging_man.array) if v]
    
    return dragonfly_dojis, bullish_hammers, bearish_hanging_men
~~~

## Ideas for strategy improvement
As next steps, we could further refine the strategy by 

* Implementing more sophisticated position sizing
  
* Adding risk management features like stop-loss or take-profit orders
  
* Incorporating additional indicators or fundamental data, or introducing "regimes"
  
* Implementing a more complex exit strategy like trailing stops 


**Visualization**
Matplotlib allows for looping in your plot function, so trading signals can easily be inserted into the chart of the native to show entry and exit signals and other indicators. This is a great way to avoid "black box" situations where we have a highly profitable trading signal but do not fully understand why - so the risk of **spurious results**, **calculation error**, **biases** or **unrealistic assumptions** is unacceptable. 

The code for this could look something  like this:

~~~
for trade in strategy.trade_log:
        if trade['type'] == 'BUY':
            ax1.scatter(trade['date'], trade['price'], color='g', marker='^', s=100)
        else:  # SELL
            ax1.scatter(trade['date'], trade['price'], color='r', marker='v', s=100)
~~~

to show the signals defined in Backtrader classes as markers on the plot. ![Plot](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/matplotlibSignals.jpg)


**Optimization**

In real life, we probably have some sophisticated idea that involves parsing X for the comments by exposed personalities about our tokens or on-chain statistics and so on. Traditional technical patterns that only reference past price action are not very likely to provide a long term source of edge. However, for the purpose of this tutorial, they are much easier to demonstrate the open source tools on and can be refined very easily. First, we need to define the strategy in unambiguous terms that can be tested and verified. This could look something like this:

`
Trading Strategy:
1. Entry: Enter a long position when either a Dragonfly Doji or a Bullish Hammer candlestick pattern is detected in a downtrend.
2. Exit: Exit the position if any of the following conditions are met:
   a) A Bearish Hanging Man pattern occurs after entry
   b) The closing price falls below 80% of the entry price (20% stop loss)
   c) The position value doubles (100% take profit)
3. Cooldown: Do not enter a new position within 7 days of the last entry.
4. Position Sizing: Invest all available cash in each trade, accounting for trading fees.
`

Spoiler: the strategy described does not make any money across our native tokens investable universe. However, it is a good way to discuss code refinement to allow for fees and complex entry and exit logic.

![Dragonfly](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/DragonflyCandles.png)
