from http import client
from read_extract import read_table 
import datetime
import json
import boto3
# import botocore.exceptions

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


        # response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=file_path, Delimiter='/')
        # if 'Contents' in response:
        #     print("YESSSSSSSSS")

        #     # Retrieve JSON file from S3
        #     json_file = s3.get_object(Bucket=BUCKET_NAME, Key='counterparty/2024/08/15/16-14-58.json')
        #     json_data = json.loads(json_file['Body'].read())
        #     # Compare data
        #     changes = deepdiff.DeepDiff(data_with_json_format, json_data)
        #     # Determine changes
        #     if changes:
        #     # Generate updated JSON
        #         updated_json_data = json_bytes  # implement logic to generate updated JSON
        #         # Upload updated JSON to S3
        #         # s3.put_object(Body=json.dumps(updated_json_data), Bucket='bucket_name', Key='file_name.json')
        #         s3.put_object(Body=updated_json_data, Bucket=BUCKET_NAME, Key=f'{db_table}/{timestamp}.json')

    
    
        

    

    
        




    # # Upload the JSON file to S3
    # s3.put_object(Body=json_bytes, Bucket='team-hyper-accelerated-dragon-bucket-ingestion', Key=f'{db_table}/{timestamp}.json')


    
  




load_table("counterparty")