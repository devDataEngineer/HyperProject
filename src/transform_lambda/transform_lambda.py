import json
import boto3
import boto3.exceptions
import pandas as pd
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

# # ---------[test purpose]convert json to df-------------------#
# def convert_json_to_df(jsonfile):
#    data = jsonfile['Body'].read().decode('utf-8')
#    string_io = io.StringIO(data)
#    df = pd.read_json(string_io, orient='records')
#    return df


def create_fact_sales_order_df(df_fact_slae):
   pass

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


