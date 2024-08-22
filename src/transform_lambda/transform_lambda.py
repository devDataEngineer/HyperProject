import json
import boto3
import boto3.exceptions
import pandas as pd
import numpy as np

import pyspark.sql.functions as F
import io

def get_data(file_path: str):
   s3_client = boto3.client('s3') 
   SOURCE_BUCKET = 'Ingestion_bucket'
   file_key = file_path
   try :
      if file_path.startswith("S3://"):
         file_path = file_path[5:]
         SOURCE_BUCKET, file_key = file_path.split('/',1)
      file = s3_client.get_object(Bucket=SOURCE_BUCKET, Key=file_key)
      return file
   except Exception as e:
        print("File path is wrong: " + str(e))
        raise e


#----------formate dim_currency data frame----------------------#
def create_df_dim_currency(df_currency):
   dim_currency = df_currency
   currency_names = {
            'GBP': 'British Pound',
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'CHF': 'Swiss Franc'
        }
   dim_currency['currency_name'] = dim_currency['currency_code'].apply(lambda x: currency_names[x])
   dim_currency = dim_currency.drop(columns = ['created_at','last_update'])
   dim_currency.set_index= dim_currency['currency_id']
   dim_currency.name = "dim_currency"
   return dim_currency

#----------formate dim_date_df data frame----------------------#
def create_df_dim_date(df_date):
   dim_date = df_date
   dim_date['year'] = pd.DatetimeIndex(dim_date['created_date']).year
   dim_date['month'] = pd.DatetimeIndex(dim_date['created_date']).month
   dim_date['day'] = pd.DatetimeIndex(dim_date['created_date']).day
   dim_date['day_of_week'] = pd.DatetimeIndex(dim_date['created_date']).day_of_week
   dim_date['day_name'] = dim_date['created_date'].dt.day_name()
   dim_date['month_name'] = dim_date['created_date'].dt.month_name()
   dim_date['quarter'] = pd.DatetimeIndex(dim_date['created_date']).quarter
   dim_date = dim_date.rename(columns = {'created_date': "date_id"})
   dim_date.set_index = dim_date['date_id']
   dim_date.name = 'dim_date'
   return dim_date



#sales_record_id [SERIAL], created_date
#----------formate dim_date_df data frame----------------------#
def create_df_fact_sales_order(df_sales_order):
   fact_sales_order = df_sales_order
   fact_sales_order.name = 'fact_sales_order'
   fact_sales_order['created_at'] = pd.to_datetime(fact_sales_order['created_at'])
   fact_sales_order['created_date'] = fact_sales_order['created_at'].dt.date
   fact_sales_order['created_time'] = fact_sales_order['created_at'].dt.time
   fact_sales_order['last_updated'] = pd.to_datetime(fact_sales_order['last_updated'])
   fact_sales_order['last_updated_date'] = fact_sales_order['last_updated'].dt.date     
   fact_sales_order['last_updated_time'] = fact_sales_order['last_updated'].dt.time
   fact_sales_order = fact_sales_order.drop(columns=[ 'created_at', 'last_updated'])
   fact_sales_order = fact_sales_order.rename(columns={"staff_id": "sales_staff_id"})
   fact_sales_order['sales_record_id'] = 1
   start_value = 1
   stop_value = len(fact_sales_order) + 1  # adjust this based on your DataFrame size
   step = 1
   fact_sales_order['sales_record_id'] = np.arange(start_value, stop_value, step)

   fact_sales_order.set_index = fact_sales_order['sales_record_id']
   fact_sales_order = fact_sales_order.reindex(columns=['sales_record_id', 'sales_order_id', 'created_date', 'created_time', 'last_updated_date', 'last_updated_time', 
                                                        'sales_staff_id', 'counterparty_id', 'units_sold', 'unit_price', 'currency_id', 'design_id', 
                                                        'agreed_payment_date', 'agreed_delivery_date', 'agreed_delivery_location_id'])
   return fact_sales_order





