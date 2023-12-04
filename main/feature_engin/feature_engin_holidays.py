import sys
import os

# Get the current working directory
current_dir = os.getcwd()

# Assuming your notebook is in the 'feature_engin' directory,
# and you want to add 'main' to the path
main_dir = os.path.dirname(current_dir)
sys.path.append(main_dir)


import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from preproc.data import clean_data_holidays

def scale_holidays():
    try:
        holidays_df = clean_data_holidays()
    except Exception as e:
        raise RuntimeError(f"Error loading holidays data: {e}")

    # Convert 'date' column to datetime
    holidays_df['date'] = pd.to_datetime(holidays_df['date'])

    # Replace empty strings with NaN in 'holiday' column
    holidays_df['holiday'] = holidays_df['holiday'].replace('', pd.NA)

    # Drop rows with NaN values in 'holiday'
    holidays_df = holidays_df.dropna(subset=['holiday'])

    if holidays_df.empty:
        raise RuntimeError("After cleaning, the DataFrame is empty.")

    scaler = MinMaxScaler()

    # Convert 'holiday' column to numeric
    holidays_df['holiday'] = pd.to_numeric(holidays_df['holiday'], errors='coerce')

    # Set 'date' as index for subsequent operations
    holidays_df.set_index('date', inplace=True)

    # Handle duplicates during resampling
    holidays_df = holidays_df[~holidays_df.index.duplicated(keep='first')]
    holidays_df = holidays_df.resample('15T').ffill()

    return holidays_df
