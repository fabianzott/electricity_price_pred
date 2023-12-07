import requests
import pandas as pd

# Define the API endpoint and parameters
url = 'https://api.energy-charts.info/public_power'
params = {
    'country': 'de',
    'start': '2023-01-01T00:00+01:00',
    'end': '2023-01-01T23:45+01:00'
}

# Make the GET request
response = requests.get(url, params=params, headers={'accept': 'application/json'})

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Create a DataFrame from the response data
    df = pd.DataFrame()

    # Add 'unix_seconds' column
    df['unix_seconds'] = data['unix_seconds']

    # Convert 'unix_seconds' to a readable date format
    df['date'] = pd.to_datetime(df['unix_seconds'], unit='s')
    # Add selected production type columns
    selected_columns = [
        'Biomass', 'Fossil brown coal / lignite', 'Fossil hard coal',
        'Fossil gas', 'Hydro pumped storage consumption', 'Residual load'
    ]

    for column in selected_columns:
        df[column] = next(item['data'] for item in data['production_types'] if item['name'] == column)

    # Rename columns
    column_mapping = {
        'Biomass': 'biomass',
        'Fossil brown coal / lignite': 'lignite',
        'Fossil hard coal': 'hard_coal',
        'Fossil gas': 'nat_gas',
        'Hydro pumped storage consumption': 'hydro_storage_in',
        'Residual load': 'residual_load'
    }

    df = df.rename(columns=column_mapping)

    # Drop the 'unix_seconds' column
    df = df.drop(columns=['unix_seconds'])
    # Save the DataFrame to a CSV file
    df.to_csv('df.csv', index=False)

    # Print the DataFrame
    print("DataFrame with selected columns:")
    print(df)

    print("DataFrame saved to df.csv")
else:
    print(f"Error: {response.status_code} - {response.text}")
