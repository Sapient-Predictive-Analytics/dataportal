# Utility of this project and some notes on stack choices

Recap of the Catalyst mission: Cardano native token data in ADA is unreliable and not usable for either trading or risk management. This severely limits DeFi and token funding. There are some good APIs for DEX users and paying professional users, but freely available data APIs and histroical data is limited to very poor often USD denominated token data. The open source community around trading and investment is familiar with Python (and to a lesser extend R and Matlab) tools and free or low cost data APIs or at least static historical data such as coinmarketcap and nasdaq/quandl. Most people are familiar with Pandas, for example reading CSV files and conveniently slicing, charting and backtesting their trading ideas.

Most books on DIY quantitative trading and automation of trading strategies today use Python and its rich package ecosystem. We have settled on the common pandas read_csv data compatibility instead of json or other formats popular with blockchain api feeds as it will be more familiar for anyone with exposure of backtesting and trading applications ranging from amateur MOOCs to professional fund managers.

The first chapters of IPython notebook examples and trading strategies is unlikely to result profitable results in real life, but meant to show how data data is imported and used. There are many pitfalls in automated or machine trading strategies, and careful choice of timeframes, order book consideration, fees, slippage, and for Cardano native tokens reliability of DEXes to execute swaps or limit orders and availability of desired trading volumes are all critical to success. These asspects will be added with more tokens being listed and the site growing over the course of the project. We hope to receive feedback early on and are keen to steer the direction according to user demand and responsive to ecosystem trends and best practices.

![Imgur](https://i.imgur.com/Jy0djnR.jpeg)

## Getting Zipline
Installing Zipline as our main Backtesting package on Anaconda (root -> Terminal):

`conda create -n zip38 python=3.8`

`activate zip38`

`conda install -c conda-forge zipline-reloaded`


![Zipline](https://i.imgur.com/DDetr8I.png)

***

## Useful resources:
### Data cleaning
* https://docs.cleanlab.ai/stable/index.html
* https://pyjanitor-devs.github.io/pyjanitor/ 
### Refactoring
* https://github.com/CharlieShelbourne/data-manipulation
### Data manipulation
* https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
* https://github.com/yhilpisch/py4fi2nd
### Backtesting
* https://zipline-trader.readthedocs.io/en/latest/
* https://zipline.ml4trading.io/
* https://kernc.github.io/backtesting.py/
* https://pypi.org/project/Backtesting/
### Trading bots etc.
* https://www.geniusyield.co/marketmakerbot?lng=en
* https://www.axo.trade/programmable-swaps
### Market coverage
* https://defillama.com/chain/Cardano
* https://www.taptools.io/openapi/subscription?currency=ADA
* https://api-mainnet-prod.minswap.org
* https://github.com/SundaeSwap-finance/sundae-sdk
* https://docs.muesliswap.com/cardano/muesli-api/api-v1
### Complexity/Prediction
* https://docs.nixtla.io/
* https://python.langchain.com/docs/templates/extraction-openai-functions
