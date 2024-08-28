import pandas as pd
import boto3
import logging
# import pyarrow.parquet as pq
from botocore.exceptions import ClientError
import io


logger = logging.getLogger()
logger.setLevel("INFO")

def get_pq_from_bucket(key):

    s3_client = boto3.client('s3')
    SOURCE_BUCKET = 'team-hyper-accelerated-dragon-bucket-processed'

    try:
        logger.info(f"Reading {key} parquet file from the Processed S3 bucket")
        response = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=key)
        parquet_data = response['Body'].read()
        
        df = pd.read_parquet(io.BytesIO(parquet_data))
        return df
    
    except ClientError as e:
        logger.error(f"Error accessing S3 Processed bucket: {str(e)}")
        raise

