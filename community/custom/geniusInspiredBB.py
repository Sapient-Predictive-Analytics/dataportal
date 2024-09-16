import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt

class BollingerBandStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2),
        ('stop_loss', 0.15),  # 15% stop loss
    )

    def __init__(self):
        self.bband = bt.indicators.BollingerBands(self.data.close, period=self.p.period, devfactor=self.p.devfactor)
        self.order = None
        self.entry_price = None
        self.account_values = []

    def next(self):
        # Record the account value for this bar
        self.account_values.append(self.broker.getvalue())

        if self.order:
            return

        if not self.position:
            if self.data.close[0] < self.bband.lines.bot[0]:
                available_cash = self.broker.getcash()
                size = int(available_cash / self.data.close[0])
                self.order = self.buy(size=size)
                self.entry_price = self.data.close[0]
        else:
            if self.data.close[0] > self.bband.lines.top[0] or \
               self.data.close[0] < self.entry_price * (1 - self.p.stop_loss):
                self.order = self.close()

    def stop(self):
        self.final_value = self.broker.getvalue()

def run_backtest(data):
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))
    cerebro.addstrategy(BollingerBandStrategy)

    initial_cash = 100000.0
    cerebro.broker.setcash(initial_cash)

    print(f'Starting Portfolio Value: ${initial_cash:.2f}')
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    print(f'Final Portfolio Value: ${final_value:.2f}')

    return results[0].account_values

# Load data
data = pd.read_csv('AGIX.csv', parse_dates=['date'], index_col='date')
data = data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})

# Run backtest
account_balance = run_backtest(data)

# Plot account balance
plt.figure(figsize=(12, 6))
plt.plot(data.index[:len(account_balance)], account_balance)
plt.title('Account Balance Over Time')
plt.xlabel('Date')
plt.ylabel('Balance (ADA)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate and print total return
total_return = (account_balance[-1] - account_balance[0]) / account_balance[0]
print(f'Total Return: {total_return:.2%}')