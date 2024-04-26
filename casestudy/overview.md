# iPython Notebook WMT_Casestudy overview

The easiest way to use this iPython notebook is to download the folder and open it with your own Anaconda jupyter notebook app as done in the video walkthrough. You can see the static content in the WMT_Casestudy.ipynb file directly in Github as well. We may add the binder link back that we have removed for the time being for performance issues. It is of course also posssible to run ipython from the command line if you have all the packages installed and clone the code in your terminal. Either way you choose, this gives an initial overview of how easy it is to play around with native token data similar to any other stock or crypto time series and showcases the advantages of Python for data manipulation and plotting if you are not very familiar with it yet. In the Utility section of this repository there is a markdown file with recommended packages and reading.

### First Code Block
Introduces Pandas read_csv which will be the main utility prior to API integration
Currently plotting a custom 14 day moving average and token prices on Minswap

![Imgur](https://i.imgur.com/36OI07m.jpeg)
Any part of the notebook can be altered by the interactive user (for example if you download the folder into your Documents and open Anaconda).

```
# Allow inline plotting
%matplotlib inline

# Import all needed libraries
import pandas as pd

# Read the data from disk
data = pd.read_csv('wmt.csv', index_col='Date', parse_dates=['Date'])
data = data.rename(columns={'C': 'WMT'})

# Calculate 14-day moving average and plot along with token data
data['SMA 60'] = data['WMT'].rolling(60).mean()
data[['WMT', 'SMA 60']].plot()
```

### Second Code Block
Introduces "backtesting" by plotting Profit and Loss of a simplified moving average crosssover based on real WMT data, but without slippage, order book consideration, fees.

User can play around with the plots or inputs, for example try different moving averages. Numpy library is introduced which allows logic and mathematical functions and adds np.where to introduce very simple conditionality, intead of relying on bespoke backtesting libraries, to get a first feel for which strategies might work without the heavy compute.

```
# Allow inline plotting
%matplotlib inline

# Import all needed libraries
import pandas as pd
import numpy as np

# Read the data from disk
data = pd.read_csv('wmt.csv', index_col='Date', parse_dates=['Date'])
data = data.rename(columns={'C': 'WMT'})

# Calculate two moving averages for crossover
data['SMA7'] = data['WMT'].rolling(7).mean()
data['SMA30'] = data['WMT'].rolling(30).mean()

# Set to 1 if 7-day is above 30-day
data['Position'] = np.where(data['SMA7'] > data['SMA30'], 1, 0)

# Buy on signal delay to next day
data['Position'] = data['Position'].shift()

# Calculate daily % return per day
data['StrategyPct'] = data['WMT'].pct_change(1) * data['Position']

# Calculate cumulative returns
data['Crossover Strategy'] = (data['StrategyPct'] + 1).cumprod()

# Calculate index cumulative returns
data['Token Buy&Hold'] = (data['WMT'].pct_change(1) + 1).cumprod()

# Plot the result
data[['Token Buy&Hold', 'Crossover Strategy']].plot()
```

### Third Code Block
Introduces helper functions and correlation as well as ADA-USD time series.

Some native tokens may move against ADA-USD as holders try to "cash out" if ADA rises, while others are correlated with ADA - if the ecosystem grows, the tokene economy may grow exponentially. This is an important cue for whether there are more buyers or sellers and will be an obvious field of study during later stages of the project when more sophisticated methods are available.

```
# Allow inline plotting
%matplotlib inline

# Import all needed libraries
import pandas as pd

# Helper function to create returns series
def get_returns(file):
    """
    This function reads a data file from disk
    and returns percentage returns.
    
    """
    return pd.read_csv(file + '.csv', index_col=0, parse_dates=True).pct_change()

# Get the WMT token data from file
df = get_returns('wmt_corr')

# Get the ADA-USD data from file
df['ADA'] = get_returns('ada_corr')

# Calculate correlations and plot the last 365 data points
df['WMT'].rolling(60).corr(df['ADA'])[-365:].plot()
```

### Fourth Code Block
Introduces Matplotlib and more advanced charting, while computing possible areas of interest like relative strength, volatility, correlation and comparison of asset class prices in the same standardized chart.
Interactive iPython users can manipulate the plots, scales and parameters or combine the more advanced charting features with "backtesting" from the second code block.

```
# Allow inline plotting
%matplotlib inline

# Import all needed libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Helper functions
def get_data(file):
    """
    Fetch data from disk
    """
    data = pd.read_csv(file + '.csv', index_col='Date', parse_dates=['Date'])
    return data

def calc_corr(ser1, ser2, window):
    """
    Calculates correlation between two series.
    """
    ret1 = ser1.pct_change()
    ret2 = ser2.pct_change()
    corr = ret1.rolling(window).corr(ret2)
    return corr

# Define how many points, i.e. trading days, we want to plot
points_to_plot = 365

# Get the log return data
data = get_data('fiat')

# Rebase the two series to the same point in time, start where the plot will start
for ind in data:
    data[ind + '_rebased'] = (data[-points_to_plot:][ind].pct_change() + 1).cumprod()
    
# Relative strength, WMT to ADA
data['rel_str'] = data['WMT'] / data['ADA']

# Calculate 60 day rolling correlation
data['corr'] = calc_corr(data['ADA'], data['WMT'], 60)

# Calculate the volatility metrics
data['WMT_Volatility'] = data['WMT'].pct_change().rolling(60).std() * np.sqrt(365)
data['ADA_Volatility'] = data['ADA'].pct_change().rolling(60).std() * np.sqrt(365)

# Slice the data, cut points we don't intend to plot
plot_data = data[-points_to_plot:]

# Make new figure and set the size
fig = plt.figure(figsize=(12, 8))

# The first subplot, planning for 5 plots high, 1 plot wide, this being the first
ax = fig.add_subplot(511)
ax.set_title('USD Performance Comparison')
ax.semilogy(plot_data['WMT_rebased'], linestyle='-', color="red", label='WMT', linewidth=3.0)
ax.semilogy(plot_data['ADA_rebased'], linestyle='--', label='ADA', linewidth=3.0)
ax.legend()
ax.grid(False)

# Second sub plot
ax = fig.add_subplot(512)
ax.plot(plot_data['rel_str'], label='Relative Strength, WMT to ADA', linestyle=':', linewidth=3.0)
ax.legend()
ax.grid(True)

# Third sub plot
ax = fig.add_subplot(513)
ax.plot(plot_data['corr'], label='Correlation WMT to ADA', linestyle='-.', linewidth=3.0)
ax.legend()
ax.grid(True)

# Fourth sub plot
ax = fig.add_subplot(514)
ax.plot(plot_data['ADA_Volatility'], label='Annualized Volatility ADA', linestyle='--', linewidth=3.0)
ax.legend()
ax.grid(True)

# Fifth sub plot
ax = fig.add_subplot(515)
ax.plot(plot_data['WMT_Volatility'], label='Annualized Volatility WMT', linestyle='--', linewidth=3.0)
ax.legend()
ax.grid(True)
```
