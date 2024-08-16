from http import client
from read_extract import read_table 
import datetime
import json
import boto3
def load_table(db_table):
   

    try:
        s3 = boto3.client('s3')
        BUCKET_NAME = 'test-bucket-for-gz'
        FOLDER_NAME = db_table
        timestamp = datetime.datetime.now().strftime('%Y/%m/%d/%H-%M-%S')
        # file_path = f"{db_table}/2024/08/15/"
        table_data = read_table(db_table)
        data_with_json_format = json.dumps(table_data, indent=4, sort_keys=True, default=str)

        # convert json type data to json byte 
        json_bytes = json.dumps(data_with_json_format).encode('UTF-8')

        s3.put_object(Body=json_bytes, Bucket=BUCKET_NAME, Key=f'{db_table}/{timestamp}.json')
    except Exception as e:
        print(f"An error occurred: {e}")
        return False