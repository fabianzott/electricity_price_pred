import sys
import os
import pandas as pd

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from feature_engin.feature_engin_pmi import scale_pmi_index
from feature_engin.feature_engin_commodity import combine_dataframes
from feature_engin.feature_engin_electrcity import scale_electricity_data
from feature_engin.feature_engin_holidays import scale_holidays
from feature_engin.feature_engin_weather import scale_weather


# Function to merge all datasets by date
def merge_all_datasets():
    # Load and scale individual datasets
    scaled_electricity = scale_electricity_data()
    scaled_weather = scale_weather()
    scaled_holidays = scale_holidays()
    scaled_pmi = scale_pmi_index()
    combined_comodity = combine_dataframes()

    # Merge datasets on the 'Date' index
    merged_data = scaled_electricity.merge(scaled_weather, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(scaled_holidays, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(scaled_pmi, how='outer', left_index=True, right_index=True)
    merged_data = merged_data.merge(combined_comodity, how='outer', left_index=True, right_index=True)

    # # Forward-fill NaN values
    merged_data = merged_data.ffill()

    # Count the number of rows
    num_rows = len(merged_data)

    # Print the number of rows
    print(f"The DataFrame has {num_rows} rows before deleting NaN rows.")

    merged_data = merged_data.dropna()

    # Count the number of rows
    num_rows_no_nan = len(merged_data)

    # Print the number of rows
    print(f"The DataFrame has {num_rows_no_nan} rows AFTER deleting NaN rows.")

    return merged_data

#----------------------------------------------------------------
# UNCOMENT IF  DATSETS ARE CHANGED

# Call the function to get the merged dataset
#merged_dataset = merge_all_datasets()
#print(merged_dataset.info())
#print(merged_dataset.head())
#csv_filename = 'fianal_ML_data.csv'
#merged_dataset.to_csv(csv_filename, index=True)

# print(f"Dataset saved to: {csv_filename}")
# # Print or use the merged dataset as needed
# print(merged_dataset)

# holidays_df = scale_holidays()
# print(holidays_df)
# pmi_df = scale_pmi_index()
# # _df = scale_pmi_index()
# print(pmi_df)
