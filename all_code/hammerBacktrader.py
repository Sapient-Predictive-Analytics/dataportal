# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:15:23 2024

@author: tom

Trading Strategy:
1. Entry: Enter a long position when a Bullish Hammer candlestick pattern is detected in a downtrend.
2. Exit: Exit the position after 7 days (including the entry day).
3. Cooldown: Do not enter a new position if another Bullish Hammer occurs within 7 days of the last entry.
4. Position Sizing: Invest all available cash in each trade, accounting for trading fees.
"""

import os
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tabulate import tabulate

print(os.getcwd())

class BullishHammerIndicator(bt.Indicator):
    lines = ('bullish_hammer',)
    params = (('body_ratio', 0.3), ('wick_ratio', 2.0), ('trend_period', 14))

    def __init__(self):
        self.addminperiod(self.p.trend_period)
        self.trend = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.trend_period)

    def next(self):
        candle = self.data
        body = abs(candle.close[0] - candle.open[0])
        wick = candle.high[0] - max(candle.open[0], candle.close[0])
        tail = min(candle.open[0], candle.close[0]) - candle.low[0]
        
        is_hammer = (body <= (candle.high[0] - candle.low[0]) * self.p.body_ratio and
                     tail >= body * self.p.wick_ratio and
                     wick <= body * 0.1)
        
        is_downtrend = candle.close[0] < self.trend[0] and self.trend[0] < self.trend[-1]
        
        self.lines.bullish_hammer[0] = int(is_hammer and is_downtrend and candle.close[0] > candle.open[0])

class BullishHammerStrategy(bt.Strategy):
    params = (
        ('trading_fee', 0.001),  # 0.1% trading fee
        ('exit_days', 7),        # Exit after 7 days (including entry day)
    )

    def __init__(self):
        self.bullish_hammer = BullishHammerIndicator(self.data)
        self.order = None
        self.trade_log = []
        self.portfolio_value = []
        self.total_fees = 0
        self.entry_count = 0
        self.entry_date = None
        self.cooldown = 0

    def next(self):
        # Update portfolio value
        self.portfolio_value.append(self.broker.getvalue())

        # Decrease cooldown counter
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.order:
            return

        # Check for exit
        if self.position and (len(self) - self.entry_date) >= self.params.exit_days - 1:
            self.order = self.close()
            return

        # Check for entry
        if not self.position and self.cooldown == 0 and self.bullish_hammer[0]:
            available_cash = self.broker.getcash()
            max_size = int(available_cash / (self.data.close[0] * (1 + self.params.trading_fee)))
            self.order = self.buy(size=max_size)
            self.entry_count += 1
            self.entry_date = len(self)
            self.cooldown = self.params.exit_days  # Set cooldown to avoid immediate re-entry

    def notify_order(self, order):
        if order.status in [order.Completed]:
            fee = order.executed.value * self.params.trading_fee
            self.total_fees += fee
            if order.isbuy():
                self.log_trade("BUY", order.executed.size, order.executed.price, fee)
            elif order.issell():
                self.log_trade("SELL", order.executed.size, order.executed.price, fee)
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

def plot_results(data, strategy):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)

    # Plot price data
    ax1.plot(data.index, data['close'], label='Close Price')
    
    # Plot buy and sell signals
    for trade in strategy.trade_log:
        if trade['type'] == 'BUY':
            ax1.scatter(trade['date'], trade['price'], color='g', marker='^', s=100)
        else:  # SELL
            ax1.scatter(trade['date'], trade['price'], color='r', marker='v', s=100)

    ax1.set_title('WMT Token Price (ADA) and Trading Signals')
    ax1.set_ylabel('Price (ADA)')
    ax1.grid(True)
    ax1.legend(['Close Price', 'Buy Signal', 'Sell Signal'])

    # Plot portfolio value
    portfolio_values = strategy.portfolio_value
    if len(portfolio_values) < len(data):
        portfolio_values = [portfolio_values[0]] * (len(data) - len(portfolio_values)) + portfolio_values
    ax2.plot(data.index, portfolio_values, label='Portfolio Value', color='purple')
    ax2.set_title('Portfolio Value')
    ax2.set_ylabel('Value (ADA)')
    ax2.grid(True)

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    
    plt.tight_layout()
    plt.show()

# Main script
data = pd.read_csv('WMT.csv', parse_dates=['date'], index_col='date')

cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(BullishHammerStrategy)

initial_cash = 100000.0
cerebro.broker.setcash(initial_cash)

results = cerebro.run()
strategy = results[0]

plot_results(data=data, strategy=strategy)

print("\nTrade Summary Table:")
table_data = [
    [trade['date'], trade['type'], f"${trade['price']:.2f}", trade['size'],
     f"${trade['fee']:.2f}", f"${trade['portfolio_value']:.2f}", trade['position']]
    for trade in strategy.trade_log
]
headers = ["Date", "Type", "Price", "Size", "Fee", "Portfolio Value", "Position"]
print(tabulate(table_data, headers=headers, tablefmt="grid"))

final_value = strategy.portfolio_value[-1] if strategy.portfolio_value else initial_cash
total_pnl = final_value - initial_cash
total_return = (final_value - initial_cash) / initial_cash

print(f'\nInitial Portfolio Value: ${initial_cash:.2f}')
print(f'Final Portfolio Value: ${final_value:.2f}')
print(f'Total Profit/Loss: ${total_pnl:.2f}')
print(f'Total Return: {total_return:.2%}')
print(f'Total Trading Fees: ${strategy.total_fees:.2f}')
print(f'Number of Entries: {strategy.entry_count}')