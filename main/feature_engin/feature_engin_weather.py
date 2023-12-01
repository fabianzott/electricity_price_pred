import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

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
    weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], utc=True)

    # Remove rows where the Date is NaN
    weather_df = weather_df[weather_df['datetime'].notna()]

    # Set 'Date' as the index
    weather_df.set_index('datetime', inplace=True)

    # Remove any potential duplicate indices
    weather_df = weather_df[~weather_df.index.duplicated(keep='first')]

    # Creating scalers for different types of features
    scaler_temp = StandardScaler()
    scaler_windspeed = RobustScaler()

    # Columns to be scaled
    temp_columns = ['temp_north', 'temp_south', 'temp_brocken']
    windspeed_columns = ['windspeed_north', 'windspeed_south', 'windspeed_brocken']

    # Applying StandardScaler to temperature features
    weather_df[temp_columns] = scaler_temp.fit_transform(weather_df[temp_columns])

    # Applying RobustScaler to windspeed features
    weather_df[windspeed_columns] = scaler_windspeed.fit_transform(weather_df[windspeed_columns])

    # solar columns for MinMaxScaler
    solar_columns = ['solarradiation_south', 'solarenergy_south', 'solarradiation_brocken', 'solarenergy_brocken']

    # Creating and applying MinMaxScaler to the specific solar data
    scaler_solar_specific = MinMaxScaler()
    weather_df[solar_columns] = scaler_solar_specific.fit_transform(weather_df[solar_columns])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    weather_df = weather_df.resample('15T').ffill()




    return weather_df
