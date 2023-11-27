import pandas as pd


# Loading the files into Pandas DataFrames

dataframes = [pd.read_csv(file) for file in file_paths]

# Merging the dataframes
# Assuming that the dataframes have a similar structure and can be concatenated one after the other

merged_df = pd.concat(dataframes, ignore_index=True)


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
