import json
import pandas as pd
import boto3
import boto3.exceptions
import botocore



def get_data(file_path):

   s3_client = boto3.client('s3') 

   SOURCE_BUCKET = 'Ingestion_bucket'
   DESTINATION_BUCKET = 'Transform_bucket'
   try :
    
    file = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=file_path)
    return file
   except Exception as e:
    
        print("Ingestion bucket is empty: " + str(e))


    
    
    
    


