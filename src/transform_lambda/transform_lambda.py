import json
import boto3
from botocore.exceptions import ClientError

def get_data(file_path):

   s3_client = boto3.client('s3') 

   SOURCE_BUCKET = 'Ingestion_bucket'
   DESTINATION_BUCKET = 'Transform_bucket'
   try :
    
    file = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=file_path)
    return file
   except ClientError as e:
        print("Ingestion bucket is empty: " + str(e))


    
    
    
    


