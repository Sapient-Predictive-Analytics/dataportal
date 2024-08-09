import pandas as pd
import numpy as np

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
