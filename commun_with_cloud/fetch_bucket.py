import os
from dotenv import load_dotenv
from google.cloud import storage
import pandas as pd
from io import StringIO

#Hello
# Load environment variables from .env file
load_dotenv()

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("CREDENTIALS_PATH")

# Initialize a client
client = storage.Client()

# Define your bucket name and object name (file name)
bucket_name = os.environ.get("BUCKET_NAME")
blob_name = "weather_south.csv"

# Create a bucket object and read the file
bucket = client.bucket(bucket_name)
blob = bucket.blob(blob_name)

try:
    # Download the blob as bytes
    blob_data = blob.download_as_bytes()

    # Convert to a file-like object
    string_data = StringIO(blob_data.decode('utf-8'))

    # Read the CSV data into a DataFrame
    df = pd.read_csv(string_data, delimiter=';')

    # Print the entire DataFrame
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")
