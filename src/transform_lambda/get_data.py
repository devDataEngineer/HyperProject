import json
import boto3
import boto3.exceptions
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def get_data_from_ingestion_bucket(file_path: str):
   s3_client = boto3.client('s3') 
   SOURCE_BUCKET = 'team-hyper-accelerated-dragon-bucket-ingestion'
   file_key = file_path
   try :
      if file_path.startswith("s3://"):
         file_path = file_path[5:]
         SOURCE_BUCKET, file_key = file_path.split('/',1)
      logger.info(f"Reading file {file_path} from the Ingestion s3 bucket")
      file = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=file_key)
      return file['Body'].read().decode('utf-8')
   except Exception as e:
      logger.error(f"Error occured during reading the file {file_path}. More info:" + str(e))
      raise e
