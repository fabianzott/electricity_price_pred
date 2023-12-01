import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from preproc.data import clean_data_electricity
from preproc.data import clean_data_weather
from preproc.data import clean_data_coal, clean_data_gas, clean_data_oil
from preproc.data import clean_data_pmi_index
from preproc.data import clean_data_holidays
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

def scale_coal_prices(scaling_method='minmax'):
    """
    Loads, processes, and scales coal price data.
    Parameters:
        scaling_method (str): The scaling method to use ('minmax', 'standard', or 'robust').
    Returns:
        Processed DataFrame with scaled coal prices.
    """
    try:
        coal_price_df = clean_data_coal()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone
    coal_price_df['Date'] = pd.to_datetime(coal_price_df['Date'], utc=True)

    # Remove rows where the Date is NaT
    coal_price_df = coal_price_df[coal_price_df['Date'].notna()]

    # Set 'Date' as the index
    coal_price_df.set_index('Date', inplace=True)

    # Remove any potential duplicate indices
    coal_price_df = coal_price_df[~coal_price_df.index.duplicated(keep='first')]

    # Select the scaler based on the method
    if scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unsupported scaling method: {scaling_method}")

    # Scale 'coal_adj_close' column
    coal_price_df['coal_adj_close'] = scaler.fit_transform(coal_price_df[['coal_adj_close']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    coal_price_df = coal_price_df.resample('15T').ffill()

    return coal_price_df

def scale_gas_prices(scaling_method='minmax'):
    """
    Loads, processes, and scales gas price data.
    Returns: Processed DataFrame with scaled gas prices.
    """
    try:
        gas_price_df = clean_data_gas()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone and set as index
    gas_price_df['Date'] = pd.to_datetime(gas_price_df['Date'], utc=True)
    gas_price_df.set_index('Date', inplace=True)

    # Select the scaler based on the method
    if scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unsupported scaling method: {scaling_method}")

    # Scale 'coal_adj_close' column
    gas_price_df['ttf_adj_close'] = scaler.fit_transform(gas_price_df[['ttf_adj_close']])
    gas_price_df['ttf_volume'] = scaler.fit_transform(gas_price_df[['ttf_volume']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    gas_price_df = gas_price_df.resample('15T').ffill()

    return gas_price_df

def scale_oil_prices(scaling_method='minmax'):
    """
    Loads, processes, and scales oil price data.
    Returns: Processed DataFrame with scaled oil prices.
    """
    try:
        oil_price_df = clean_data_oil()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone and set as index
    oil_price_df['Date'] = pd.to_datetime(oil_price_df['Date'], utc=True)
    oil_price_df.set_index('Date', inplace=True)

    # Select the scaler based on the method
    if scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unsupported scaling method: {scaling_method}")

    # Scale 'coal_adj_close' column
    oil_price_df['oil_adj_close'] = scaler.fit_transform(oil_price_df[['oil_adj_close']])
    oil_price_df['oil_volume'] = scaler.fit_transform(oil_price_df[['oil_volume']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    oil_price_df = oil_price_df.resample('15T').ffill()

    return oil_price_df

def combine_dataframes(scaling_method='minmax'):
    """
    Combines coal, gas, and oil dataframes on the Date index and drops rows with any NaN values.
    Parameters:
        scaling_method (str): The scaling method to use ('minmax', 'standard', or 'robust').
    """
    scaled_coal_prices = scale_coal_prices(scaling_method)
    scaled_gas_prices = scale_gas_prices(scaling_method)
    scaled_oil_prices = scale_oil_prices(scaling_method)

    # Merge coal and gas dataframes
    combined_df = pd.merge(scaled_coal_prices, scaled_gas_prices, left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the oil dataframe
    combined_df = pd.merge(combined_df, scaled_oil_prices, left_index=True, right_index=True, how='outer')

    # Drop rows with any NaN values
    combined_df = combined_df.dropna()

    return combined_df

def scale_pmi_index():
    try:
        pmi_df = clean_data_pmi_index()
    except Exception as e:
        raise RuntimeError(f"Error loading PMI Germany data: {e}")

    pmi_df['date'] = pd.to_datetime(pmi_df['date'], utc=True)
    pmi_df.set_index('date', inplace=True)

    # Convert 'actual_pmi' to numeric, handling errors by setting them as NaN
    pmi_df['actual_pmi'] = pd.to_numeric(pmi_df['actual_pmi'], errors='coerce')

    # Drop rows with NaN values in 'actual_pmi'
    pmi_df = pmi_df.dropna(subset=['actual_pmi'])

    if pmi_df.empty:
        raise RuntimeError("After cleaning, the DataFrame is empty.")

    scaler = MinMaxScaler()

    # Scale 'actual_pmi' column
    pmi_df['actual_pmi'] = scaler.fit_transform(pmi_df[['actual_pmi']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    pmi_df = pmi_df.resample('15T').ffill()

    return pmi_df

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




# Function to merge all datasets by date
def merge_all_datasets():
    # Load and scale individual datasets
    scaled_electricity = scale_electricity_data()
    scaled_weather = scale_weather()
    scaled_holidays = scale_holidays()
    scaled_pmi = scale_pmi_index()
    combined_prices = combine_dataframes()

    # Merge datasets on the 'Date' index
    merged_data = scaled_electricity.merge(scaled_weather, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(scaled_holidays, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(scaled_pmi, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(combined_prices, how='outer', left_index=True, right_index=True)

    # # Forward-fill NaN values
    merged_data = merged_data.ffill()

    return merged_data

# Call the function to get the merged dataset
merged_dataset = merge_all_datasets()
csv_filename = 'alltogether.csv'
merged_dataset.to_csv(csv_filename, index=True)

print(f"Dataset saved to: {csv_filename}")
# # Print or use the merged dataset as needed
# print(merged_dataset)

# holidays_df = scale_holidays()
# print(holidays_df)
# pmi_df = scale_pmi_index()
# # _df = scale_pmi_index()
# print(pmi_df)
