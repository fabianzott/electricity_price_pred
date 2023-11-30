from data import clean_data_coal, clean_data_gas, clean_data_oil
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def scale_coal_prices():
    """
    Loads, processes, and scales coal price data.
    Returns: Processed DataFrame with scaled coal prices.
    """
    try:
        coal_price_df = clean_data_coal()
    except Exception as e:
        raise RuntimeError(f"Error loading coal data: {e}")

    # Convert 'Date' to datetime with UTC timezone and set as index
    coal_price_df['Date'] = pd.to_datetime(coal_price_df['Date'], utc=True)
    coal_price_df.set_index('Date', inplace=True)

    scaler = MinMaxScaler()

    # Scale 'coal_adj_close' column
    coal_price_df['coal_adj_close'] = scaler.fit_transform(coal_price_df[['coal_adj_close']])

    return coal_price_df

def scale_gas_prices():
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

    scaler = MinMaxScaler()

    # Scale 'coal_adj_close' column
    gas_price_df['gas_adj_close'] = scaler.fit_transform(gas_price_df[['gas_adj_close']])

    return gas_price_df


def scale_oil_prices():
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

    scaler = MinMaxScaler()

    # Scale 'coal_adj_close' column
    oil_price_df['oil_adj_close'] = scaler.fit_transform(oil_price_df[['oil_adj_close']])

    return oil_price_df


scaled_coal_prices = scale_coal_prices()
scaled_gas_prices = scale_gas_prices()
scaled_oil_prices = scale_oil_prices()

print(scaled_coal_prices.head())
print(scaled_gas_prices.head())
print(scaled_oil_prices.head())
