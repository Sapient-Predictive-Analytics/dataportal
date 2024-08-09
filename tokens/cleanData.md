## Data vs Clean Data: How to Screen, Transform, Merge or Reshape Raw Token Time Series Data

Most of the time, we receive time series data from a DEX's API, some aggregator source or download it directly from someone else. It is highly unlikely that this data represents the reality of what actually can be achieved in the market at any point in time. From obvious "fat finger" errors like 9.1112 instead of 0.1112 as the token's high price, the opening could be identical to the previous' day's close because the market "never closes" and timezones or trading hours are not established in crypto markets. Also, the low could be achieved by a cascading AMM fill for stop loss orders being triggered where the final order to execute is for a few hundred ADA at a price that is close to zero. Data manipulation or data connectivity problems during the API call could be other sources or wrong or mangled data. Ideally, we want to run a few scripts over our time series to find the most harmful errors that could badly skew our trading strategy analysis, or lead to wrong risk measurements.

We use a simple Python script you can find in this folder **dataScanner.py** to scan data and produce a "quality report". This flags potentially problematic date format, outlier detection using the [IQR method](https://medium.com/@pp1222001/outlier-detection-and-removal-using-the-iqr-method-6fab2954315d) and descriptive statistics. It also reports on the existence of "not a number". The report also has a list at the bottom of the exact dates potential outliers occur, so we can manually check and correct the data in Excel, or run scripts to remedy problems if there are more than a few.

### The Data Quality Analysis Report Program

~~~
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
~~~

### The Output of the Report (Example: Wing Rider Token)

**Data Quality Analysis Report**
**===========================**

Column Names:
['date', 'open', 'high', 'low', 'close', 'volume']

Date Format: 2022-07-14
Date Range: 2022-07-14 00:00:00 to 2024-08-09 00:00:00

Percentage of NaN values in each column:
date: 0.00%
open: 0.00%
high: 0.00%
low: 0.00%
close: 0.00%
volume: 0.00%

High and Low values for numeric columns:
open:
  High: 1.489598
  Low: 0.050753
high:
  High: 1.834970
  Low: 0.050753
low:
  High: 1.394460
  Low: 0.050716
close:
  High: 1.489598
  Low: 0.050734
volume:
  High: 2242306.788919
  Low: 83.840115

Basic statistics for numeric columns:
                      date        open  ...       close        volume
count                  758  758.000000  ...  758.000000  7.580000e+02
mean   2023-07-27 12:00:00    0.300665  ...    0.299318  5.840136e+04
min    2022-07-14 00:00:00    0.050753  ...    0.050734  8.384011e+01
25%    2023-01-19 06:00:00    0.122701  ...    0.121516  1.198718e+04
50%    2023-07-27 12:00:00    0.305998  ...    0.305058  2.749772e+04
75%    2024-02-01 18:00:00    0.404336  ...    0.403845  6.314951e+04
max    2024-08-09 00:00:00    1.489598  ...    1.489598  2.242307e+06
std                    NaN    0.228743  ...    0.227199  1.320554e+05

[8 rows x 6 columns]

Number of duplicate rows: 0

Potential outliers (using IQR method):
open: 22 potential outliers
high: 23 potential outliers
low: 21 potential outliers
close: 21 potential outliers
volume: 59 potential outliers

Trading Volume Analysis:
Average Daily Volume: 58401.36
Highest Volume Day: 2022-08-02 00:00:00 (2242306.79)
Lowest Volume Day: 2024-07-15 00:00:00 (83.84)

Annualized Volatility: 58.77%

A plot of price and volume history has been saved as 'price_volume_history.png'

Detailed Outlier Report:

open:
Extreme outliers (3 * IQR method):
  2022-07-15 00:00:00: 1.489598
  2022-07-16 00:00:00: 1.417721
  2022-07-17 00:00:00: 1.393708
  2022-07-18 00:00:00: 1.363342
  2022-07-19 00:00:00: 1.284046

high:
Extreme outliers (3 * IQR method):
  2022-07-14 00:00:00: 1.834970
  2022-07-15 00:00:00: 1.489598
  2022-07-16 00:00:00: 1.485451
  2022-07-17 00:00:00: 1.401535
  2022-07-18 00:00:00: 1.369497
  2022-07-19 00:00:00: 1.287530

low:
Extreme outliers (3 * IQR method):
  2022-07-15 00:00:00: 1.394460
  2022-07-16 00:00:00: 1.393707
  2022-07-17 00:00:00: 1.357308
  2022-07-18 00:00:00: 1.267492

close:
Extreme outliers (3 * IQR method):
  2022-07-14 00:00:00: 1.489598
  2022-07-15 00:00:00: 1.417721
  2022-07-16 00:00:00: 1.393708
  2022-07-17 00:00:00: 1.363342
  2022-07-18 00:00:00: 1.284046
