# Native Token Dataportal
Public repository for Sapient's Cardano Native Tokens data portal.
Fungible Tokens at launch: **AGIX**, **BOOK** (now: STUFF), **COPI**, **EMP**, **FLDT**, **GENS**, **HUNT**, **IAG**, **INDY**, **LENFI**, **MELD**, **MILK**, **MIN**, **NEWM**, **NMKR**, **NTX**, **SNEK**, **SUNDAE**, **WMT**, **WRT**

The Native Token Dataportal is now live with step-by-step introduction to open source Python backtesting and plotting, strategy execution, risk management, clean token data and API. Please watch the video below how to get the most out of the service. There is also a landing website and feedback channels via X, Telegram and Google forms. We have opened Github Discussions and will deal with submitted issues and PRs prompty. Looking forward to your feedback and contribution!


![WMT Backtest](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/WMT_SMA20_October1.png)


*Simple SMA20 backtest for WMT token since first DEX listing used to showcase use of open source Python libraries and data API to build from simple trading strategies to more complex ones.*

***
## Flow of the Dataportal and recommended reading

*Optional: set up virtual environment to manage dependencies and keep separate from your own projects*
~~~
python3 -m venv backtesting
source backtesting/bin/activate
~~~

To use all the files of this repo in once place (recommended):
~~~
git clone https://github.com/Sapient-Predictive-Analytics/dataportal.git
pip install requirements.txt
~~~


**(1)** If you are new to Python data analysis, backtesting, trading or native tokens please start with our simple **World Mobile Token [Casestudy](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/casestudy/overview.md).**

**(2)** Next or if you have some background, proceed to the **[Backtesting](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/backtesting.md)** section to get started with Backtrader and Python plotting.

**(3)** Refer to our section on the **[Heatmap](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md)** feature next for advanced plotting and optimization of trading strategies.

**(4)** More feature-rich or complex backtests are dealt with in the **[Advanced Backtesting](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/backtesting2.md)** section.

**(5)** This is continued in the **[Advanced Heatmap](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md#advanced-optimization)** optimization study.

**(6)** Don't miss the chapter on **[Risk Management](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md)** before you consider actually trading native tokens!

**(7)** Learn about **data cleaning and outlier detection** [here](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/cleanData.md).

**(8)** To trade, discuss with likeminded people or test DEXes on Testnet, visit the **[Community](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/community/community.md)** section about trading venues, their communities and Dataportal collaboration

**(9)** Finally, download or ingest native tokens data using our **[API](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/api/documentationAPI.md)**

* **Get in [touch](https://x.com/SapientSwarm)**, share [ideas](https://github.com/Sapient-Predictive-Analytics/dataportal/discussions), submit [feedback](https://forms.gle/H1fMqNMmyYhaVepV6), submit an [issue](https://github.com/Sapient-Predictive-Analytics/dataportal/issues), [reach out](https://www.sapientswarm.com/cardano.html).
  
* This website and repo are **[NOT FINANCIAL ADVICE]**(https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/disclaimer.md)!

***

**Any feedback, request for new features, tickers, custom signals or plots can be submitted via our Google Form**

![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)
[Fill out the form](https://forms.gle/H1fMqNMmyYhaVepV6)

![x](http://i.imgur.com/tXSoThF.png)
[Or provide Feedback / Request feature on X](https://twitter.com/SapientSwarm)

***

Please contact us or contribute to this repository if you have ideas, requests or directions how to grow quantitative trading and better market making and risk management for Cardano's native tokens investable assets universe.

***
[Notes on data formats, packages and utility](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/utility.md)

[How the first 10 Native Tokens to be featured were chosen](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/rationale.md)

***



## Casestudy to get started with Python Backtesting

[How To](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/casestudy/overview.md)

Simple data manipulation on clean WMT (Minswap) data

[Download folder for interactive notebook](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/casestudy)

Download folder for interactive IPython notebook and time series data.

***
## How to use this repository and project

[<img src="https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Complex4Dheatmap.png" width="200" height="140" />](https://youtu.be/AIDbk8Iq5TM)

***
## Backtesting and Heatmap Tool
Introduction to backtesting concepts, the Zipline package, trading strategy design with heatmaps and use of Seaborn and other plotting libraries.
New token prices have been added and charts, backtests and heatmap related files (images, code and notebooks) are added regularly.

***

## Log-plotting and financial candlesticks charts

![LogMILK](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/MILK_candles_log.png)

*Here, we scale the axis logarithmically optimized for the entire price range to show meaningful price action across a highly volatile token like MILK (MuesliSwap's native token)*

~~~
def custom_log_scale(min_val, max_val):
    lower = max(0.05, np.floor(min_val * 2) / 2)
    upper = np.ceil(max_val * 2) / 2
    
    base = 2
    start = np.log(lower) / np.log(base)
    stop = np.log(upper) / np.log(base)
    ticks = np.logspace(start, stop, num=8, base=base)
    
    ticks[0] = lower
    return lower, upper, ticks
~~~

***
*Below is a [Heatmap](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md) for parameter-optimization and risk-tuning for a trading strategies with 2 degrees of freedom*
![heatmap2d](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Heatmap2D.png)

***

![Surfaces](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/Complex4Dheatmap.png)

Even complex strategies with many features can be optimized using the Heatmap feature with enough compute and the right plotting library.
