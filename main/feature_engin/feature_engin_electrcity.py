import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Add the 'main' directory to sys.path
main_dir = os.path.dirname(os.path.dirname(__file__))  # Path to the 'main' directory
sys.path.append(main_dir)

from preproc.data import clean_data_electricity

def scale_electricity_data(scaling_method='standard'):
    """
    Load, clean, and scale electricity data using specified scaling method.

    Parameters:
        scaling_method (str): The scaling method to use ('standard', 'minmax', or 'robust').

    Returns:
        pandas.DataFrame: A DataFrame of scaled electricity data.
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

    # Select the scaler based on the method
    if scaling_method == 'standard':
        scaler = StandardScaler()
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_method == 'robust':
        scaler = RobustScaler()
    else:
        print(f"Unsupported scaling method: {scaling_method}")
        sys.exit(1)

    # Extract the target variable
    target_variable = electricity_df['day_ahead_price']

    # Drop the target variable from the DataFrame before scaling
    electricity_df = electricity_df.drop(columns=['day_ahead_price'])

    # Apply scaling to the remaining features
    electricity_scaled = scaler.fit_transform(electricity_df)
    electricity_scaled_df = pd.DataFrame(electricity_scaled, columns=electricity_df.columns, index=electricity_df.index)

    # Extracting features from the datetime index
    electricity_scaled_df = electricity_scaled_df.copy()

    # Creating a combined feature for hour and minutes as fractional hours
    #electricity_scaled_df['hour'] = electricity_scaled_df.index.hour
    electricity_scaled_df['fractional_hour'] = electricity_scaled_df.index.hour + electricity_scaled_df.index.minute / 60

    # the other datetime features
    electricity_scaled_df['day_of_week'] = electricity_scaled_df.index.dayofweek
    electricity_scaled_df['week_of_year'] = electricity_scaled_df.index.isocalendar().week
    electricity_scaled_df['month'] = electricity_scaled_df.index.month
    electricity_scaled_df['year'] = electricity_scaled_df.index.year

    # Reordering the columns to bring the new columns to the beginning
    column_order = ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year'] + [col for col in electricity_scaled_df.columns if col not in ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year']]
    electricity_scaled_df = electricity_scaled_df[column_order]

    # Reattach the target variable to the scaled DataFrame
    electricity_scaled_df['day_ahead_price'] = target_variable

    # Selecting the features to be scaled
    features_to_scale = ['fractional_hour', 'day_of_week', 'week_of_year', 'month', 'year']
    scaled_features = scaler.fit_transform(electricity_scaled_df[features_to_scale])

    # Creating a new DataFrame for the scaled features
    df_scaled = pd.DataFrame(scaled_features, columns=features_to_scale, index=electricity_scaled_df.index)

    # Merging the scaled features with the original data
    electricity_scaled_df = pd.concat([df_scaled, electricity_scaled_df.drop(columns=features_to_scale)], axis=1)

    return electricity_scaled_df
