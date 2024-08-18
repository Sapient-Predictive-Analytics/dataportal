# dataportal
Public repository for Sapient's Cardano Native Tokens data portal.
Fungible Tokens at launch: **AGIX**, **BOOK**, **COPI**, **FLDT**, **GENS**, **HUNT**, **IAG**, **INDY**, **LENFI**, **MELD**, **MIN**, **MILK**, **NEWM**, **NTX**, **SNEK**, **SUNDAE**, **WMT**, **WRT**

![WMT Backtest](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/backtesting/WMT_SMA20_full_signals.png)


*Simple SMA20 backtest for WMT token since first DEX listing used to showcase use of open source Python libraries and data API to build from simple trading strategies to more complex ones.*


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
## Casestudy Milestone 1
Simple data manipulation on clean WMT (Minswap) data

[Download folder for interactive notebook](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/casestudy)


***
## How to use this repository and project

[<img src="https://i.imgur.com/NiU8xcT.png" width="200" height="140" />](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE)

***
## Backtesting and Heatmap Tool Milestone 2
Introduction to backtesting concepts, the Zipline package, trading strategy design with heatmaps and use of Seaborn and other plotting libraries.
New token prices have been added and charts, backtests and heatmap related files (images, code and notebooks) are added regularly.

*IAGON is now on the Dataportal*

![IAG Candles](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/IAG_candles_log.png)

*SNEK is now on the Dataportal*

![SNEK Candles](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/SNEK_candles.png)

![SNEK](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/snek.png)

*MIN is now on the Dataportal*

![MIN Candles](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/MIN_candles_log.png)

![MINv2](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/minv2.png)

***
## Video walkthrough of trading strategy design for native tokens

[<img src="https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/NEW_ICON_SW.png" width="200" height="140" />](https://youtu.be/f6Z5DMaJmcw)

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
