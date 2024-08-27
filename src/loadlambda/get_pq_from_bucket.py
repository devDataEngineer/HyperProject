import pandas as pd
import boto3
import boto3.exceptions
import logging
import pyarrow.parquet as pq
import botocore
import io


logger = logging.getLogger()
logger.setLevel("INFO")

def get_pq_from_bucket(bucket_name, key):

    s3_client = boto3.client('s3')

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        parquet_data = response['Body'].read()
        
        
        df = pd.read_parquet(io.BytesIO(parquet_data))
        return df
    
    except botocore.exceptions.ClientError as e:
        print(f"Error accessing S3: {str(e)}")
        return None

