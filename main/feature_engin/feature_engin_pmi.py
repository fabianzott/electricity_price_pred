import sys
import os

# Get the current working directory
current_dir = os.getcwd()

# Assuming your notebook is in the 'feature_engin' directory,
# and you want to add 'main' to the path
main_dir = os.path.dirname(current_dir)
sys.path.append(main_dir)

from preproc.data import clean_data_coal, clean_data_gas, clean_data_oil
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from preproc.data import clean_data_pmi_index

def scale_pmi_index():
    try:
        pmi_df = clean_data_pmi_index()
    except Exception as e:
        raise RuntimeError(f"Error loading PMI Germany data: {e}")

    pmi_df['date'] = pd.to_datetime(pmi_df['date'], utc=True)
    pmi_df.set_index('date', inplace=True)

    # Convert 'actual_pmi' to numeric, handling errors by setting them as NaN
    pmi_df['actual_pmi'] = pd.to_numeric(pmi_df['actual_pmi'], errors='coerce')

    # Drop rows with NaN values in 'actual_pmi'
    pmi_df = pmi_df.dropna(subset=['actual_pmi'])

    if pmi_df.empty:
        raise RuntimeError("After cleaning, the DataFrame is empty.")

    scaler = MinMaxScaler()

    # Scale 'actual_pmi' column
    pmi_df['actual_pmi'] = scaler.fit_transform(pmi_df[['actual_pmi']])

    # Resample the DataFrame to 15-minute intervals, forward-filling the data
    pmi_df = pmi_df.resample('15T').ffill()

    return pmi_df
