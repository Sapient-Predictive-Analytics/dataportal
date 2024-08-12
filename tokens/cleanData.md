## How to Screen and Clean Raw Token Time Series Data

Most of the time, we receive time series data from a DEX's API, some aggregator source or download it directly from someone else. It is highly unlikely that this data represents the reality of what actually can be achieved in the market at any point in time. From obvious errors like wrong separators or wrong date format, wrong ordering of columns or even dates is possible. Very often, open data is identical to close data of the previous day as we trade 24/7. Some values are not tradeable, for example the low could be achieved by a cascading AMM fill for stop loss orders being triggered where the final order to execute is for a few hundred ADA at a price that is close to zero. A trader observing the market would have no chance to enter at the price printed later in the DEX report. Data manipulation or data connectivity problems during the API call could be other sources or wrong or mangled data. Ideally, we want to run a few scripts over our time series to find the most harmful errors that could badly skew our trading strategy analysis, or lead to wrong risk measurements.

We use a simple Python script you can find in this folder [**dataScanner.py**](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/dataScanner.py) to scan data and produce a "quality report". This flags potentially problematic date format, outlier detection using the [IQR method](https://medium.com/@pp1222001/outlier-detection-and-removal-using-the-iqr-method-6fab2954315d) and descriptive statistics. It also reports on the existence of "not a number". The report also has a list at the bottom of the exact dates potential outliers occur, so we can manually check and correct the data in Excel, or run scripts to remedy problems if there are more than a few.

***

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

***

### The Output of the Report (Example: Wing Rider Token)

***

## Data Quality Analysis Report

### Column Names

- date
- open
- high
- low
- close
- volume


### Date Information

- **Date Format:** 2022-07-14
- **Date Range:** 2022-07-14 to 2024-08-09


### Percentage of NaN Values

| Column | NaN Percentage |
|--------|----------------|
| date | 0.00% |
| open | 0.00% |
| high | 0.00% |
| low | 0.00% |
| close | 0.00% |
| volume | 0.00% |



### High and Low Values for Numeric Columns

| Column | High | Low |
|--------|------|-----|
| open | 1.489598 | 0.050753 |
| high | 1.834970 | 0.050753 |
| low | 1.394460 | 0.050716 |
| close | 1.489598 | 0.050734 |
| volume | 2242306.788919 | 83.840115 |



### Basic Statistics for Numeric Columns

|       | date                |        open |        high |         low |       close |           volume |
|:------|:--------------------|------------:|------------:|------------:|------------:|-----------------:|
| count | 758                 | 758         | 758         | 758         | 758         |    758           |
| mean  | 2023-07-27 12:00:00 |   0.300665  |   0.305987  |   0.294209  |   0.299318  |  58401.4         |
| min   | 2022-07-14 00:00:00 |   0.0507535 |   0.0507535 |   0.0507161 |   0.0507343 |     83.8401      |
| 25%   | 2023-01-19 06:00:00 |   0.122701  |   0.122729  |   0.121452  |   0.121516  |  11987.2         |
| 50%   | 2023-07-27 12:00:00 |   0.305998  |   0.308991  |   0.302119  |   0.305058  |  27497.7         |
| 75%   | 2024-02-01 18:00:00 |   0.404336  |   0.412074  |   0.395286  |   0.403845  |  63149.5         |
| max   | 2024-08-09 00:00:00 |   1.4896    |   1.83497   |   1.39446   |   1.4896    |      2.24231e+06 |
| std   | nan                 |   0.228743  |   0.237738  |   0.220421  |   0.227199  | 132055           |


### Duplicate Rows

**Number of duplicate rows:** 0


### Potential Outliers (IQR Method)

- **open:** 22 potential outliers
- **high:** 23 potential outliers
- **low:** 21 potential outliers
- **close:** 21 potential outliers
- **volume:** 59 potential outliers



### Trading Volume Analysis

- **Average Daily Volume:** 58401.36
- **Highest Volume Day:** 2022-08-02 (2242306.79)
- **Lowest Volume Day:** 2024-07-15 (83.84)


### Volatility

**Annualized Volatility:** 58.77%


![Price and Volume History](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/price_volume_history.png)


### Detailed Outlier Report

#### open

**Extreme outliers (3 * IQR method):**

| Date | Value |
|------|-------|

| 2022-07-15 | 1.489598 |

| 2022-07-16 | 1.417721 |

| 2022-07-17 | 1.393708 |

| 2022-07-18 | 1.363342 |

| 2022-07-19 | 1.284046 |



#### high

**Extreme outliers (3 * IQR method):**

| Date | Value |
|------|-------|

| 2022-07-14 | 1.834970 |

| 2022-07-15 | 1.489598 |

| 2022-07-16 | 1.485451 |

| 2022-07-17 | 1.401535 |

| 2022-07-18 | 1.369497 |

| 2022-07-19 | 1.287530 |



#### low

**Extreme outliers (3 * IQR method):**

| Date | Value |
|------|-------|

| 2022-07-15 | 1.394460 |

| 2022-07-16 | 1.393707 |

| 2022-07-17 | 1.357308 |

| 2022-07-18 | 1.267492 |



#### close

**Extreme outliers (3 * IQR method):**

| Date | Value |
|------|-------|

| 2022-07-14 | 1.489598 |

| 2022-07-15 | 1.417721 |

| 2022-07-16 | 1.393708 |

| 2022-07-17 | 1.363342 |

| 2022-07-18 | 1.284046 |



#### volume

**Extreme outliers (3 * IQR method):**

| Date | Value |
|------|-------|

| 2022-07-14 | 1710444.909539 |

| 2022-07-15 | 230131.956095 |

(... 31 more rows ...)

***

## Data Cleaning Remedies
For an asset as volatile and illiquid as Cardano native tokens, especially those of smaller protocols or excluded from DEX aggregation, automatically removing or smooting outliers is likely counterproductive. Imagine we have a 100% jump on one day and replace it with a forward fill until the token reverts back to its initial level. All trading opportunities that may be very significant are then removed as well! If we are lucky, the data problems are obvious from the above report and we can easily remove them manually. If for example out of 1000 days of WMT history, I have 9.xx values instead of 0.xx values, this is obviously an API- or "fat finger" issue. An AI assistant may also help if we have more than a handful or they are not obvious to spot when plotting the data. 

However, a few simple Python scripts can help. Some ideas:

* Normalize volume: for example, we can use 10 bins for volume ranges instead of absolute tokens
* Calculate ADA volume instead of token numbers for volume
* Use log of token price instead of absolute ADA price if the period we analyze saw huge rise of fall in the level
* Remove days with no trading or NaN (not a number) data
* Ensure date format is consistent and ordered
* Ensure OHLC data is indeed allocated to the right column, i.e. high is the highest or equal, low is the lowest or equal etc.

The most powerful remedies are usually those that involve the trading strategy level. For example, trusting volume in native tokens for trading signals is often a bad idea, as DEX aggregation and over the counter trading can obscure what is really going on. Also, as most DEXes trade 24/7, relying on candlesticks or there being any significant difference between today's close and tomorrow's open are probably not real opportunities. 

The function below covers some of these suggestions and can be found in [**csvCleaning.py**](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/tokens/csvCleaning.py)

~~~
def clean_and_enhance_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    print("Data Cleaning and Enhancement Report")
    print("====================================\n")

    # Check and convert date column to datetime
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            print("Date column successfully converted to datetime.")
        except:
            print("Error: Unable to convert date column to datetime.")
            return

        # Sort by date
        df = df.sort_values('date')
        print("Data sorted chronologically by date.")

        # Remove rows with NaN in date column
        nan_dates = df['date'].isna().sum()
        df = df.dropna(subset=['date'])
        print(f"Removed {nan_dates} rows with NaN dates.")

    else:
        print("Error: Date column not found in the CSV file.")
        return

    # Fix OHLC data if necessary
    ohlc_columns = ['open', 'high', 'low', 'close']
    if all(col in df.columns for col in ohlc_columns):
        def fix_ohlc(row):
            o, h, l, c = row['open'], row['high'], row['low'], row['close']
            fixed_h = max(o, h, l, c)
            fixed_l = min(o, h, l, c)
            return pd.Series({'high': fixed_h, 'low': fixed_l})

        original_df = df.copy()
        df[['high', 'low']] = df.apply(fix_ohlc, axis=1)
        changes = ((df[['high', 'low']] != original_df[['high', 'low']]).sum().sum())
        print(f"Fixed {changes} OHLC inconsistencies.")
    else:
        print("Warning: OHLC columns not found. Skipping OHLC fix.")

    # Create ADA volume column
    if 'volume' in df.columns and 'close' in df.columns:
        df['ada_volume'] = df['volume'] * df['close']
        print("Created 'ada_volume' column.")
    else:
        print("Warning: Unable to create 'ada_volume' column. Missing 'volume' or 'close' column.")

    # Create Volume bin column
    if 'volume' in df.columns:
        df['volume_bin'] = pd.qcut(df['volume'], q=10, labels=False) + 1
        print("Created 'volume_bin' column with deciles from 1 to 10.")
    else:
        print("Warning: Unable to create 'volume_bin' column. Missing 'volume' column.")

    # Save the cleaned and enhanced data
    output_file = 'cleaned_enhanced_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\nCleaned and enhanced data saved to {output_file}")

    # Print summary statistics
    print("\nSummary Statistics:")
    print(df.describe())

    return df

# Call the function with our CSV file path
cleaned_df = clean_and_enhance_data('WRT.csv')
~~~

### Pandas as a go-to tool for data cleaning
The Pandas library provides powerful functions like groupby and apply to create new improved columns, manipulate timezones and datetime objects to fit our needs, or aggregate data and create signals. The Groupby object is a very useful data preparation step to avoid resource-consuming iteration and work database-like with our CSV data. The first parameter to .groupby() can accept several different arguments:

* A column or list of columns
* A dict or pandas Series
* A NumPy array or pandas Index, or an array-like iterable of these
  
We can take advantage of the latter to group by for example bins of average scores etc.

A more detailed breakdown of how groupby works:

* **Split**: The data is divided into groups based on some criteria. This criteria can be one or more columns in your DataFrame. When we call groupby on a DataFrame, we specify which column(s) we want to group by. This divides the DataFrame into multiple groups based on unique values in the specified column(s).

* **Apply**: A function is applied to each group independently. This function can be a built-in aggregation function (such as sum, mean, count, etc.), a custom function, or even a combination of multiple functions. We apply various functions to each group. Common functions include aggregation: calculating a single value for each group, such as mean, sum, count, etc. Transformation: returning an object that's the same size as the group, typically used for normalization or other element-wise operations. Filtration: Returning subsets of the original object based on some group-wise criteria.

* **Combine**: The results of the function applications are combined into a new DataFrame or Series. The results of the applied functions are combined into a new DataFrame or Series, which can be used for further analysis or visualization.


**Risk of over-automation**
While it is good to use scripts and APIs for work with large datasets and choose the right instrument, time horizon and approach for our trading strategies, good data cleaning should involve some human element. This adds a "sanity check" element and also familiarizes ourselves with the dataset.
