import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from preproc.data import clean_data_electricity

def scale_electricity_data(scaling_method='standard'):
    """
    Load, clean, and scale electricity data using specified scaling method.

    Parameters:
        scaling_method (str): The scaling method to use ('standard', 'minmax', or 'robust').

    Returns:
        pandas.DataFrame: A DataFrame of scaled electricity data.
    """
    # Load and clean the data
    electricity_df = clean_data_electricity()
    electricity_df = electricity_df.dropna()

    # Convert 'Date' to datetime and set as index
    try:
        electricity_df['date_gmt+1'] = pd.to_datetime(electricity_df['date_gmt+1'], utc=True)
        electricity_df.set_index('date_gmt+1', inplace=True)
        electricity_df.index.rename('Date', inplace=True)
    except Exception as e:
        print(f"Error processing the Date column: {e}")
        sys.exit(1)

    # Convert all non-date columns to floats
    for column in electricity_df.select_dtypes(include=['object']).columns:
        electricity_df[column] = pd.to_numeric(electricity_df[column], errors='coerce')

    # Select the scaler based on the method
    if scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        print(f"Unsupported scaling method: {scaling_method}")
        sys.exit(1)

    # Apply scaling
    electricity_scaled = scaler.fit_transform(electricity_df)
    electricity_scaled_df = pd.DataFrame(electricity_scaled, columns=electricity_df.columns, index=electricity_df.index)

    return electricity_scaled_df
