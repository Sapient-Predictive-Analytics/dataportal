# Risk Management of Native Tokens

The chapter on our [HeatmapTool](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/HeatmapTool/heatmap.md) for strategy factor optimization touched on assessing risks and improving expected return on a single strategy. This section will greatly expand the coverage of optimization and risk management, covering individual token holdings and portfolios of tokens. **Diversification** is often [referred](https://www.advisorperspectives.com/commentaries/2024/03/14/only-free-lunch-in-investing) to as *"the only free lunch in investing"*.  Instead of betting the ranch on a single project with huge upside and probably quite high risk, a portfolio on themes like "Cardano DeFi" is likely to perform much better *per unit of risk* if expected returns are not perfectly correlated. In the DeFi space, there are a lot of factors apart from the general environment in crypto and the success of Cardano relative to other chains. Does the team have the skills needed? Are the founders true visionaries that can generate the necesssary visibility and innovation? While all tokens will swing wildly, only a few will be breakout successes. A basket that holds many promising projects will as a whole move a lot less, while *on average* returning the same yield for the holder. Unless we have truly superior information, what is not to like?

Apart from diverisification and portfolio construction, we also look at on-chain and off-chain analytics, descriptive statistics and a popular measure called **Value-at-Risk** to analyze our investment holding and invest "the right amount" - as opposed to amounts that are not meaningful to our wealth or potentially ruinous. We cover meaning of and improvements to the popular **Sharpe ratio** - i.e. how good is our trading strategy in delivering return for the risk taken. Finally, we finish with discussing **rug-pulls** and **other factors** unique to crypto, native tokens or decentralized finance.

***

## Quick reference - Contents of this section

**([1](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#factor-investing)) Factor investing**

**([2](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#portfolio-construction-and-analysis)) Portfolio construction and analysis**

**([3](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#descriptive-statistics)) Descriptive statistics**

**([4](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#value-at-risk)) Value at risk**

**([5](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#sharpe--sortino--and-calmar-ratio)) Sharpe-, Sortino- and Calmar-Ratio**

**([6](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#optimization-and-automation)) Optimization and automation**

**([7](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#rug-pulls)) "Rug-pulls"**

**([8](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/risk.md#other-factors)) Other factors**

***

## Factor investing
Recently, factor investing has become the preferred way to look at investment portfolios instead of more traditional measures like alpha, beta, expected risk and expected return derived from [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp) and the Capital Asset Pricing Model [CAPM](https://www.investopedia.com/terms/c/capm.asp). This alternative framework for estimating input is to boil each asset down to the underlying determinants, or **factors**, that drive the risk and returns of the asset. Such factors are traditionally large cap / small cap, growth / value and so on but for the native token universe could be quite different and expand to other *factors*. We discussed ADA positive / ADA negative in the [Casestudy](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/casestudy/overview.md). While some native tokens amplify the ADA move, i.e. rise in a bull market, others are more likely to hold a stable USD value and fall if ADA goes up because the token holders look for a certain fiat return. Other factors could be the geography (Americas, Asia, Africa etc), theme (impact, metaverse, DeFi) or correlation to gold, network congestion or other factors that could even be "memes".  If we understand how the factors influence returns, and we understand the factors, we will be able to construct more robust portfolios. Generally, factor analysis should yield better results than traditional finance measures like beta which have never been conclusively proven even for the equity universe they were intended for. This is of course subject of heated debate, but we agree with the general [thinking](https://johnrothe.com/the-problem-with-modern-portfolio-theory/) behind the doubts.

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


## Descriptive statistics
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

| *Basket* | *Standard Deviation* | *Annualized Volatility* | *Annualized Return* | *Sharpe Ratio* |
| --- | --- | --- | --- | --- |
| Equal Weight Basket | 0.0545 | 0.8647 | 1.1013 | 1.2159 |
| Market Cap Weight Basket | 0.0809 | 1.2843 | 2.9393 | 2.2497 |


Correlation between baskets:
| Metric | Correlation |
| --- | --- |
| Between Baskets | 0.5859 |

## Value at risk
Value-at-risk [(VaR)](https://www.investopedia.com/terms/v/var.asp) is one of the most widely used risk measures, and a much debated one. Loved by practitioners for its intuitive appeal, it is widely discussed and criticized by many — mainly on theoretical grounds, with regard to its limited ability to capture what is called tail risk (more on this shortly). In words, VaR is a number denoted in fiat or ADA units indicating a loss (of a portfolio, a single position, etc.) that is not exceeded with some confidence level (probability) over a given period of time. Consider a stock position, worth 1 million ADA today, that has a VaR of 100,000 ADA at a confidence level of 99% over a time period of 30 days (one month). This VaR figure says that with a probability of 99% (i.e., in 99 out of 100 cases), the loss to be expected over a period of 30 days will not exceed 100,000 ADA. However, it does not say anything about the size of the loss once a loss beyond 50,000 USD occurs — i.e., if the maximum loss is 200,000 or 500,000 ADA what the probability of such a specific “higher than VaR loss” is. All it says is that there is a 1% probability that a loss of a minimum of 100,000 ADA or higher will occur. Value-at-Risk is by definition "skating where the puck was" as increased volatility will make the future look more risky and vice versa. If we had rebalanced our DEX portfolio at the end of 2022 to accound for the steep losses in our dataset, we would have entered the year 2023 with reduced risk limits and not been able to capture the rally (see section on TVL-weighted baskets). Many risk practitioners therefore now prefer some form of **stress test** for example exposing your portfolio to simulated price moves based on long-term statistical properties of its holdings and their [covariance](https://www.investopedia.com/terms/c/covariance.asp). 

Having said this, Value-at-Risk is still an important part of many professional trading outfits, as it provides risk managers and investors a good gauge how much potential loss a speculative or long-term holding might occur under adverse conditions at the 95% or 99% confidence interval. As you can see from below chart, you may be surprised how many ADA are "at risk" if we had invested 100,000 ADA into either equal-weight or market cap-weight DEX baskets. This does not take into account any ADA/USD movement and is purely from the perspective of an ADA-centric perspective.

![VaR](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/risk/ValueAtRisk.png)


## Sharpe-, Sortino- and Calmar-Ratio

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

In some cases, the Sortino Ratio is a better performance metric than the Sharpe Ratio. This is due to the reasons discussed earlier in the fictional portfolio of only money making months. Even if the only positive returns are all over the place causing a higher volatility, this isn’t bad because the portfolio is never down.

One thing all investors can probably agree on is their dislike of large losses. The Calmar Ratio is a stricter measure of downside than the Sortino Ratio. Calmar Ratio measures the portfolio’s risk adjusted return compared to its worst performing month or time frame. The only difference in calculation for the Calmar Ratio is the denominator. Here is the Calmar Ratio formula:

Calmar Ratio = (Portfolio Return — Risk free rate) / (Maximum portfolio drawdown)


## Optimization and automation
With countless APIs and open source libraries to create trading bots, portfolio analysis tools and so on, it is tempting to optimize and automate once we have found promising trading strategies. There are a lot of pitfalls though, so let's briefly discuss the possibilities and limitations. As a rule of thumb, any strategy we create needs to go through a certain evolution to avoid surprise losses.

* Ideation: does the strategy make sense, is it based on a creative or at least credible hypothesis *WHY* it should make money?
* Backtest: the strategy should have a positive but most importantly somewhat reliable historical performance when run through Backtrader or Zipline
* Validation: the strategy needs to survive out-of-sample runs and have adequate statistical properties, ideally low correlation to other stategies we employ
* Paper trading: we need to expose the strategy to a dry run of trading simulation in a real market environment, or if that is not possible trade with miniscule ADA
* Monitoring: before we automate, and while we run automated bot trading, it is vital to have "kill switches" and/or human supervision in case something unexpected happens

There are some open source Pythonic or Python-friendly crypto trading libraries and frameworks can be considered for Cardano native tokens. We not recommend any of them, but have used Hummingbot ourselves. Please read the part about risks and pitfalls below thoroughly if you consider bots!!!

* [ccxt](https://github.com/ccxt/ccxt) (CryptoCurrency eXchange Trading Library)

Supports multiple exchanges
Can be adapted for Cardano if the exchange supports it
Provides a unified API for trading operations

* [freqtrade](https://github.com/freqtrade/freqtrade)

Open-source crypto trading bot framework
Supports multiple exchanges and strategies
Can be extended to work with Cardano native tokens

* [Hummingbot](https://github.com/hummingbot/hummingbot)

Open-source market making bot
Supports multiple exchanges and assets
Community-driven development with potential for Cardano integration

**Merits and marketing pitches**

The main selling points of these solutions often include:
* Automation: 24/7 trading without constant human intervention
*  Speed: Faster execution of trades compared to manual trading
* Emotion-free trading: Bots follow predefined strategies without emotional bias
* Backtesting capabilities: Ability to test strategies on historical data
* Customization: Flexibility to implement custom trading strategies
* Multi-asset support: Ability to trade multiple cryptocurrencies simultaneously

**Risks and problems**

There are several potential issues to consider:
* Market volatility: Native token markets are highly volatile, and bots may not adapt quickly to sudden changes or "whiplash", i.e. get exploited by stop loss chasing players.
* DEX risk: on Cardano there are a lot of DEXes and some trade very little volume in certain tokens. Consider aggregators or choose the most liquid DEX.
* Technical failures: Bugs, network issues, or exchange API problems can lead to unexpected behavior especially with open source libraries that are not well maintained. Also, popular bot scripts could be well known with exploits already waiting for your deployment.
* Lack of human judgment: Bots can't interpret news or broader market sentiment, or when they are parsing newsfeeds are prone to be misled by fake news
* Over-optimization: Strategies that perform well in backtests may fail in live markets
* Security risks: Bots require API access to your exchange account, creating potential security vulnerabilities
* Liquidity issues: For less popular Cardano native tokens, low liquidity can lead to slippage and difficulty executing trades
* Smart contract risks: If interacting with DeFi protocols, smart contract vulnerabilities could lead to losses
* Complexity of Cardano's eUTXO model: This can make certain types of automated trading more challenging compared to account-based blockchains (which are more common and probably behind some of the bot logic that went into the most popular scripts)
  
When considering automated trading for native tokens, it is crucial to thoroughly understand these risks and implement robust risk management strategies.


## "Rug-pulls"

**Rug pulls** are a significant concern in the crypto space, and Cardano native tokens despite the overall high level of integrity of the ecosystem are no exception. Understanding rug pulls for the investor and in our portfolio construction is crucial as it can skew performance and creates many idiosyncracies for native token portfolios that have no parallel in traditional asset classes except maybe penny stocks.

What is a Rug Pull?
A rug pull is a type of scam in the cryptocurrency world where the developers of a project suddenly withdraw all liquidity or funds, effectively "pulling the rug" out from under investors. This typically results in the token's value plummeting to near zero, leaving investors with worthless assets and no recourse. A slow burn liquidation among a cascade of soothing or bullish news is also a possibility, we may call this "salami rug pull" borrowed from the term "salami crash" where a stock market sell off occurs over several sell-off events instead of a big Black Monday style breakdown.

Rug pulls traditionally occur in decentralized finance (DeFi) projects, particularly those involving newly launched tokens on decentralized exchanges or peer to peer. These projects often lure investors with alleged technical novely and innovation, a large team, huge social media followers (initially mostly fake accounts, of course) but they are designed from the start to defraud.

**How Can a Token Investor Spot Hallmarks or Tell-Tale Signs?**
Spotting a rug pull can be challenging, especially because the projects often appear legitimate at first. However, there are several red flags that investors can look out for:

* Anonymous or Unverifiable Team:
Projects where the team members are anonymous or have unverifiable identities should be approached with caution. Legitimate projects usually have transparent teams with verifiable backgrounds.

* No Audit or Poor Quality Audits:
Reputable protocols usually undergo audits by well-known security firms. A lack of audit or an audit by an unknown or dubious firm is a red flag.

* Large fully diluted market cap
Tokens with an extremely high supply can be manipulated easily. Additionally, if a small group holds a large percentage of the tokens, they can easily dump them, causing the price to crash.

* No Locked Liquidity:

In a rug pull, developers withdraw liquidity from the DEX. Legitimate projects often lock liquidity for a specified period to assure investors that the team can't withdraw it immediately.

* Unrealistic Returns:

Promises of extremely high returns, especially if they seem too good to be true, are often a sign of a scam. Always be skeptical of projects that guarantee high returns with little to no risk.

* Sudden Changes in Project Structure or Tokenomics:
Unexpected changes in token distribution, supply, or governance structure can indicate that the project is gearing up for a rug pull.

* No Clear Use Case or Roadmap:
A project without a clear use case, roadmap, or development plan is likely to be a cash grab. Always look for projects that have a well-defined purpose and a detailed plan for future growth.

* Suspicious Marketing Tactics:
Over-reliance on hype, especially if the project is being pushed by influencers with no technical knowledge, can be a red flag. Be cautious of projects that spend more on marketing than on development.

**How Does the Risk of Rug Pulls Affect the Construction of Crypto Portfolios?**
The risk of rug pulls significantly impacts how investors should approach building a crypto portfolio:

Diversification:

Given the high risk of rug pulls, diversification is crucial. By spreading investments across multiple projects, especially established ones, investors can mitigate the risk of any single project collapsing.
Due Diligence:

Investors should conduct thorough research on any project before investing. This includes reading whitepapers, analyzing the development team, checking for audits, and understanding the project's use case and tokenomics.
Focus on Established Projects:

While new projects can offer high returns, they also carry higher risks. A balanced portfolio should include established cryptocurrencies like Bitcoin or Ethereum, which are less susceptible to rug pulls.
Liquidity Considerations:

Investing in tokens with locked liquidity or those on reputable exchanges reduces the risk of rug pulls. Consider avoiding projects that are only available on smaller, less regulated platforms.
Risk Management:

Allocate only a small portion of the portfolio to high-risk, high-reward projects. This way, even if one project fails, it won't devastate the entire portfolio.

Maybe most importantly, **hope is not a viable investment strategy**. If things go badly, for example your token of choice woefully underperforms peers or has a few shar jumps followed by long periods of liquiditation, it is often better to exit pre-emptively instead of "giving the benefit of the doubt". Real breakthroughs are generally not made overnight, and especially developing on Cardano and building sustainable, loyal community takes time. Sell first, ask questions later. And if you were wrong to exit, you can always get back in. Some successful protocols have gone 20x or 100x over several years, so be in it for the long run and the big score, while cutting losers and possible rug pulls.


## Other factors
Below are some additional risks that native token traders and investors may face. These are not unique to Cardano native tokens and probably not on the radar of most investors at the moment who do not use hedges and see their native token positions either as short term trading strategies or "moonshot" long-term investments into an undervalued and high potential project. However, we like to list them here for completeness and as they may be highly significant to your particular approach to the market.

### Trading strategies vs buy-and-hold
When using backtesting libraries or heatmap optimization, we sometimes forget that our project-agnostic trading signals are not judgments about the ecosystem or protocol we invest in. Letting your positive feelings influence the trading strategy is as risky as letting buy signals with positive expected value color the assessment of long term outlook. We should always keep investing and trading apart. A strategy has clearly defined stop loss levels or exit signals to keep us clear of large losses. Long-term investments on the other hand may be quite happy about the occasional drawdown to add cheaply to a position we believe in for the long haul.

### Biases and overfitting
In the real of portfolio and trading strategy design, no mistake is as ubiquitous as overfitting the data. The more degrees of freedom, the more optimization, and the better the backtesting result, the less likely it is that paper profit can be realised in the forward-looking real world. We have discussed this in some depth in the Heapmap section and Backtesting, but the subject deserves some outside references as it is so important to success as a systematic trader. Marco Lopez de Prado wrote the ["bible"](https://www.amazon.com/Advances-Financial-Machine-Learning-Marcos) of machine learning in finance and this is a difficult but excellent read. The [internet](https://hub.algotrade.vn/knowledge-hub/biases-in-algorithmic-trading/) has many great sources to the subject for beginners as well.

### Oracle-risk
When trading on decentralized exchanges, some traders use smart contracts to interact with the market in some way, be it to utilize "flash loans" or adjust risk in the event of adverse price moves. As we are operating in a young and volatile market, with many functions carried out by new and unproven parts of the plumbing, it is important to be aware that any price-feed could become stale, show the result of automated or erroneous trading at extreme prices, or be subject to manipulation or gaming. This is what [S&P Global](https://www.spglobal.com/en/research-insights/special-reports/utility-at-a-cost-assessing-the-risks-of-blockchain-oracles) has to say about the risk: *"Oracles enhance the efficacy of smart contracts by giving access to off-chain data and computing power, as well as the ability to export data off-chain to the real world. Oracles can help to address interoperability between financial market participants that use different public and private blockchains. Evaluating the risks of smart contracts also means considering the key vulnerabilities introduced by oracles: concentration, data quality and technical risks."*

### Basis risk
Basis risk is a term that originates in the futures markets. As futures contracts only require the full principal payment versus delivery of the underlying asset at some specified future date, interest rates that can be earned on the funds earmarked for purchase or other factors like staking rewards, dividends, voting power, storage costs or supply imbalances and infrastructure imperfections can cause large differences in the price gap between asset (for example ADA in your wallet that has the right to vote, be staked etc) and the futures contract price. Differences in the difference between the hedge and the asset to be hedged are called [BASIS](https://moneyterms.co.uk/basis-risk/), and this basis can fluctuate causing unwanted changes in profit and loss. What the hedger actually wants is a perfect fit. If you hedge ADA with Bitcoin futures, you have a huge basis risk, if you hedge Apple stock with Apple single stock futures, a much smaller risk. Bear in mind that this relationship can change in the future, and perfectly safe "baskets" that are used by everyone and everyday can suddenly stop to work as hedges. There are a lot of academic papers how this and that basket of cryptoassets "perfectly" correlates with an unhedgeable ETF or coin price, but not being aware of the risk of breakdown in this relationship can cause unnecessary and/or large [losses](https://www.e-education.psu.edu/ebf301/node/571).
