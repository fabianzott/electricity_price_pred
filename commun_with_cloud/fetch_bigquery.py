import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Set the path to your Google Cloud credentials JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("CREDENTIALS_PATH")

# Initialize a BigQuery client
client = bigquery.Client()

# Get the dataset name from the environment variables
bq_dataset = os.environ.get("BQ_DATASET")

# Construct a SQL query
query = f"""
SELECT *
FROM `{bq_dataset}.oil_price`
LIMIT 20
"""

# Run the query and get a pandas DataFrame
df = client.query(query).to_dataframe()

# Print the DataFrame
print(df)
