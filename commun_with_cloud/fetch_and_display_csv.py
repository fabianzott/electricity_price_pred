import os
from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from .env file

GCP_PROJECT = os.environ.get("GCP_PROJECT")
print(GCP_PROJECT)

"""from google.cloud import storage
import pandas as pd
import gzip
from io import StringIO

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/nepomuk/code/Nepomuk11/08-Project/electricity-price-prediction-f6c44aa442b0.json"

# Initialize a client
client = storage.Client()

# Define your bucket name and object name (file name)
bucket_name = "electricity_price_pred"
blob_name = "oil_price.csv.gz"

# Create a bucket object and read the file as a string
bucket = client.bucket(bucket_name)
blob = bucket.blob(blob_name)
compressed_data = blob.download_as_bytes()

# Decompress the data and convert to a file-like object
decompressed_data = gzip.decompress(compressed_data)
string_data = StringIO(decompressed_data.decode('utf-8'))

# Read the CSV data and print the first 20 rows
df = pd.read_csv(string_data, delimiter=';')
print(df.head(20))"""
