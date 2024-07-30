# Refining our backtesting toolkit

So far, we have bought WMT token whenever the price was above the SMA20 line, and stayed out of the market if it wasn't. This has historically worked really well, and the heatmap looks promising insofar as changing the average period slightly does not dramatically alter trading results, a sure hallmark of spurious data mining results.

However, we need to up our game to trade other tokens, deploy money in the real world where fees and slippage can eat away profits, and take into account other risk factors we may encounter. This section and the separate chapter on [Risk](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md) will cover those aspect.

### Gradually refining our approach
It is important to move gradually with your programs to spot inconsistencies, biases and bugI've made several key changes to implement a more complex trading strategy:

Implemented a moving average crossover strategy using two Simple Moving Averages (SMA).
Added a trading fee parameter (set to 0.1% by default).
Modified the trading logic to enter when the fast MA crosses above the slow MA, and exit when it crosses below.
Updated the log_trade method to include the trading fee.
Modified the plotting function to show both moving averages.
Updated the trade summary table to include the fee for each trade.

Here's a breakdown of the main changes:

Strategy Parameters:

fast_period: The period for the fast moving average (default: 10 days)
slow_period: The period for the slow moving average (default: 30 days)
trading_fee: The percentage fee for each trade (default: 0.1%)

Trading Logic:

The strategy buys when the fast MA crosses above the slow MA.
It sells when the fast MA crosses below the slow MA.
When not in a position, it stays out of the market.

Fee Calculation:

The trading fee is now factored into each trade.
The available cash for buying is reduced by the fee amount.
The fee is logged for each trade in the trade summary.

Visualization:

The plot now shows both the fast and slow moving averages along with the close price.s early. Trading strategies can be very complex and incorporate multi-period signals and indicators. From the SMA-signal, the next level of complexity is an SMA-crossover. 
