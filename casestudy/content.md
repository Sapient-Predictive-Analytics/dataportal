# iPython Notebook WMT_Casestudy overview

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
