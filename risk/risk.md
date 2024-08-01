# Risk Management of Native Tokens


## Portfolio construction and analysis

### Equal-weighted basket

### TVL-weighted basket

### Descriptive statistics

### Value at risk

### Sharpe-, Sortino- and Calmar-Ratio

# Risk Management in Native Token Investments: Beyond the Sharpe Ratio

In the dynamic world of native tokens, which often experience huge volatility and liquidity might be moving between DEXes, risk management of strategy designs is crucial in this compelling yet volatile asset class. As the market matures, so too must our approaches to risk management and performance evaluation. While traditional finance has long relied on metrics like the Sharpe ratio to gauge risk-adjusted returns, the unique characteristics of the native token space demand a more nuanced perspective.

The Sharpe ratio, developed by Nobel laureate William Sharpe, has been a cornerstone of portfolio analysis for decades. It measures an investment's excess return relative to its volatility, providing a standardized way to compare different assets or strategies. In essence, it answers the question: How much additional return are we getting for each unit of risk we're taking on?

However, the crypto market's tendency towards extreme price swings and non-normal return distributions has led many analysts to question whether the Sharpe ratio alone is sufficient for evaluating native token investments. Enter alternative metrics like the Sortino and Calmar ratios, which may offer more appropriate benchmarks for judging performance in this unique asset class.

As we delve deeper into these metrics and their applications, we'll explore how a more comprehensive toolkit for risk management can help investors navigate the exciting yet treacherous waters of native token investments. Whether you're a seasoned trader or a curious newcomer, understanding these concepts is crucial for developing robust trading strategies and making informed investment decisions in the blockchain era.

Knowing the Sharpe Ratio, Sortino Ratio, and Calmar Ratio is important for any investor, regardless of how large or small their portfolio is. The goal of this post is to deep dive into the Sharpe Ratio, Sortino Ratio, and Calmar Ratio to show how each measure the performance of an investment and/or investment manager. Regardless of whether you’re a hands-off or hands-on investor, knowing these performance metrics can save you a fortune over the course of your lifetime. Let’s jump right into it by looking at the Sharpe Ratio first!

The Sharpe Ratio measures an investment’s risk adjusted performance relative to its volatility. Nobel Prize winning economist William Sharpe created the ratio in 1966. The comparison of performance to volatility is the main reason that the Sharpe Ratio is the industry standard for performance evaluation. Sharpe Ratio is mostly used by investors, portfolio managers, and traders who focus on the stock market and bond market. Here is the Sharpe Ratio calculation for a more thorough understanding:

Sharpe Ratio = (Portfolio return — Risk free rate) / Portfolio volatility

Let’s define the formula terms for those unfamiliar with them. The portfolio return is the percentage gain or loss in the portfolio. The risk free rate is the rate of return for investing in a 10 year US government bond. Portfolio volatility is measured by standard deviation, a statistical method for measuring data dispersion around the mean of a dataset. Portfolio standard deviation measures the variability of the portfolio. It also accounts for the variability of all assets and asset weightings, where weighting is the percentage of one asset’s value relative to the total portfolio value. Please note that each example from the reading uses annual numbers.

Think of calculation and interpretation as two separate tasks, because focusing too heavily on calculation causes us to lose sight of the forest from the trees. The ideal portfolio Sharpe Ratio has a higher risk adjusted return than its volatility. That’s why a Sharpe of 1 is considered acceptable, while a Sharpe of 1.5 or higher is preferrable. A Sharpe Ratio below 1 means the portfolio’s risk adjusted return is less than its volatility, and the investor is risking more than they are earning. No investor prefers this scenario if there is a better alternative. John from XYZ firm has demonstrated exceptional returns and risk management based on his Sharpe Ratio of 1.57. Let’s review the numerical interpretation of Sharpe ratios before moving on:

Sharpe ratio > 1; the investment manager is earning more than their risk

Sharpe ratio = 1; the investment manager is earning the same as their risk

Sharpe Ratio < 1; the investment manager is earning less than their risk

