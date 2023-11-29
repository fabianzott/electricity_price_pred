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
    'pmi_index': 'PMI_germany.csv'
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

                # Print the entire DataFrame
                #print(df)

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

                # Print the entire DataFrame
                #print(df)

            except Exception as e:
                print(f"An error occurred: {e}")

            print(f"Loaded {bucket_dict[name]} successfully.")

    except FileNotFoundError:
        print(f"File not found: {path}")

    return dataframe

#data = get_data_cloud()
#for key, value in data.items() :
#    print (key)


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

    return oil_price_data

def clean_data_electricity():

    # clean electricity data
    # Access the electricity data
    elec_data = get_data_cloud("elec")

    # Step 1: Deleting the first row and creating a copy of the DataFrame
    elec_data = elec_data.iloc[1:].copy()

    # Step 2: Converting "Date__GMT__" to datetime and sorting
    elec_data['Date__GMT__'] = pd.to_datetime(elec_data['Date__GMT__'])
    elec_data = elec_data.sort_values(by='Date__GMT__')

    # Step 3: Filling NaN values in "Nuclear" column with 0
    elec_data['Nuclear'] = elec_data['Nuclear'].fillna(0)

    # Step 4: Merging "Day_Ahead_Auction__DE_AT_LU_" and "Day_Ahead_Auction__DE_LU_"
    elec_data['Day_Ahead_Auction__DE_AT_LU_'] = elec_data['Day_Ahead_Auction__DE_AT_LU_'].fillna(elec_data['Day_Ahead_Auction__DE_LU_'])

    # Dropping the now redundant "Day_Ahead_Auction__DE_LU_" column
    elec_data = elec_data.drop(columns=['Day_Ahead_Auction__DE_LU_'])


    # Step 1: Deleting the "Fossil_coal_derived_gas" column
    elec_data.drop(columns=['Fossil_coal_derived_gas'], inplace=True)

    # Step 2: Renaming "Fossil_brown_coal___lignite" to "lignite" and filling missing values with 0
    elec_data.rename(columns={'Fossil_brown_coal___lignite': 'lignite'}, inplace=True)
    elec_data['lignite'] = elec_data['lignite'].fillna(0)

    # Step 3: Renaming and filling missing values for hydro storage columns
    elec_data.rename(columns={'Hydro_pumped_storage_consumption': 'hydro_storage_out',
                   'Hydro_pumped_storage': 'hydro_storage_in'}, inplace=True)
    elec_data['hydro_storage_out'] = elec_data['hydro_storage_out'].fillna(0)
    elec_data['hydro_storage_in'] = elec_data['hydro_storage_in'].fillna(0)

    # Step 4: Renaming "Date__GMT__" to "datetime" and deleting rows with missing values
    elec_data.rename(columns={'Date__GMT__': 'datetime'}, inplace=True)
    elec_data = elec_data.dropna(subset=['datetime'])

    # Step 5: Deleting rows where values are missing in specific columns
    columns_to_check = ['Renewable_share_of_load', 'Renewable_share_of_generation', 'Residual_load', 'Load', 'Solar']
    elec_data = elec_data.dropna(subset=columns_to_check)

    return None

print(clean_data_coal())
print(clean_data_gas())
print(clean_data_oil())
