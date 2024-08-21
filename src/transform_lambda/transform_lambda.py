import json
import boto3
import boto3.exceptions
import pandas as pd
import io

def get_data(file_path):

   s3_client = boto3.client('s3') 
   objject_lsit = []
   SOURCE_BUCKET = 'Ingestion_bucket'
   DESTINATION_BUCKET = 'Transform_bucket'
   try :
    
    file = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=file_path)
    return file
   except Exception as e:
        print("Ingestion bucket is empty: " + str(e))

# ---------[test purpose]convert json to df-------------------#
def convert_json_to_df(jsonfile):
   data = jsonfile['Body'].read().decode('utf-8')
   string_io = io.StringIO(data)
   df = pd.read_json(string_io, orient='records')
   return df


def create_fact_sales_order_df(df_fact_slae):
   pass

#----------formate dim_currency data frame----------------------#
def create_df_dim_currency(df_currency):
   dim_currency = df_currency.drop(columns=['created_at','last_update'])
   return dim_currency