Consider a theoretical portfolio that only has positively returning months with no consistency of the amount returned. Perhaps one month earned 50%, another month 5%, one month 75%, another month 15%, etc. Regardless of the volatile nature of returns, the portfolio makes money every month. Compared with a lower volatility portfolio that has down months, more consistent return amounts, and returns less overall, Sharpe Ratio may cause us to choose the portfolio that earns less with down months. Certainly, anyone would prefer the fictional portfolio of only money making months.

This is why pairing Sharpe Ratio and Sortino Ratio is important. The Sortino Ratio measures downside portfolio volatility using downside deviation. Downside deviation is the volatility of negatively returning months without accounting for positively returning months. It’s ironic that downside deviation is a positive number despite its focus on downside. It’s calculated the same way as standard deviation using only negative data points. Speaking of similar calculations, the Sortino Ratio formula is the same as the Sharpe ratio formula except downside portfolio volatility replaces total portfolio volatility. Here is the formula for the Sortino Ratio:

Sortino Ratio = (Portfolio return — Risk Free Rate) / Downside portfolio volatility

In some cases, the Sortino Ratio is a better performance metric than the Sharpe Ratio. This is due to the reasons discussed earlier in the fictional portfolio of only money making months. Even if the only positive returns are all over the place causing a higher volatility, this isn’t bad because the portfolio is never down. Sortino Ratio is interpreted similarly to Sharpe Ratio, and here is how to interpret it:

Sortino Ratio > 1; the portfolio is earning more than its downside volatility

Sortino Ratio = 1; the portfolio is earning the same as its downside volatility

Sortino Ratio < 1; the portfolio is earning less than its downside volatility.

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

Calmar Ratio > 1; Total portfolio return is greater than its worst performing period

Calmar Ratio = 1; Total portfolio return is the same as its worst performing period

Calmar Ratio < 1; Total portfolio return is less than its worst performing period

Now that we know how to interpret Calmar Ratio, let’s calculate it for the portfolios used in the Sortino Ratio calculations. Here’s the same table of monthly returns from before:

Portfolio 1’s maximum drawdown is -10% and happened in September. Portfolio 2’s maximum drawdown is -12.13% and happened over the two month spand of September and October. Considering a portfolio 1 return of 30.39%, portfolio 2 return of 39.13%, and risk free rate of 5%, here are the Calmar Ratio calculations for each portfolio:

Portfolio 1 Calmar Ratio = (30.39% return — 5% risk free rate) / (Max drawdown -10%) = 2.54 Calmar Ratio

Portfolio 2 Calmar Ratio = (39.13% return — 5% risk free rate) / (Max drawdown -12.13%) = 2.81 Calmar Ratio

This comparison shows that portfolio 2 outperformed portfolio 1 based on its Calmar Ratio. Portfolio 1 positively returned 2.54 times its maximum downside, while Portfolio 2 positively returned 2.81 times its maximum downside. Something to keep in mind is that Portfolio 2 had a larger drawdown despite outperformance in Calmar Ratio. While some prefer the Sortino Ratio and Calmar Ratio because they measure investment performance relative to downside, the Sharpe Ratio is still the standard performance metric used. When using downside ratios, always consider the downside on a standalone basis as well. A portfolio that has a 100% return and 50% maximum drawdown has a high Calmar Ratio, but a 50% drawdown is unacceptable for any period.

Hopefully this deep dive into Sharpe Ratio, Sortino Ratio, and Calmar Ratio has been useful. To summarize, the Sharpe Ratio is an investment’s risk adjusted performance relative to its total volatility. Sortino Ratio is an investment’s risk adjusted performance relative to its downside volatility. Calmar Ratio is an investment’s risk adjusted performance relative to its maximum drawdown. All three ratios are key performance metrics for portfolio performance, so it’s important to know as an investor regardless of your investment style or total holdings. Next time you’re with your investment manager, ask them what their Sharpe Ratio is. You might be surprised at their answer, and they will most likely be surprised that you asked.

## Optimization and automation

### Trading strategies vs buy-and-hold

### Biases and overfitting

### Oracle-risk

## Other factors

### Basis risk

### Model risk, jumps and "rug-pulls"
