import pandas as pd
import os
from dotenv import load_dotenv
from google.cloud import storage
import pandas as pd
from io import StringIO



# Get the current working directory
current_directory = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Construct the paths to the CSV files in the 'raw_data' subdirectory

paths_dict = {
    'elect': os.path.join(parent_directory, 'rawdata', 'germany_electricity_generation_2018-2023.csv'),
    'coal': os.path.join(parent_directory, 'rawdata', 'coal_price.csv'),
    'oil': os.path.join(parent_directory, 'rawdata', 'oil_price.csv'),
    'gas': os.path.join(parent_directory, 'rawdata', 'ttf_price.csv'),
    'weather_north_hourly': os.path.join(parent_directory, 'rawdata', 'weather_north_hourly.csv'),
    'weather_north_daily': os.path.join(parent_directory, 'rawdata', 'weather_north_daily.csv'),
    'weather_south_hourly': os.path.join(parent_directory, 'rawdata', 'weather_south_hourly.csv'),
    'weather_south_daily': os.path.join(parent_directory, 'rawdata', 'weather_south_daily.csv'),
    'pmi_index': os.path.join(parent_directory, 'rawdata', 'PMI_germany.csv')
}


def get_data_local():
    # Initialize a dictionary to hold the dataframes
    dataframes = {}

    # Load each file into a separate dataframe
    for key, path in paths_dict.items():
        try:
            if "germany_electricity_generation_2018-2023.csv " in path:
                print(path)
                dataframes[key] = pd.read_csv(path, sep=',', index_col=False, low_memory=False)
                print(f"Loaded {key} successfully.")
            else:
                dataframes[key] = pd.read_csv(path, sep=';', index_col=False)
                print(f"Loaded {key} successfully.")

        except FileNotFoundError:
            print(f"File not found: {path}")

        return dataframes


# filenames in the Google cloud data bucket
bucket_dict = {
    'elect': 'germany_electricity_generation_2018-2023.csv',
    'coal': 'coal_price.csv',
    'oil': 'oil_price.csv',
    'gas': 'ttf_price.csv',
    'weather_north_hourly': 'weather_north_hourly.csv',
    'weather_north_daily': 'weather_north_daily.csv',
    'weather_south_hourly': 'weather_south_hourly.csv',
    'weather_south_daily': 'weather_south_daily.csv',
    'pmi_index': 'PMI_germany.csv',
    'weather_brocken_daily': 'weather_brocken_daily.csv',
    'weather_brocken_hourly': 'weather_brocken_hourly.csv',
    'holidays': 'holidays.csv'
}


def get_data_cloud(name):

    # Load environment variables from .env file
    load_dotenv()

    # Set the path to your Google Cloud credentials JSON file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("CREDENTIALS_PATH")

    # Initialize a client
    client = storage.Client()

    try:
        if "germany_electricity_generation_2018-2023.csv" in bucket_dict[name]:

            # Define your bucket name and object name (file name)
            bucket_name = os.environ.get("BUCKET_NAME")
            blob_name = bucket_dict[name]

            # Create a bucket object and read the file
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            try:
                # Download the blob as bytes
                blob_data = blob.download_as_bytes()

                # Convert to a file-like object
                string_data = StringIO(blob_data.decode('utf-8'))

                # Read the CSV data into a DataFrame
                dataframe = pd.read_csv(string_data, sep=',', index_col=False, low_memory=False)

            except Exception as e:
                print(f"An error occurred: {e}")

            print(f"Loaded {bucket_dict[name]} successfully.")

        else:
            # Define your bucket name and object name (file name)
            bucket_name = os.environ.get("BUCKET_NAME")
            blob_name = bucket_dict[name]

            # Create a bucket object and read the file
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            try:
                # Download the blob as bytes
                blob_data = blob.download_as_bytes()

                # Convert to a file-like object
                string_data = StringIO(blob_data.decode('utf-8'))

                # Read the CSV data into a DataFrame
                dataframe = pd.read_csv(string_data, sep=';', index_col=False)

            except Exception as e:
                print(f"An error occurred: {e}")

            print(f"Loaded {bucket_dict[name]} successfully.")

    except FileNotFoundError:
        print(f"File not found: {path}")

    return dataframe


