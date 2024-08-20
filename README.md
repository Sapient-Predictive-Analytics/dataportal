# dataportal
Public repository for Sapient's Cardano Native Tokens data portal.
Fungible Tokens at launch: **AGIX**, **BOOK**, **COPI**, **EMP**, **FLDT**, **GENS**, **HUNT**, **IAG**, **INDY**, **LENFI**, **MELD**, **MIN**, **MILK**, **NEWM**, **NMKR**, **NTX**, **SNEK**, **SUNDAE**, **WMT**, **WRT**

Our website and repository are constantly evolving and will launch in September as part of our [Catalyst Project](https://cardano.ideascale.com/c/idea/114247). New sections and updated data and charts are constantly being added and community feedback incorporated. A full tutorial, how-to-use flow and video will be provided upon launch, in the meantime you can find all section's information in their respective Markdown (.md) files with links to code, charts and data. Please also use the feedback form, Twitter or Github issues/discussion to get in touch, request API key, contribute content or request features or tickers. **Thank you and hope you enjoy the content!**

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

## Flow of the Dataportal and recommended reading

(1) If you are new to Python data analysis, backtesting, trading or native tokens please start with our simple World Mobile Token casestudy.
(2) Next or if you have some background, proceed to the Backtesting section to get started with Backtrader and Python plotting.
(3) Refer to our section on the Heatmap feature next for advanced plotting and optimization of trading strategies.
(4) More feature-rich or complex backtests are dealt with in the continued Backtesting section.
(5) This is continued in the Advanced Heatmap optimization study.
(6) Don't miss the chapter on Risk Management before you consider actually trading native tokens!
(7) Learn about data cleaning and outlier detection here.
(8) Finally, download or ingest native tokens data using our API.
* Get in touch, share ideas, reach out.
* This website and repo are NOT FINANCIAL ADVICE!

***

## Casestudy Milestone 1
Simple data manipulation on clean WMT (Minswap) data

[Download folder for interactive notebook](https://github.com/Sapient-Predictive-Analytics/dataportal/tree/main/casestudy)


***
## How to use this repository and project

[<img src="https://i.imgur.com/NiU8xcT.png" width="200" height="140" />](https://youtu.be/97e-LBkXwn4?si=V-zD0qgLHCa7VRZi)

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
