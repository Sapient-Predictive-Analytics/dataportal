# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:15:23 2024

@author: tom

Trading Strategy:
1. Entry: Enter a long position when either a Dragonfly Doji or a Bullish Hammer candlestick pattern is detected in a downtrend.
2. Exit: Exit the position if any of the following conditions are met:
   a) A Bearish Hanging Man pattern occurs after entry
   b) The closing price falls below 80% of the entry price (20% stop loss)
   c) The position value doubles (100% take profit)
3. Cooldown: Do not enter a new position within 7 days of the last entry.
4. Position Sizing: Invest all available cash in each trade, accounting for trading fees.
"""

import os
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tabulate import tabulate

print(os.getcwd())

class DragonflyDojiIndicator(bt.Indicator):
    lines = ('dragonfly_doji',)
    params = (('body_ratio', 0.1), ('trend_period', 14))

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        open, high, low, close = self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0]
        body = abs(close - open)
        total_range = high - low
        
        is_doji = body <= total_range * self.p.body_ratio
        is_dragonfly = is_doji and (high - max(open, close)) <= body
        
        is_downtrend = close < self.trend[0] and self.trend[0] < self.trend[-1]
        
        self.lines.dragonfly_doji[0] = int(is_dragonfly and is_downtrend)

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

class BearishHangingManIndicator(bt.Indicator):
    lines = ('bearish_hanging_man',)
    params = (('body_ratio', 0.3), ('wick_ratio', 2.0), ('trend_period', 14))

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        open, high, low, close = self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0]
        body = abs(close - open)
        wick = high - max(open, close)
        tail = min(open, close) - low
        
        is_hanging_man = (body <= (high - low) * self.p.body_ratio and
                          wick >= body * self.p.wick_ratio and
                          tail <= body * 0.1)
        
        is_uptrend = close > self.trend[0] and self.trend[0] > self.trend[-1]
        
        self.lines.bearish_hanging_man[0] = int(is_hanging_man and is_uptrend and close < open)

class AdvancedDualEntryStrategy(bt.Strategy):
    params = (
        ('trading_fee', 0.001),  # 0.1% trading fee
        ('cooldown_days', 7),    # Cooldown period after entry
        ('stop_loss_pct', 0.20), # 20% stop loss
        ('take_profit_pct', 1.0) # 100% take profit
    )

    def __init__(self):
        self.dragonfly_doji = DragonflyDojiIndicator(self.data)
        self.bullish_hammer = BullishHammerIndicator(self.data)
        self.bearish_hanging_man = BearishHangingManIndicator(self.data)
        self.order = None
        self.trade_log = []
        self.portfolio_value = []
        self.total_fees = 0
        self.entry_count = 0
        self.entry_date = None
        self.cooldown = 0
        self.stop_loss = None
        self.take_profit = None
        self.entry_price = None
        self.stop_loss_levels = []
        self.take_profit_levels = []

    def prenext(self):
        self.portfolio_value.append(self.broker.getvalue())

    def nextstart(self):
        self.next()

    def next(self):
        self.portfolio_value.append(self.broker.getvalue())

        if self.cooldown > 0:
            self.cooldown -= 1

        if self.order:
            return

        if self.position:
            if (self.bearish_hanging_man[0] or 
                self.data.close[0] <= self.stop_loss or 
                self.data.close[0] >= self.take_profit):
                self.order = self.close()
                return

        if not self.position and self.cooldown == 0 and (self.dragonfly_doji[0] or self.bullish_hammer[0]):
            available_cash = self.broker.getcash()
            max_size = int(available_cash / (self.data.close[0] * (1 + self.params.trading_fee)))
            self.order = self.buy(size=max_size)
            self.entry_count += 1
            self.entry_date = len(self)
            self.cooldown = self.params.cooldown_days
            self.entry_price = self.data.close[0]
            self.stop_loss = self.entry_price * (1 - self.params.stop_loss_pct)
            self.take_profit = self.entry_price * (1 + self.params.take_profit_pct)
            self.stop_loss_levels.append((self.data.datetime.date(0), self.stop_loss))
            self.take_profit_levels.append((self.data.datetime.date(0), self.take_profit))

    def notify_order(self, order):
        if order.status in [order.Completed]:
            fee = order.executed.value * self.params.trading_fee
            self.total_fees += fee
            if order.isbuy():
                self.log_trade("BUY", order.executed.size, order.executed.price, fee)
            elif order.issell():
                self.log_trade("SELL", order.executed.size, order.executed.price, fee)
                self.stop_loss = None
                self.take_profit = None
                self.entry_price = None
        self.order = None

    def log_trade(self, order_type, size, price, fee):
        self.trade_log.append({
            'date': self.data.datetime.date(0),
            'type': order_type,
            'price': price,
            'size': size,
            'fee': fee,
            'portfolio_value': self.portfolio_value[-1],
            'position': self.position.size
        })

def run_strategy(data):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(AdvancedDualEntryStrategy)

    initial_cash = 100000.0
    cerebro.broker.setcash(initial_cash)

    results = cerebro.run()
    return results[0]

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

def plot_results(data, strategy, dragonfly_dojis, bullish_hammers, bearish_hanging_men):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

    ax1.plot(data.index, data['close'], label='Close Price')
    
    for trade in strategy.trade_log:
        if trade['type'] == 'BUY':
            ax1.scatter(trade['date'], trade['price'], color='g', marker='^', s=100)
        else:  # SELL
            ax1.scatter(trade['date'], trade['price'], color='r', marker='v', s=100)

    ax1.scatter(dragonfly_dojis, data.loc[dragonfly_dojis, 'close'], color='blue', marker='D', s=50, alpha=0.5, label='Dragonfly Doji')
    ax1.scatter(bullish_hammers, data.loc[bullish_hammers, 'close'], color='cyan', marker='^', s=50, alpha=0.5, label='Bullish Hammer')
    ax1.scatter(bearish_hanging_men, data.loc[bearish_hanging_men, 'close'], color='orange', marker='v', s=50, alpha=0.5, label='Bearish Hanging Man')

    ax1.set_title('Indigo DAO Token and Trading Signals')
    ax1.set_ylabel('Price (ADA)')
    ax1.grid(True)
    ax1.legend()

    portfolio_values = strategy.portfolio_value
    if len(portfolio_values) < len(data):
        portfolio_values = [portfolio_values[0]] * (len(data) - len(portfolio_values)) + portfolio_values
    ax2.plot(data.index, portfolio_values, label='Portfolio Value', color='purple')
    ax2.set_title('Portfolio Value')
    ax2.set_ylabel('Value (ADA)')
    ax2.grid(True)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    
    plt.tight_layout()
    plt.show()

# Main script
data = pd.read_csv('INDY.csv', parse_dates=['date'], index_col='date')

strategy = run_strategy(data)
dragonfly_dojis, bullish_hammers, bearish_hanging_men = flag_all_patterns(data)

plot_results(data, strategy, dragonfly_dojis, bullish_hammers, bearish_hanging_men)

print("\nTrade Summary Table:")
table_data = [
    [trade['date'], trade['type'], f"${trade['price']:.2f}", trade['size'],
     f"${trade['fee']:.2f}", f"${trade['portfolio_value']:.2f}", trade['position']]
    for trade in strategy.trade_log
]
headers = ["Date", "Type", "Price", "Size", "Fee", "Portfolio Value", "Position"]
print(tabulate(table_data, headers=headers, tablefmt="grid"))

final_value = strategy.portfolio_value[-1] if strategy.portfolio_value else 100000.0
total_pnl = final_value - 100000.0
total_return = (final_value - 100000.0) / 100000.0

print(f'\nInitial Portfolio Value: $100000.00')
print(f'Final Portfolio Value: ${final_value:.2f}')
print(f'Total Profit/Loss: ${total_pnl:.2f}')
print(f'Total Return: {total_return:.2%}')
print(f'Total Trading Fees: ${strategy.total_fees:.2f}')
print(f'Number of Entries: {strategy.entry_count}')

print("\nStop Loss Levels for Each Entry:")
for date, level in strategy.stop_loss_levels:
    print(f"Entry Date: {date}, Stop Loss Level: ${level:.2f}")

print("\nTake Profit Levels for Each Entry:")
for date, level in strategy.take_profit_levels:
    print(f"Entry Date: {date}, Take Profit Level: ${level:.2f}")

print("\nAll Dragonfly Dojis:")
for date in dragonfly_dojis:
    print(date.strftime('%Y-%m-%d'))

print("\nAll Bullish Hammers:")
for date in bullish_hammers:
    print(date.strftime('%Y-%m-%d'))

print("\nAll Bearish Hanging Men:")
for date in bearish_hanging_men:
    print(date.strftime('%Y-%m-%d'))
