import pandas as pd
import os

# Get the current working directory
current_directory = os.getcwd()

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Construct the path to the 'data.csv' file in the 'raw_data' subdirectory
data_file_path = os.path.join(parent_directory, 'raw_data', 'data.csv')

# Now you can use data_file_path to open and read the file
try:
    with open(data_file_path, 'r') as file:
        data = file.read()
        # Process the data
        print(data)
except FileNotFoundError:
    print(f"File not found: {data_file_path}")


########################################################
# Loading the files into Pandas DataFrames

dataframes = [pd.read_csv(file) for file in "/raw]

# Merging the dataframes
# Assuming that the dataframes have a similar structure and can be concatenated one after the other

merged_df = pd.concat(dataframes, ignore_index=True)

#####################################################
# Data curation involves several steps:
# 1. Removing rows with non-numerical data (like headers or units included in the data)
# 2. Ensuring data types are correct for each column
# 3. Handling missing or null values

# Step 1: Removing rows with non-numerical data
# We assume that rows with NaN in 'Date (GMT+1)' are non-numerical rows
curated_df = merged_df[merged_df['Date (GMT+1)'].notna()]

# Step 2: Ensuring data types are correct
# Converting 'Date (GMT+1)' to datetime and other columns to numeric types
curated_df['Date (GMT+1)'] = pd.to_datetime(curated_df['Date (GMT+1)'])
for col in curated_df.columns:
    if col != 'Date (GMT+1)':
        curated_df[col] = pd.to_numeric(curated_df[col], errors='coerce')

# Step 3: Handling missing or null values
# Checking for missing values
missing_values = curated_df.isnull().sum()

# Displaying a summary of missing values and the first few rows of the curated dataframe
missing_values_summary = missing_values.to_dict(), curated_df.head()
missing_values_summary


########################################################
# Filling the NaN values in the "Nuclear" column with 0
merged_df['Nuclear'].fillna(0, inplace=True)

# Verifying if there are any NaN values left in the "Nuclear" column
remaining_nan_in_nuclear = merged_df['Nuclear'].isna().sum()
remaining_nan_in_nuclear
