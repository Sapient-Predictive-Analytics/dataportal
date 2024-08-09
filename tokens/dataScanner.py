# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from dateutil.parser import parse
import matplotlib.pyplot as plt

def analyze_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, parse_dates=['date'])

    print("Data Quality Analysis Report")
    print("===========================\n")

    # Print column names
    print("Column Names:")
    print(df.columns.tolist())
    print()

    # Analyze date format
    date_col = df['date']
    date_formats = date_col.apply(lambda x: x.strftime('%Y-%m-%d')).unique()
    print(f"Date Format: {date_formats[0]}")
    print(f"Date Range: {date_col.min()} to {date_col.max()}")
    print()

    # Percentage of NaN values in each column
    print("Percentage of NaN values in each column:")
    nan_percentages = df.isnull().mean() * 100
    for col, percentage in nan_percentages.items():
        print(f"{col}: {percentage:.2f}%")
    print()

    # High and low values for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print("High and Low values for numeric columns:")
    for col in numeric_cols:
        print(f"{col}:")
        print(f"  High: {df[col].max():.6f}")
        print(f"  Low: {df[col].min():.6f}")
    print()

    # Basic statistics
    print("Basic statistics for numeric columns:")
    print(df.describe())
    print()

    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    print()

    # Check for outliers using IQR method
    print("Potential outliers (using IQR method):")
    outliers_report = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        print(f"{col}: {len(outliers)} potential outliers")
        outliers_report[col] = {'count': len(outliers), 'data': outliers}
    print()

    # Analyze trading volume
    print("Trading Volume Analysis:")
    print(f"Average Daily Volume: {df['volume'].mean():.2f}")
    print(f"Highest Volume Day: {df.loc[df['volume'].idxmax(), 'date']} ({df['volume'].max():.2f})")
    print(f"Lowest Volume Day: {df.loc[df['volume'].idxmin(), 'date']} ({df['volume'].min():.2f})")
    print()

    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change()

    # Calculate volatility (standard deviation of returns)
    volatility = df['daily_return'].std() * np.sqrt(252)  # Annualized volatility
    print(f"Annualized Volatility: {volatility:.2%}")

    # Plot price and volume
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['close'])
    plt.title('Price History')
    plt.ylabel('Price')

    plt.subplot(2, 1, 2)
    plt.bar(df['date'], df['volume'])
    plt.title('Volume History')
    plt.ylabel('Volume')

    plt.tight_layout()
    plt.savefig('price_volume_history.png')
    plt.close()

    print("\nA plot of price and volume history has been saved as 'price_volume_history.png'")

    # Detailed outlier report
    print("\nDetailed Outlier Report:")
    for col, data in outliers_report.items():
        print(f"\n{col}:")
        if data['count'] <= 6:
            print("Outlier dates:")
            for _, row in data['data'].iterrows():
                print(f"  {row['date']}: {row[col]:.6f}")
        else:
            # Perform 3 * IQR analysis for columns with more than 6 outliers
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            extreme_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            print(f"Extreme outliers (3 * IQR method):")
            for _, row in extreme_outliers.iterrows():
                print(f"  {row['date']}: {row[col]:.6f}")

# Call the function with our CSV file path
analyze_csv('WRT.csv')