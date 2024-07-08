import requests
import pandas as pd
import boto3
import io
import os
from botocore.exceptions import NoCredentialsError
from time import time


def download_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def upload_dataframe_to_s3(df, bucket, object_name):
    """Upload a DataFrame to an S3 bucket as a Parquet file"""
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    aws_access_key_id = os.getenv("aws-access-key-id")
    aws_secret_access_key = os.getenv("aws-secret-access-key")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    try:
        s3_client.upload_fileobj(buffer, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True


data_url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.json?accessType=DOWNLOAD"
start_time = time()
print("Downloading dataset...")
full_data = download_data(data_url)
print("Dataset downloaded. Transforming into a dataframe...")

column_dict = full_data["meta"]["view"]["columns"]
columns = [i["name"] for i in column_dict]
f_columns = [
    "County",
    "City",
    "State",
    "Model Year",
    "Make",
    "Model",
    "Electric Range",
    "Vehicle Location",
]
data = full_data["data"]

df = pd.DataFrame(data=data, columns=columns)
df = df[f_columns]
df = df.dropna()

print(f"Dataframe created with size {df.shape}. Saving to S3...")

bucket_name = "electric-vehicle-bucket"
uploaded = upload_dataframe_to_s3(df, bucket_name, "electric_vehicles.parquet")
if uploaded:
    print("File was uploaded to S3")
else:
    raise Exception("File upload failed.")

total_time = round(time() - start_time, 2)
print(f"Time taken: {total_time} seconds.")
