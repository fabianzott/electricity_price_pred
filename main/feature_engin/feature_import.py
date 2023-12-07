import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from preproc.data import clean_data_coal, clean_data_gas, clean_data_oil
from preproc.data import clean_data_electricity
from preproc.data import clean_data_holidays
from preproc.data import clean_data_pmi_index
from preproc.data import clean_data_weather

def proc_coal_prices():
    """
    Loads and processes coal price data.

    Returns:
        Processed DataFrame with coal prices.
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

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    coal_price_df = coal_price_df.resample('15T').ffill()

    return coal_price_df


def proc_gas_prices():
    """
    Loads and processes gas price data.
    Returns: Processed DataFrame with gas prices.
    """
    try:
        gas_price_df = clean_data_gas()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone and set as index
    gas_price_df['Date'] = pd.to_datetime(gas_price_df['Date'], utc=True)
    gas_price_df.set_index('Date', inplace=True)

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    gas_price_df = gas_price_df.resample('15T').ffill()

    return gas_price_df


def proc_oil_prices(scaling_method='minmax'):
    """
    Loads and processes oil price data.
    Returns: Processed DataFrame with oil prices.
    """
    try:
        oil_price_df = clean_data_oil()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone and set as index
    oil_price_df['Date'] = pd.to_datetime(oil_price_df['Date'], utc=True)
    oil_price_df.set_index('Date', inplace=True)

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    oil_price_df = oil_price_df.resample('15T').ffill()

    return oil_price_df


def preproc_electricity_data():
    """
    Load, clean electricity data and preproc method.

    Returns:
        pandas.DataFrame: A DataFrame of electricity data.
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



    # Extract the target variable
    #target_variable = electricity_df['day_ahead_price']

    # Drop the target variable from the DataFrame before scaling
    #electricity_df = electricity_df.drop(columns=['day_ahead_price'])

    # Apply scaling to the remaining features
    #electricity_scaled = scaler.fit_transform(electricity_df)
    #electricity_df = pd.DataFrame(electricity_scaled, columns=electricity_df.columns, index=electricity_df.index)

    # Extracting features from the datetime index
    electricity_df = electricity_df.copy()

    # Creating a combined feature for hour and minutes as fractional hours
    #electricity_df['hour'] = electricity_df.index.hour
    electricity_df['fractional_hour'] = electricity_df.index.hour + electricity_df.index.minute / 60

    # the other datetime features
    electricity_df['day_of_week'] = electricity_df.index.dayofweek
    electricity_df['week_of_year'] = electricity_df.index.isocalendar().week
    electricity_df['month'] = electricity_df.index.month
    electricity_df['year'] = electricity_df.index.year

    # Reordering the columns to bring the new columns to the beginning
    column_order = ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year'] + [col for col in electricity_df.columns if col not in ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year']]
    electricity_df = electricity_df[column_order]

    # Reattach the target variable to the scaled DataFrame
    #electricity_df['day_ahead_price'] = target_variable

    # Selecting the features to be scaled
    #features_to_scale = ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year']
    #scaled_features = scaler.fit_transform(electricity_df[features_to_scale])

    # Creating a new DataFrame for the scaled features
    #df_scaled = pd.DataFrame(scaled_features, columns=features_to_scale, index=electricity_df.index)

    # Merging the scaled features with the original data
    #electricity_df = pd.concat([df_scaled, electricity_df.drop(columns=features_to_scale)], axis=1)

    return electricity_df


def preproc_holiday():
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

    # Convert 'holiday' column to numeric
    holidays_df['holiday'] = pd.to_numeric(holidays_df['holiday'], errors='coerce')

    # Set 'date' as index for subsequent operations
    holidays_df.set_index('date', inplace=True)

    # Handle duplicates during resampling
    holidays_df = holidays_df[~holidays_df.index.duplicated(keep='first')]
    holidays_df = holidays_df.resample('15T').ffill()

    return holidays_df



from preproc.data import clean_data_pmi_index

def preproc_pmi_data():
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

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    pmi_df = pmi_df.resample('15T').ffill()

    return pmi_df



def preproc_weather():
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

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    weather_df = weather_df.resample('15T').ffill()

    return weather_df


def combine_dataframes():
    """
    Combines coal, gas, and oil dataframes on the Date index and drops rows with any NaN values.

    """
    scaled_coal_prices = proc_coal_prices()
    scaled_gas_prices = proc_gas_prices()
    scaled_oil_prices = proc_oil_prices()
    electricit_data = preproc_electricity_data()
    holiday_data = preproc_holiday()
    pmi_data = preproc_pmi_data()
    weather_data = preproc_weather()

    # Merge coal and gas dataframes
    combined_df = pd.merge(scaled_coal_prices, scaled_gas_prices, left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the oil dataframe
    combined_df = pd.merge(combined_df, scaled_oil_prices, left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the electricity generation dataframe
    combined_df = pd.merge(combined_df, electricit_data, left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the holiday dataframe
    combined_df = pd.merge(combined_df, holiday_data, left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the pmi dataframe
    combined_df = pd.merge(combined_df, pmi_data , left_index=True, right_index=True, how='outer')

    # Merge the combined dataframe with the weather dataframe
    combined_df = pd.merge(combined_df, weather_data , left_index=True, right_index=True, how='outer')

    # Drop rows with any NaN values
    combined_df = combined_df.dropna()

    # covert all to float64
    combined_df = combined_df.astype('float64')

    return combined_df

#df = combine_dataframes()

# test
#print(df.info())
