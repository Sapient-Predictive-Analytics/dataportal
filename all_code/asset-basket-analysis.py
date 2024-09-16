# -*- coding: utf-8 -*-
"""
Created on Tue Aug 5 15:17:15 2024

@author: sapient
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from scipy import stats

def load_data(tokens):
    dataframes = {}
    for token in tokens:
        try:
            df = pd.read_csv(f"{token}.csv")
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            elif df.index.name == 'date':
                df.index = pd.to_datetime(df.index)
            else:
                print(f"Warning: 'date' column not found in {token}.csv")
                continue
            
            if 'close' not in df.columns:
                print(f"Warning: 'close' column not found in {token}.csv")
                continue
            
            dataframes[token] = df
        except Exception as e:
            print(f"Error loading {token}.csv: {str(e)}")
    return dataframes

def calculate_equal_weight_basket(dataframes, tokens):
    combined_df = pd.concat([df['close'] for df in dataframes.values()], axis=1, keys=tokens)
    equal_weight_basket = combined_df.mean(axis=1)
    return equal_weight_basket

def calculate_market_cap_weight_basket(dataframes, tokens, token_supplies):
    combined_df = pd.concat([df['close'] for df in dataframes.values()], axis=1, keys=tokens)
    
    market_cap_basket = pd.Series(dtype=float)
    
    for month_start, month_group in combined_df.groupby(pd.Grouper(freq='MS')):
        if month_group.empty:
            continue
        
        market_caps = month_group.iloc[0] * token_supplies
        weights = market_caps / market_caps.sum()
        
        month_basket = (month_group * weights).sum(axis=1)
        market_cap_basket = pd.concat([market_cap_basket, month_basket])
    
    return market_cap_basket

def calculate_descriptive_stats(results, start_date='2023-01-01', end_date='2023-12-31', risk_free_rate=0.05):
    """
    Calculate descriptive statistics for the baskets.
    
    :param results: DataFrame containing both baskets
    :param start_date: Start date for the analysis period (string 'YYYY-MM-DD')
    :param end_date: End date for the analysis period (string 'YYYY-MM-DD')
    :param risk_free_rate: Annual risk-free rate (default 5%)
    :return: DataFrame with descriptive statistics
    """
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

def calculate_var(returns, confidence_level=0.95):
    """Calculate Value at Risk"""
    return np.percentile(returns, 100 * (1 - confidence_level))

def calculate_and_plot_var(results, start_date='2023-01-01', end_date='2023-12-31', confidence_level=0.95, initial_investment=100000):
    """
    Calculate and plot Value at Risk for both baskets in terms of ADA.
    
    :param results: DataFrame containing both baskets
    :param start_date: Start date for the analysis period (string 'YYYY-MM-DD')
    :param end_date: End date for the analysis period (string 'YYYY-MM-DD')
    :param confidence_level: Confidence level for VaR calculation (default 0.95)
    :param initial_investment: Initial investment in ADA (default 100000)
    """
    # Filter data for the specified period
    period_results = results.loc[start_date:end_date]
    
    # Calculate daily returns
    daily_returns = period_results.pct_change().dropna()
    
    # Calculate 20-day rolling VaR for both baskets
    window = 20
    var_equal = daily_returns['Equal Weight Basket'].rolling(window=window).apply(lambda x: calculate_var(x, confidence_level))
    var_market_cap = daily_returns['Market Cap Weight Basket'].rolling(window=window).apply(lambda x: calculate_var(x, confidence_level))
    
    # Calculate cumulative returns
    cumulative_returns_equal = (1 + daily_returns['Equal Weight Basket']).cumprod()
    cumulative_returns_market_cap = (1 + daily_returns['Market Cap Weight Basket']).cumprod()
    
    # Calculate VaR in terms of ADA
    var_ada_equal = var_equal * initial_investment * cumulative_returns_equal
    var_ada_market_cap = var_market_cap * initial_investment * cumulative_returns_market_cap
    
    # Create a new DataFrame with VaR values
    var_df = pd.DataFrame({
        'Equal Weight Basket VaR (ADA)': var_ada_equal,
        'Market Cap Weight Basket VaR (ADA)': var_ada_market_cap
    }, index=daily_returns.index)
    
    # Plot VaR
    plt.figure(figsize=(12, 6))
    plt.plot(var_df.index, var_df['Equal Weight Basket VaR (ADA)'], label='Equal Weight Basket VaR')
    plt.plot(var_df.index, var_df['Market Cap Weight Basket VaR (ADA)'], label='Market Cap Weight Basket VaR')
    
    plt.title(f'{confidence_level*100}% Value at Risk (20-day rolling window)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value at Risk (ADA)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    # Format y-axis to show ADA values
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{abs(x):,.0f} ADA'))
    
    plt.tight_layout()
    plt.show()
    
    return var_df

def calculate_descriptive_stats(results, start_date='2023-01-01', end_date='2023-12-31', risk_free_rate=0.05, confidence_level=0.95):
    """
    Calculate descriptive statistics for the baskets.
    
    :param results: DataFrame containing both baskets
    :param start_date: Start date for the analysis period (string 'YYYY-MM-DD')
    :param end_date: End date for the analysis period (string 'YYYY-MM-DD')
    :param risk_free_rate: Annual risk-free rate (default 5%)
    :param confidence_level: Confidence level for VaR calculation (default 0.95)
    :return: DataFrame with descriptive statistics
    """
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
        stats.loc[column, f'VaR ({confidence_level*100}%)'] = calculate_var(returns, confidence_level)
    
    # Calculate correlation between baskets
    correlation = daily_returns['Equal Weight Basket'].corr(daily_returns['Market Cap Weight Basket'])
    
    # Create a separate DataFrame for correlation
    corr_df = pd.DataFrame({'Correlation': [correlation]}, index=['Between Baskets'])
    
    return stats, corr_df

def dataframe_to_markdown(df):
    """Convert a DataFrame to a markdown-formatted string."""
    markdown = "| " + " | ".join(df.columns) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
    for _, row in df.iterrows():
        markdown += "| " + " | ".join([f"{x:.4f}" if isinstance(x, (int, float)) else str(x) for x in row]) + " |\n"
    return markdown

def plot_baskets(results):
    # Filter data for 2023
    results_2023 = results.loc['2023-01-01':'2023-12-31']

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(results_2023.index, results_2023['Equal Weight Basket'], label='Equal Weight Basket')
    plt.plot(results_2023.index, results_2023['Market Cap Weight Basket'], label='Market Cap Weight Basket')

    # Customize the plot
    plt.title('Comparison of Equal Weight and Market Cap Weight Baskets (2023)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Basket Value', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels

    # Show the plot
    plt.tight_layout()
    plt.show()
    
    
def main():
    tokens = ['MIN', 'MILK', 'GENS', 'SUNDAE', 'WRT']
    token_supplies = [3000000000, 10000000, 100000000, 2000000000, 100000000]
    
    dataframes = load_data(tokens)
    
    if not dataframes:
        print("No valid data loaded. Exiting.")
        return
    
    equal_weight_basket = calculate_equal_weight_basket(dataframes, tokens)
    market_cap_weight_basket = calculate_market_cap_weight_basket(dataframes, tokens, token_supplies)
    
    # Combine results into a single DataFrame
    results = pd.DataFrame({
        'Equal Weight Basket': equal_weight_basket,
        'Market Cap Weight Basket': market_cap_weight_basket
    })
    
    # Plot the normalized baskets
    plot_baskets(results)
    
    # Calculate and plot VaR
    var_df = calculate_and_plot_var(results, start_date='2023-01-01', end_date='2023-12-31')
    
    # Calculate descriptive statistics
    stats, corr = calculate_descriptive_stats(results, start_date='2023-01-01', end_date='2023-12-31', risk_free_rate=0.05)
    
    # Convert stats to markdown
    stats_markdown = dataframe_to_markdown(stats.reset_index().rename(columns={'index': 'Basket'}))
    corr_markdown = dataframe_to_markdown(corr.reset_index().rename(columns={'index': 'Metric'}))
    
    print("\nDescriptive Statistics for 2023:")
    print(stats_markdown)
    print("\nCorrelation between baskets:")
    print(corr_markdown)

if __name__ == "__main__":
    main()
