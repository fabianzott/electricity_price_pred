import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from preproc.data import clean_data_weather

def scale_weather():
    """
    Loads, processes, and scales weather data.
    Returns: Processed DataFrame with scaled weather data.
    """
    try:
        weather_df = clean_data_weather()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone
    #coal_price_df['Date'] = pd.to_datetime(coal_price_df['Date'], utc=True)

    # Remove rows where the Date is NaT
    #coal_price_df = coal_price_df[coal_price_df['Date'].notna()]

    # Set 'Date' as the index
    #coal_price_df.set_index('Date', inplace=True)

    # Remove any potential duplicate indices
    #coal_price_df = coal_price_df[~coal_price_df.index.duplicated(keep='first')]

    #scaler = MinMaxScaler()

    # Scale 'coal_adj_close' column
    #coal_price_df['coal_adj_close'] = scaler.fit_transform(coal_price_df[['coal_adj_close']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    #coal_price_df = coal_price_df.resample('15T').ffill()

    return weather_df
