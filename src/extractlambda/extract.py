try:
    from connection import close_db_connection, db_connection
    from utilities import format_extract_lambda_as_rows
    from time_param_funcs import update_time_param
except:
    from src.extractlambda.connection import close_db_connection, db_connection
    from src.extractlambda.utilities import format_extract_lambda_as_rows
    from src.extractlambda.time_param_funcs import update_time_param
from botocore.exceptions import ClientError
from pg8000 import DatabaseError

from datetime import datetime
import logging

import os
import boto3
import json

logger = logging.getLogger()
logger.setLevel("INFO")


def read_table(
        table_name: str,
        current_time: datetime,
        previous_time: datetime
        ) -> str | None:
    """DOCSTRING GOES HERE"""

    logger.info(f"Reading table {table_name}")

    table_whitelist = [
        'counterparty', 'currency', 'department',
        'design', 'staff', 'sales_order',
        'address', 'payment', 'purchase_order',
        'payment_type', 'transaction'
        ]
    
    if table_name not in table_whitelist:
        raise ValueError(f"Invalid table name: {table_name}")
    
    try:
        conn = db_connection()
        query = f"""SELECT * FROM {table_name}
                    WHERE last_updated BETWEEN :previous_time AND :current_time;"""
        
        rows = conn.run(query, current_time = current_time, previous_time = previous_time)
        column_list = [conn.columns[i]['name'] for i in range(len(conn.columns))]
        formatted = format_extract_lambda_as_rows(rows, column_list)
        close_db_connection(conn)
        return formatted
    
    except DatabaseError as e:
        logger.info(f"got an error when reading table {table_name}")
        raise e

def get_filename(table_name, current_time: datetime) -> str:
    return f"{table_name}/{current_time.strftime('%Y/%m/%d/%H-%M-%S')}.json"

def load_table(
        table_name: str,
        table_data: str,
        current_time: datetime
        ) -> None:
    """DOCSTRING GOES HERE"""

    try:
        s3 = boto3.client('s3')
        BUCKET_NAME = 'team-hyper-accelerated-dragon-bucket-ingestion'
        timestamp = current_time.strftime('%Y/%m/%d/%H-%M-%S')

        logger.info(
            f"Packing table {table_name} into {table_name}/{timestamp}.json"
            )
        json_bytes = json.dumps(
            table_data,
            indent=4,
            sort_keys=True,
            default=str
            ).encode('UTF-8')

        logger.info(f"Loading table {table_name} into ingestion bucket")
        s3.put_object(
            Body=json_bytes,
            Bucket=BUCKET_NAME,
            Key=f'{table_name}/{timestamp}.json'
            )
        
    except Exception as e:
        print(f"An error occurred: {e}")


def load_all_tables(
        current_time: datetime,
        previous_time: datetime
        ) -> dict:
    """DOCSTRING GOES HERE"""

    tables_modified = {}
    try:
        logger.info("Attempting to load all tables")
        table_list = [
            'counterparty', 'currency', 'department', 'design',
            'staff', 'sales_order', 'address', 'payment',
            'purchase_order', 'payment_type', 'transaction'
            ]
        for table in table_list:
            logger.info(f"Reading table {table}")
            table_data = read_table(
                table_name = table,
                current_time = current_time,
                previous_time = previous_time
                )
            if (len(table_data) > 0):
                logger.info(f"Table {table} has updated contents")
                tables_modified[table] = get_filename(
                    table_name = table,
                    current_time = current_time
                    )
                load_table(
                    table_name = table,
                    table_data = table_data,
                    current_time = current_time
                    )

    except ClientError as e:
        
        logger.error("Extract lambda failed to pull from DB and load the data to s3 bucket")
        topic_arn = os.environ.get('TOPIC_ARN')
        client = boto3.client('sns')  
        client.publish(
            TopicArn = topic_arn,
            Message = f"""Error Summary:
                Function Name: Extract Lambda
                Region: eu-west-2
                Error Message: Extract lambda failed to pull from DB and load the data to s3 bucket
                Detailed Logs: {str(e)}
                Next Steps:
                Please investigate this issue as a priority. You can start by reviewing the CloudWatch logs linked above. Additionally, ensure that any upstream or downstream services that rely on this Lambda function are not impacted by this error.
                Support:
                If you need further assistance, please feel free to reach out to the AWS DevOps team or consult the AWS documentation here"""
                            )

    finally:
        return tables_modified
    

def lambda_handler(event, context) -> dict:
    """DOCSTRING GOES HERE
    output = {
        "table_name_1": "filepath_1",
        "table_name_2": "filepath_2"
        }
    key value pair for each table that has new entries
    key as table name
    value as path to file in s3 bucket
    """

    current_time, previous_time = update_time_param()

    logger.info(f"Running extract lambda_handler!")
    logger.info(f"current_time = {current_time}")
    logger.info(f"previous_time = {previous_time}")

    tables_modified = load_all_tables(current_time, previous_time)
    return tables_modified


