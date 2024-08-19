from connection import close_db_connection, db_connection
from utilities import format_extract_lambda_as_rows
from time_param_funcs import upload_time_to_param, get_date_from_param
from pg8000 import DatabaseError
from datetime import datetime
import logging

import os
import boto3
import json

logger = logging.getLogger()
logger.setLevel("INFO")

date_to_compare = get_date_from_param()

def load_table(table_name, table_data):
    logger.info(f"packing table {table_name} into {table_name}/{timestamp}.json")
    try:
        s3 = boto3.client('s3')
        BUCKET_NAME = 'team-hyper-accelerated-dragon-bucket-ingestion'
        timestamp = date_to_compare.strftime('%Y/%m/%d/%H-%M-%S')
        data_with_json_format = json.dumps(table_data, indent=4, sort_keys=True, default=str)
        json_bytes = json.dumps(data_with_json_format).encode('UTF-8')

        s3.put_object(Body=json_bytes, Bucket=BUCKET_NAME, Key=f'{table_name}/{timestamp}.json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def read_table(db_table):
    global date_to_compare
    logger.info(f"reading table {db_table}")
    table_whitelist = ['counterparty', 'currency', 'department', 'design', 
                       'staff', 'sales_order', 'address', 'payment', 
                       'purchase_order', 'payment_type', 'transaction']
    
    if db_table not in table_whitelist:
        raise ValueError(f"Invalid table name: {db_table}")
    
    try:
        conn = db_connection()
        current_date_time=datetime.now()
        query = f"""SELECT * FROM {db_table}
                    WHERE last_updated BETWEEN :date_to_compare AND :current_date_time;"""
        
        rows = conn.run(query, date_to_compare=date_to_compare, current_date_time=current_date_time)
        column_list = [conn.columns[i]['name'] for i in range(len(conn.columns))]
        formatted = format_extract_lambda_as_rows(rows,column_list)
        upload_time_to_param(current_date_time)
        return formatted, current_date_time
    
    except DatabaseError as e:
        logger.info(f"got an error when reading table {db_table}")
        raise e
    
    finally:
        close_db_connection(conn)


def load_all_tables():
    logger.info("loading all tables...")
    table_list = ['counterparty', 'currency', 'department', 'design', 
                       'staff', 'sales_order', 'address', 'payment', 
                       'purchase_order', 'payment_type', 'transaction']
    for table in table_list:
        load_table(table, read_table(table)[0])

def lambda_handler(event, context):   
   logger.info(f"running extract lambda_handler at {datetime.now()}")
   logger.info(f"date_to_compare is {date_to_compare}")

   try:
      load_all_tables()
    
   except:
      topic_arn = os.environ.get('TOPIC_ARN')
      client = boto3.client('sns')  
      client.publish(TopicArn=topic_arn,Message="Error has occured")



