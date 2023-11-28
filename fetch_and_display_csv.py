import os
from google.cloud import storage
import pandas as pd

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/nepomuk/code/Nepomuk11/08-Project/electricity-price-prediction-f6c44aa442b0.json"

# Initialize a client
client = storage.Client()

# Define your bucket name and object name (file name)
bucket_name = "electricity_price_pred"
blob_name = "oil_price.csv"
local_file_name = "oil_price.csv"

# Create a bucket object and download the file
bucket = client.bucket(bucket_name)
blob = bucket.blob(blob_name)
blob.download_to_filename(local_file_name)

# Read the CSV file and print the first 20 rows
df = pd.read_csv(local_file_name, delimiter=';')
print(df.head(20))
