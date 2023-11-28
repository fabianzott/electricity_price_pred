import pandas as pd
import os

# Get the current working directory
current_directory = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Construct the paths to the CSV files in the 'raw_data' subdirectory
paths = {
    'elect': os.path.join(parent_directory, 'rawdata', 'Total_net_electricity_generation_in_Germany.csv'),
    'coal': os.path.join(parent_directory, 'rawdata', 'coal_price.csv'),
    'oil': os.path.join(parent_directory, 'rawdata', 'oil_price.csv'),
    'gas': os.path.join(parent_directory, 'rawdata', 'ttf_price.csv'),
    'weather_north_hourly': os.path.join(parent_directory, 'rawdata', 'weather_north.csv'),
    'weather_north_daily': os.path.join(parent_directory, 'rawdata', 'weather_north_daily.csv'),
    'weather_south_hourly': os.path.join(parent_directory, 'rawdata', 'weather_south.csv'),
    'weather_south_daily': os.path.join(parent_directory, 'rawdata', 'weather_south_daily.csv')
}

def get_data():
    # Initialize a dictionary to hold the dataframes
    dataframes = {}

    # Load each file into a separate dataframe
    for key, path in paths.items():
        try:
            dataframes[key] = pd.read_csv(path, sep=';', index_col=False)
            print(f"Loaded {key} successfully.")
        except FileNotFoundError:
            print(f"File not found: {path}")
    return dataframes


def clean_data(dataframes):

    cleaned_data = pd.DataFrame()

    # clean coal data
    # Access the coal price data
    coal_price_data = dataframes['coal']

    # Converting the 'Date' column to datetime format
    coal_price_data['Date'] = pd.to_datetime(coal_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close", and "Volume"
    coal_price_data.drop(['Open', 'High', 'Low', 'Close*', 'Volume'], axis=1, inplace=True)

    # Renaming the column "Adj Close**" to "coal_adj_close"
    coal_price_data.rename(columns={'Adj Close**': 'coal_adj_close'}, inplace=True)

    # Final cleaned data
    coal_price_data_cleaned = coal_price_data

    # clean LNG (TTF) data
    # Access the gas price data
    ttf_price_data = dataframes['gas']

    # Converting the 'Date' column to datetime format
    ttf_price_data['Date'] = pd.to_datetime(ttf_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close"
    ttf_price_data.drop(['Open', 'High', 'Low', 'Close*'], axis=1, inplace=True)

    # Renaming the columns "Adj Close**" to "ttf_adj_close" and "Volume" to "ttf_volume"
    ttf_price_data.rename(columns={'Adj Close**': 'ttf_adj_close', 'Volume': 'ttf_volume'}, inplace=True)

    # Final cleaned data
    ttf_price_data_cleaned = ttf_price_data

    # clean oil data
    # Access the oil price data
    coal_price_data = dataframes['oil']

    # Converting the 'Date' column to datetime format
    oil_price_data['Date'] = pd.to_datetime(oil_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close", and "Volume"
    oil_price_data.drop(['Open', 'High', 'Low', 'Close*'], axis=1, inplace=True)

    # Renaming the columns "Adj Close**" to "oil_adj_close" and "Volume" to "oil_volume"
    oil_price_data.rename(columns={'Adj Close**': 'oil_adj_close', 'Volume': 'oil_volume'}, inplace=True)

    # Final cleaned data
    oil_price_data_cleaned = oil_price_data

    return None
