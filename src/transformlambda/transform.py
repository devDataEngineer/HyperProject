try:
    from src.transformlambda.create_df_fact_sales_order import create_df_fact_sales_order
    from src.transformlambda.create_df_dim_staff import create_df_dim_staff
    from src.transformlambda.create_df_dim_date import create_df_dim_date
    from src.transformlambda.create_df_dim_currency import create_df_dim_currency
    from src.transformlambda.create_df_dim_location import create_dim_location
    from src.transformlambda.create_df_dim_design import create_df_dim_design
    from src.transformlambda.get_arguments import get_arguments
    from src.transformlambda.get_data import get_data_from_ingestion_bucket
    from src.transformlambda.json_to_panda_func import json_to_panda_df
    from src.transformlambda.convert_df_to_pq_bytes import convert_dataframe_to_parquet_bytes
    from src.transformlambda.upload_to_processed_bucket import upload_to_processed_bucket
    from src.transformlambda.create_df_dim_counterparty import create_df_dim_counterparty
except:
    from create_df_fact_sales_order import create_df_fact_sales_order
    from create_df_dim_staff import create_df_dim_staff
    from create_df_dim_date import create_df_dim_date
    from create_df_dim_currency import create_df_dim_currency
    from create_df_dim_location import create_dim_location
    from create_df_dim_design import create_df_dim_design
    from create_df_dim_counterparty import create_df_dim_counterparty
    from get_arguments import get_arguments
    from get_data import get_data_from_ingestion_bucket
    from json_to_panda_func import json_to_panda_df
    from convert_df_to_pq_bytes import convert_dataframe_to_parquet_bytes
    from upload_to_processed_bucket import upload_to_processed_bucket

import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def get_time():
    client = boto3.client('ssm')
    try:
        response = client.get_parameter(Name = 'dragons_time_param')
        return datetime.strptime(
            response['Parameter']['Value'],
            '%Y-%m-%d %H:%M:%S.%f'
            )
    
    except ClientError as e:
        logger.error(f"An error occurred: {e}")
        raise

def get_filename(table_name, current_time: datetime) -> str:
    return f"{table_name}/{current_time.strftime('%Y/%m/%d/%H-%M-%S')}.json"

def lambda_handler(event, context) -> None:
    """TRANSFORM"""

    current_time = get_time()
    timestamp = current_time.strftime('%Y/%m/%d/%H-%M-%S')

    logger.info("Transform Lambda beggining execution")

    logger.info("Retrieving arguments from previous Extract Lambda")
    tables_with_filepaths = get_arguments(event)
    tables_with_json_data = {}

    table_list = list(tables_with_filepaths.keys())
    logger.info(f"Tables to update: {table_list}")

    logger.info("Retrieving json files from Extract S3 Bucket")
    for table in table_list:
        logger.info(f"Retrieving {tables_with_filepaths[table]}...")
        tables_with_json_data[table] = get_data_from_ingestion_bucket(
            tables_with_filepaths[table]
            )
        logger.info(f"{table} file retrieved")

    tables_with_dataframes = {}

    logger.info(f"Converting tables from json to dataframe")
    for table in table_list:
        tables_with_dataframes[table] = json_to_panda_df(
            tables_with_json_data[table]
            )
        logger.info(f"Table [{table}] converted")

    processed_dataframes = {}
    processed_dataframe_list = []

    if "sales_order" in table_list:
        logger.info("Creating df_fact_sales_order")
        df_fact_sales_order = create_df_fact_sales_order(
            tables_with_dataframes["sales_order"]
            )
        processed_dataframes["fact_sales_order"] = df_fact_sales_order

    if "staff" in table_list and "department" in table_list:
        logger.info("Creating df_dim_staff")
        df_dim_staff = create_df_dim_staff(
            tables_with_dataframes["staff"],
            tables_with_dataframes["department"]
            )
        processed_dataframes["dim_staff"] = df_dim_staff
    
    if "address" in table_list:
        logger.info("Creating df_dim_location")
        df_dim_location = create_dim_location(
            df_fact_sales_order,
            tables_with_dataframes["address"]
            )
        processed_dataframes["dim_location"] = df_dim_location
    
    if "sales_order" in table_list:
        logger.info("Creating df_dim_date")
        df_dim_date = create_df_dim_date(
            df_fact_sales_order
            )
        processed_dataframes["dim_date"] = df_dim_date

    if "currency" in table_list:
        logger.info("Creating df_dim_currency")
        df_dim_currency = create_df_dim_currency(
            tables_with_dataframes["currency"]
            )
        processed_dataframes["dim_currency"] = df_dim_currency
        
    if "address" in table_list and "sales_order" in table_list:
        logger.info("Creating df_dim_loaction")
        df_dim_loaction = create_dim_location(
            df_fact_sales_order,
            tables_with_dataframes["address"]
            )
        processed_dataframes["dim_location"] = df_dim_location

    if "design" in table_list:
        logger.info("Creating df_dim_design")
        df_dim_design = create_df_dim_design(
            tables_with_dataframes["design"]
            )
        processed_dataframes["dim_design"] = df_dim_design

    if "counterparty" in table_list and "address" in table_list:
        logger.info("Creating dim_counterparty_df")
        df_dim_counterparty = create_df_dim_counterparty(
            tables_with_dataframes["counterparty"],
            tables_with_dataframes["address"]
        )
        processed_dataframes["dim_counterparty"] = df_dim_counterparty

    processed_dataframe_list = list(processed_dataframes.keys())
    dataframe_parquet_filepaths = {}

    logger.info(f"Processed tables: {processed_dataframe_list}")

    logger.info("Converting dataframes to parquet files")
    for df in processed_dataframe_list:
        logger.info(f"Converting {df}_df to parquet file")
        dataframe_parquet_filepaths[df] = convert_dataframe_to_parquet_bytes(
            processed_dataframes[df]
            )

    logger.info("Uploading parquet files to Processed S3 Bucket")
    for df in processed_dataframe_list:
        logger.info(f"Uploading {df}...")
        upload_to_processed_bucket(
            dataframe_parquet_filepaths[df],
            f"{df}/{timestamp}.pq"
            )
        logger.info("Upload complete!")

    logger.info("Transform Lambda ended execution")

    pq_with_filepaths = {}
    for df in processed_dataframe_list:
        pq_with_filepaths[df] = f"{df}/{timestamp}.pq"

    return pq_with_filepaths