def clean_data_coal():

    # clean coal data
    # Access the coal price data
    coal_price_data = get_data_cloud("coal")

    # Converting the 'Date' column to datetime format
    coal_price_data['Date'] = pd.to_datetime(coal_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close", and "Volume"
    coal_price_data.drop(['Open', 'High', 'Low', 'Close*', 'Volume'], axis=1, inplace=True)

    # Renaming the column "Adj Close**" to "coal_adj_close"
    coal_price_data.rename(columns={'Adj Close**': 'coal_adj_close'}, inplace=True)

    # Final cleaned data
    coal_price_data_cleaned = coal_price_data

    return coal_price_data_cleaned

def clean_data_gas():
    # clean LNG (TTF) data
    # Access the gas price data
    ttf_price_data = get_data_cloud("gas")

    # Converting the 'Date' column to datetime format
    ttf_price_data['Date'] = pd.to_datetime(ttf_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close"
    ttf_price_data.drop(['Open', 'High', 'Low', 'Close*'], axis=1, inplace=True)

    # Renaming the columns "Adj Close**" to "ttf_adj_close" and "Volume" to "ttf_volume"
    ttf_price_data.rename(columns={'Adj Close**': 'ttf_adj_close', 'Volume': 'ttf_volume'}, inplace=True)

    # Final cleaned data
    ttf_price_data_cleaned = ttf_price_data

    return ttf_price_data_cleaned

def clean_data_oil():

    # clean oil data
    # Access the oil price data
    oil_price_data = get_data_cloud("oil")

    # Converting the 'Date' column to datetime format
    oil_price_data['Date'] = pd.to_datetime(oil_price_data['Date'], errors='coerce')

    # Deleting columns "Open", "High", "Low", "Close", and "Volume"
    oil_price_data.drop(['Open', 'High', 'Low', 'Close*'], axis=1, inplace=True)

    # Renaming the columns "Adj Close**" to "oil_adj_close" and "Volume" to "oil_volume"
    oil_price_data.rename(columns={'Adj Close**': 'oil_adj_close', 'Volume': 'oil_volume'}, inplace=True)

    # Final cleaned data
    oil_price_data_cleaned = oil_price_data

    return oil_price_data_cleaned

def clean_data_electricity():

    # clean electricity data
    # Access the electricity data
    elec_data = get_data_cloud("elect")

    # Deleting row 0 and resetting the index
    elec_data = elec_data.drop(elec_data.index[0]).reset_index(drop=True)

    # Specifying the timezone handling during the datetime conversion
    elec_data['Date (GMT+1)'] = pd.to_datetime(elec_data['Date (GMT+1)'], utc=True)

    # Fill NaN values in the "Nuclear" column with 0
    elec_data['Nuclear'] = pd.to_numeric(elec_data['Nuclear'], errors='coerce').fillna(0)

    # Merging "Day Ahead Auction (DE-LU)" and "Day Ahead Auction (DE-AT-LU)" columns on NaN values
    # The idea is to fill NaN values in one column with values from the other column
    elec_data['Day Ahead Auction'] = elec_data['Day Ahead Auction (DE-LU)'].fillna(elec_data['Day Ahead Auction (DE-AT-LU)'])

    # Deleting rows with NaN values in the "Day Ahead Auction" column
    elec_data = elec_data.dropna(subset=['Day Ahead Auction'])

    # Deleting the "Day Ahead Auction (DE-LU)" and "Day Ahead Auction (DE-AT-LU)" columns
    elec_data = elec_data.drop(columns=['Day Ahead Auction (DE-LU)', 'Day Ahead Auction (DE-AT-LU)'])

    # Fill NaN values in "Hydro pumped storage consumption" with 0
    elec_data['Hydro pumped storage consumption'] = elec_data['Hydro pumped storage consumption'].fillna(0)

    # Delete rows with NaN values in "Fossil brown coal / lignite"
    elec_data = elec_data.dropna(subset=['Fossil brown coal / lignite'])

    # Fill NaN values in "Fossil coal-derived gas" with 0
    elec_data['Fossil coal-derived gas'] = elec_data['Fossil coal-derived gas'].fillna(0)

    # Fill NaN values in "Hydro pumped storage" with 0
    elec_data['Hydro pumped storage'] = elec_data['Hydro pumped storage'].fillna(0)

    # Delete rows with missing values for "Load", "Residual load", and "Renewable share of load"
    elec_data = elec_data.dropna(subset=['Load', 'Residual load', 'Renewable share of load'])

    # Renaming columns as specified
    column_rename_map = {
        "Date (GMT+1)": "date_gmt+1",
        "Hydro pumped storage consumption": "hydro_storage_in",
        "Cross border electricity trading": "cross_border",
        "Nuclear": "nuclear",
        "Hydro Run-of-River": "hydro",
        "Biomass": "biomass",
        "Fossil brown coal / lignite": "lignite",
        "Fossil hard coal": "hard_coal",
        "Fossil oil": "oil",
        "Fossil coal-derived gas": "coal_gas",
        "Fossil gas": "nat_gas",
        "Geothermal": "geothermal",
        "Hydro water reservoir": "hydro_reservoir",
        "Hydro pumped storage": "hydro_storage_out",
        "Others": "others",
        "Waste": "waste",
        "Wind offshore": "wind_offshore",
        "Wind onshore": "wind_onshore",
        "Solar": "solar",
        "Load": "load",
        "Residual load": "residual_load",
        "Renewable share of generation": "renewable_share_gen",
        "Renewable share of load": "renewable_share_load",
        "Day Ahead Auction": "day_ahead_price"
    }

    elec_data = elec_data.rename(columns=column_rename_map)

    # Deleting the "Year" column
    #elec_data = elec_data.drop(columns=["Year"])

    # Final cleaned data
    elec_data_cleaned = elec_data

    return elec_data_cleaned


def clean_data_pmi_index():
    # clean electricity data
    # Access the electricity data
    pmi_data = get_data_cloud("pmi_index")

    return None


def clean_data_weather():
    # clean weather data
    # Access the electricity data


    return None



#print(clean_data_electricity())
#print(clean_data_electricity().info())
