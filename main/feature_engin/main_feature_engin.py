import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from feature_engin_electrcity import scale_electricity_data
from feature_engin_commodity import combine_dataframes
from feature_engin_pmi import scale_pmi_index
from feature_engin_holidays import scale_holidays
from feature_engin_weather import scale_weather

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

#   ----------------------------------------------------------------
# UNCOMENT IF  DATSETS ARE CHANGED

# Call the function to get the merged dataset
merged_dataset = merge_all_datasets()
csv_filename = 'alltogether.csv'
merged_dataset.to_csv(csv_filename, index=True)
df= pd.read_csv(csv_filename)


csv_filename_new = "cleaned.csv"
if df.isna().any().any():
    print("Dataset contains NaN values. Deleting rows with NaN values.")

    # Drop rows with any NaN values
    df = df.dropna()
    df_new = df.rename(columns={'Unnamed: 0': 'date'})

    # Save the cleaned dataset back to the CSV file
    df_new.to_csv(csv_filename_new, index=False)

    print(f"Cleaned dataset saved to: {csv_filename_new}")
else:
    print("Dataset does not contain NaN values.")


# print(f"Dataset saved to: {csv_filename}")
# # Print or use the merged dataset as needed
# print(merged_dataset)
