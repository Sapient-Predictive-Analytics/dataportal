# Risk Management of Native Tokens

The chapter on our [HeatmapTool](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md) for strategy factor optimization touched on assessing risks and improving expected return on a single strategy. This section will greatly expand the coverage of optimization and risk management, covering individual token holdings and portfolios of tokens. **Diversification** is often [referred](https://www.advisorperspectives.com/commentaries/2024/03/14/only-free-lunch-in-investing) to as *"the only free lunch in investing"*.  Instead of betting the ranch on a single project with huge upside and probably quite high risk, a portfolio on themes like "Cardano DeFi" is likely to perform much better *per unit of risk* if expected returns are not perfectly correlated. In the DeFi space, there are a lot of factors apart from the general environment in crypto and the success of Cardano relative to other chains. Does the team have the skills needed? Are the founders true visionaries that can generate the necesssary visibility and innovation? While all tokens will swing wildly, only a few will be breakout successes. A basket that holds many promising projects will as a whole move a lot less, while *on average* returning the same yield for the holder. Unless we have truly superior information, what is not to like?

Apart from diverisification and portfolio construction, we also look at on-chain and off-chain analytics, descriptive statistics and a popular measure called **Value-at-Risk** to analyze our investment holding and invest "the right amount" - as opposed to amounts that are not meaningful to our wealth or potentially ruinous. Finally, we will explain and also cover improvements on the popular **Sharpe ratio** - i.e. how good is our trading strategy in delivering return for the risk taken.

## Risk factors
Recently, risk factors have become the preferred way to look at investment portfolios instead of more traditional measures like alpha and beta derived from [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp) and the Capital Asset Pricing Model [CAPM](https://www.investopedia.com/terms/c/capm.asp). This alternative framework for estimating input is to boil each asset down to the underlying determinants, or **factors**, that drive the risk and returns of the asset. Such factors are traditionally large cap / small cap, growth / value and so on but for the native token universe could be completely different. We discussed ADA positive / ADA negative in the [Casestudy](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/casestudy/overview.md). While some native tokens amplify the ADA move, i.e. rise in a bull market, others are more likely to hold a stable USD value and fall if ADA goes up because the token holders look for a certain fiat return. Other factors could be the geography (Americas, Asia, Africa etc), theme (impact, metaverse, DeFi) or correlation to gold, network congestion or other factors that could even be "memes".  If we understand how the factors influence returns, and we understand the factors, we will be able to construct more robust portfolios. Generally, factor analysis should yield better results than traditional finance measures like beta which have never been conclusively proven even for the equity universe they were intended for. This is of course subject of heated debate, but we agree with the general [thinking](https://johnrothe.com/the-problem-with-modern-portfolio-theory/) behind the doubts.

## Portfolio construction and analysis
The goal of portfolio management is to select and allocate positions in assets that achieve a desired risk-return trade-off regarding a benchmark. For a given measurement period such as the calendar or financial year, the portfolio manager selects positions that optimize diversification to reduce risks while achieving a target return. Periodically, positions will require rebalancing to account for changes in weights as some assets outperform others in order to maintain the target risk profile. A good illustration is the recent boom in ["Magnificent 7"](https://www.morganstanley.com/ideas/magnificent-7-stocks-portfolio-risk) (Big Tech) stocks on US exchanges. From a few percentage points of portfolios, these stocks now account for over a quarter of exchange traded funds or baskets tracking the broad market. This approach is called market-cap weighted as opposed to equal-weight where we maintain constant portfolio allocation to allow laggards to catch up. This goes against the conventional wisdom of letting your "winners run" while "cutting the losers", so there is a trade-off between concentration and natual selection, that represents similar opposing philosophies in short term trading between ["momentum"](https://www.investopedia.com/terms/m/momentum.asp) and ["mean-reversion"](https://www.investopedia.com/terms/m/meanreversion.asp). A very complex portfolio management approach could try to have the best of both worlds while incorporating regime switching, for example go from momentum weights to equal weights when certain indicators for froth or bubble risk flash red. However, the more we tweak our approach to fit past data, the more we are setting ourselves up for biases and hindsight trading. Here is another saying: "Skate to where the puck is going to be, not where it has been." This has often been credited to ice hockey legend Wayne Gretzky, but the [internet](https://danoshinsky.com/2015/06/26/theres-one-little-problem-with-that-famous-wayne-gretzky-quote-about-pucks/) is not so sure he really said it.

To give examples and make this easier to understand with practical examples, we work with a "Cardano DEX" portfolio considering all DEXes for which we provide data through this Dataportal.

~~~
import pandas as pd
import numpy as np

tokens = ['MIN', 'MILK', 'GENS', 'SUNDAE', 'WRT']
token_supplies = [3000000000, 10000000, 100000000, 2000000000, 100000000]
    
dataframes = load_data(tokens)

def load_data(tokens):
    dataframes = {}
    for token in tokens:
        df = pd.read_csv(f"{token}.csv", parse_dates=['date'])
        df.set_index('date', inplace=True)
        dataframes[token] = df
    return dataframes
~~~

### Equal-weighted basket
Equal-weighted indices simply invest the same amount into each of its holdings. For a portfolio of ['MIN', 'MILK', 'GENS', 'SUNDAE', 'WRT'] this would allocate 20% of the total ADA investment into each token, regardless of their price or market cap.

~~~
def calculate_equal_weight_basket(dataframes, tokens):
    combined_df = pd.concat([df['close'] for df in dataframes.values()], axis=1, keys=tokens)
    equal_weight_basket = combined_df.mean(axis=1)
    return equal_weight_basket
~~~

### TVL-weighted basket
A more common practice and used by most indices in the world like the S&P500 is to adjust the index or basket weight according to the market cap or float of the tokens, so if there are "ecosystem winners" we increase our share in them over time instead of cutting exposure to the dominant and usually most profitable protocols in favor of the low cap ones. Other metrics instead of market cap are possible, for example in the world of global commodities, the S&P GSCI measures commodity market performance through futures and is a production-weighted index taking into account not the investment amount but the value of production outputs.

We need to rebalance a TVL-weighted basket in the case of additional supply or token burn events and here do this at the first of each month.

~~~
def calculate_market_cap_weight_basket(dataframes, tokens, token_supplies):
    combined_df = pd.concat([df['close'] for df in dataframes.values()], axis=1, keys=tokens)
    
    market_cap_basket = pd.Series(index=combined_df.index, dtype=float)
    
    for month_start in combined_df.resample('MS').index:
        month_end = month_start + pd.offsets.MonthEnd(0)
        month_data = combined_df.loc[month_start:month_end]
        
        if month_start == month_data.index[0]:
            market_caps = month_data.iloc[0] * token_supplies
            weights = market_caps / market_caps.sum()
        
        month_basket = (month_data * weights).sum(axis=1)
        market_cap_basket.loc[month_start:month_end] = month_basket
    
    return market_cap_basket
~~~

Over 2023, the "DEX basket" using market cap weight did indeed outperform the equally weighted one, as MIN and MILK tokens rallied but other protocols did not. During bear market phases, equal weight may insulate the holder from some losses though - especially if they are corrections after rallies.

![DEXes](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/DEX%20baskets.png)


### Descriptive statistics
Some descriptive statistics like volatility, correlation and Sharpe ratio can easily be calculated on the fly, but most types of existential risks especially for native tokens require deeper thought about the utility, supply/demand and integrity of the protocol, loyality of the user base, ability to innovate and so on.

Here, we look at returns, correlation, volatility and Sharpe ratio of our baskets of DEX tokens.

~~~
def calculate_descriptive_stats(results, start_date='2023-01-01', end_date='2023-12-31', risk_free_rate=0.05):
    # Filter data for the specified period
    period_results = results.loc[start_date:end_date]
    
    # Calculate daily returns
    daily_returns = period_results.pct_change().dropna()
    
    # Initialize stats DataFrame
    stats = pd.DataFrame(index=['Equal Weight Basket', 'Market Cap Weight Basket'])
    
    for column in daily_returns.columns:
        returns = daily_returns[column]
        
        stats.loc[column, 'Standard Deviation'] = returns.std()
        stats.loc[column, 'Annualized Volatility'] = returns.std() * np.sqrt(252)  # Assuming 252 trading days
        stats.loc[column, 'Annualized Return'] = (1 + returns.mean()) ** 252 - 1
        stats.loc[column, 'Sharpe Ratio'] = (stats.loc[column, 'Annualized Return'] - risk_free_rate) / stats.loc[column, 'Annualized Volatility']
    
    # Calculate correlation between baskets
    correlation = daily_returns['Equal Weight Basket'].corr(daily_returns['Market Cap Weight Basket'])
    
    # Create a separate DataFrame for correlation
    corr_df = pd.DataFrame({'Correlation': [correlation]}, index=['Between Baskets'])
    
    return stats, corr_df
~~~

Using our own data and previous DEX example, this gives us some useful numbers to further assess the choice between equal weight and TVL weight.
Descriptive Statistics for 2023:
                          Standard Deviation  Annualized Volatility  Annualized Return  Sharpe Ratio
Equal Weight Basket                   0.0545                 0.8647             1.1013        1.2159
Market Cap Weight Basket              0.0809                 1.2843             2.9393        2.2497

Correlation between baskets:
                 Correlation
Between Baskets       0.5859

### Value at risk
Value-at-risk [(VaR)](https://www.investopedia.com/terms/v/var.asp) is one of the most widely used risk measures, and a much debated one. Loved by practitioners for its intuitive appeal, it is widely discussed and criticized by many — mainly on theoretical grounds, with regard to its limited ability to capture what is called tail risk (more on this shortly). In words, VaR is a number denoted in fiat or ADA units indicating a loss (of a portfolio, a single position, etc.) that is not exceeded with some confidence level (probability) over a given period of time. Consider a stock position, worth 1 million ADA today, that has a VaR of 100,000 ADA at a confidence level of 99% over a time period of 30 days (one month). This VaR figure says that with a probability of 99% (i.e., in 99 out of 100 cases), the loss to be expected over a period of 30 days will not exceed 100,000 ADA. However, it does not say anything about the size of the loss once a loss beyond 50,000 USD occurs — i.e., if the maximum loss is 200,000 or 500,000 ADA what the probability of such a specific “higher than VaR loss” is. All it says is that there is a 1% probability that a loss of a minimum of 100,000 ADA or higher will occur. Value-at-Risk is by definition "skating where the puck was" as increased volatility will make the future look more risky and vice versa. If we had rebalanced our DEX portfolio at the end of 2022 to accound for the steep losses in our dataset, we would have entered the year 2023 with reduced risk limits and not been able to capture the rally (see section on TVL-weighted baskets). Many risk practitioners therefore now prefer some form of **stress test** for example exposing your portfolio to simulated price moves based on long-term statistical properties of its holdings and their [covariance](https://www.investopedia.com/terms/c/covariance.asp). 

### Sharpe-, Sortino- and Calmar-Ratio

In the dynamic world of native tokens, which often experience huge volatility and liquidity might be moving between DEXes, risk management of strategy designs is crucial in this compelling yet volatile asset class. As the market matures, so too must our approaches to risk management and performance evaluation. While traditional finance has long relied on metrics like the Sharpe ratio to gauge risk-adjusted returns, the unique characteristics of the native token space demand a more nuanced perspective.

The Sharpe ratio, developed by Nobel laureate William Sharpe, has been the gold standard for strategy assessment and portfolio analysis since it was first published in 1966. It measures the "excess return" of an investment relative to the volatility of the period, providing a standardized way to compare different assets or strategies. It answers the question of how much additional return are we getting for each unit of risk we're taking on.

However, the crypto market's tendency towards extreme price swings and non-normal return distributions has led many analysts to question whether the Sharpe ratio alone is sufficient for evaluating native token investments. Enter alternative metrics like the Sortino and Calmar ratios, which may offer more appropriate benchmarks for judging performance in this unique asset class.

![Sen](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/SaydipSen.png)

Maximimizing Sharpe-, Sortino- or Calmar-Ratio can result in vastly different portfolios of assets or strategies. This research by [Saydip Sen](https://www.researchgate.net/figure/Portfolio-compositions-for-the-auto-sector-a-The-portfolio-with-the-maximum-Sharpe_fig2_364534078) gives a great visual demonstration.


As we delve deeper into these metrics and their applications, we'll explore how a more comprehensive toolkit for risk management can help investors navigate the exciting yet treacherous waters of native token investments. Whether you're a seasoned trader or a curious newcomer, understanding these concepts is crucial for developing robust trading strategies and making informed investment decisions in the blockchain era.

Knowing the Sharpe Ratio, Sortino Ratio, and Calmar Ratio is important for any investor, regardless of how large or small their portfolio is. The goal of this post is to deep dive into the Sharpe Ratio, Sortino Ratio, and Calmar Ratio to show how each measure the performance of an investment and/or investment manager. Regardless of whether you’re a hands-off or hands-on investor, knowing these performance metrics can save you a fortune over the course of your lifetime. Let’s jump right into it by looking at the Sharpe Ratio first!

The Sharpe Ratio measures an investment’s risk adjusted performance relative to its volatility. Nobel Prize winning economist William Sharpe created the ratio in 1966. The comparison of performance to volatility is the main reason that the Sharpe Ratio is the industry standard for performance evaluation. Sharpe Ratio is mostly used by investors, portfolio managers, and traders who focus on the stock market and bond market. Here is the Sharpe Ratio calculation for a more thorough understanding:

Sharpe Ratio = (Portfolio return — Risk free rate) / Portfolio volatility

The portfolio return is the percentage gain or loss in the portfolio. The risk free rate is the rate of return for investing in a 10 year US government bond. Portfolio volatility is measured by standard deviation, a statistical method for measuring data dispersion around the mean of a dataset. Portfolio standard deviation measures the variability of the portfolio. It also accounts for the variability of all assets and asset weightings, where weighting is the percentage of one asset’s value relative to the total portfolio value. Please note that each example from the reading uses annual numbers.

Think of calculation and interpretation as two separate tasks, because focusing too heavily on calculation causes us to lose sight of the forest from the trees. The ideal portfolio Sharpe Ratio has a higher risk adjusted return than its volatility. That’s why a Sharpe of 1 is considered acceptable, while a Sharpe of 1.5 or higher is preferrable. A Sharpe Ratio below 1 means the portfolio’s risk adjusted return is less than its volatility, and the investor is risking more than they are earning. No investor prefers this scenario if there is a better alternative.

Consider a theoretical portfolio that only has positively returning months with no consistency of the amount returned. Perhaps one month earned 50%, another month 5%, one month 75%, another month 15%, etc. Regardless of the volatile nature of returns, the portfolio makes money every month. Compared with a lower volatility portfolio that has down months, more consistent return amounts, and returns less overall, Sharpe Ratio may cause us to choose the portfolio that earns less with down months. Certainly, anyone would prefer the fictional portfolio of only money making months. Put in technical terms, the Sharpe ratio does not distinguish between upside and downside volatility. The risk measure inherent in the Sharpe ratio, i.e. the standard deviation of asset returns, does not reflect the way most HODLers or traders perceive risk. Mostly, we care about loss, not volatility.

This is why pairing Sharpe Ratio and Sortino Ratio is important. The Sortino Ratio measures downside portfolio volatility using downside deviation. Downside deviation is the volatility of negatively returning months without accounting for positively returning months. It’s ironic that downside deviation is a positive number despite its focus on downside. It’s calculated the same way as standard deviation using only negative data points. Speaking of similar calculations, the Sortino Ratio formula is the same as the Sharpe ratio formula except downside portfolio volatility replaces total portfolio volatility. Here is the formula for the Sortino Ratio:

Sortino Ratio = (Portfolio return — Risk Free Rate) / Downside portfolio volatility

In some cases, the Sortino Ratio is a better performance metric than the Sharpe Ratio. This is due to the reasons discussed earlier in the fictional portfolio of only money making months. Even if the only positive returns are all over the place causing a higher volatility, this isn’t bad because the portfolio is never down. Sortino Ratio is interpreted similarly to Sharpe Ratio, and here is how to interpret it:

Moving away from unrealistic examples like the dream portfolio of only money making months, let’s look at a more realistic example of Sortino Ratio compared with Sharpe Ratio:

Portfolio 1 had a return of 30.39% and volatility of 20.84%. Its downside deviation is 11.88%. Here is the Sharpe Ratio and Sortino Ratio calculations for portfolio 1:

Portfolio 1 Sharpe Ratio = (30.39% return — 5% risk free rate) / 20.84% portfolio volatility = 1.22 Sharpe Ratio

Portfolio 1 Sortino Ratio = (30.39% return — 5% risk free rate) / 11.88% downside volatility = 2.14 Sortino Ratio

Portfolio 2 had a return of 39.13% and volatility of 37.54%. Given the downside deviation is 9.32%, let’s calculate the Sharpe and Sortino Ratios for portfolio 2:

Portfolio 2 Sharpe Ratio = (39.13% return — 5% risk free rate) / 37.54% portfolio volatility = 0.91 Sharpe Ratio

Portfolio 2 Sortino Ratio = (39.13% return — 5% risk free rate) / 9.32% downside volatility = 3.66 Sortino Ratio

The monthly returns for portfolio 1 and portfolio 2 show a comparable number of down months. They also show a similar volatility profile. Digging a bit deeper, portfolio 1’s down months included returns of -1%, -1%, -5%, -10%, and -2%. Portfolio 2’s down months included returns of -1%, -1%, -7.5%, -5%, and -1%. Although not identical, these returns are quite similar.

Based on Sharpe Ratio alone, portfolio 1 is better than portfolio 2 because it is returning more per unit of risk. However, Sortino Ratio analysis leads us to a different conclusion. The only reasons for the higher volatility in portfolio 2 are February and July, which were big up months that returned 15% and 35% respectively. Furthermore, portfolio 2’s downside volatility is more controlled than portfolio 1. Considering that portfolio 2 has a higher Sortino Ratio than portfolio 1, portfolio 2 is the better option using Sortino Ratio.

These results conflict with one another and this happens from time to time. Similar to most things in life, there is no one size fits all rulebook for investing, portfolio management, and trading. There probably are those rulebooks, but the people who made them are selling the dream of a shortcut to success so that they can make a buck. Sharpe Ratio analysis should be paired with Sortino Ratio analysis to gain a more thorough understanding of the overall performance in question. Discretion is always a factor, and everyone’s risk tolerance is different based on their personal lives, experiences, and goals.

One thing all investors can agree on is their dislike of large losses. The Calmar Ratio is a stricter measure of downside than the Sortino Ratio. Calmar Ratio measures the portfolio’s risk adjusted return compared to its worst performing month or time frame. The only difference in calculation for the Calmar Ratio is the denominator. Here is the Calmar Ratio formula:

Calmar Ratio = (Portfolio Return — Risk free rate) / (Maximum portfolio drawdown)

In similar irony to downside deviation, maximum portfolio drawdown is stated as a positive number. Interpreting the Calmar Ratio is similar to interpreting the Sharpe Ratio and Sortino Ratio. Here is how to interpret it:

Now that we know how to interpret Calmar Ratio, let’s calculate it for the portfolios used in the Sortino Ratio calculations. Here’s the same table of monthly returns from before:

Portfolio 1’s maximum drawdown is -10% and happened in September. Portfolio 2’s maximum drawdown is -12.13% and happened over the two month spand of September and October. Considering a portfolio 1 return of 30.39%, portfolio 2 return of 39.13%, and risk free rate of 5%, here are the Calmar Ratio calculations for each portfolio:

Portfolio 1 Calmar Ratio = (30.39% return — 5% risk free rate) / (Max drawdown -10%) = 2.54 Calmar Ratio

Portfolio 2 Calmar Ratio = (39.13% return — 5% risk free rate) / (Max drawdown -12.13%) = 2.81 Calmar Ratio

This comparison shows that portfolio 2 outperformed portfolio 1 based on its Calmar Ratio. Portfolio 1 positively returned 2.54 times its maximum downside, while Portfolio 2 positively returned 2.81 times its maximum downside. Something to keep in mind is that Portfolio 2 had a larger drawdown despite outperformance in Calmar Ratio. While some prefer the Sortino Ratio and Calmar Ratio because they measure investment performance relative to downside, the Sharpe Ratio is still the standard performance metric used. When using downside ratios, always consider the downside on a standalone basis as well. A portfolio that has a 100% return and 50% maximum drawdown has a high Calmar Ratio, but a 50% drawdown is unacceptable for any period.

## Optimization and automation

### Trading strategies vs buy-and-hold

### Biases and overfitting

### Oracle-risk

## Other factors

### Basis risk

### Model risk, jumps and "rug-pulls"
