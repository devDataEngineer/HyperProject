try:
    from src.transform_lambda.create_df_fact_sales_order import create_df_fact_sales_order
    from src.transform_lambda.create_df_dim_staff import create_df_dim_staff
    from src.transform_lambda.create_df_dim_date import create_df_dim_date
    from src.transform_lambda.create_df_dim_currency import create_df_dim_currency
    from src.transformlambda.dim_location import create_dim_location
    from src.transformlambda.dim_design import create_df_dim_design
    from src.transformlambda.get_arguments import get_arguments
    from src.transform_lambda.get_data import get_data_from_ingestion_bucket
    from src.transformlambda.json_to_panda_func import json_to_panda_df
    from src.transformlambda.panda_df_to_parq import convert_dataframe_to_parquet
    from src.transformlambda.upload_to_processed_bucket import upload_to_processed_bucket
    from src.transformlambda.dim_counterparty import create_df_dim_counterparty
except:
    from create_df_fact_sales_order import create_df_fact_sales_order
    from create_df_dim_staff import create_df_dim_staff
    from create_df_dim_date import create_df_dim_date
    from create_df_dim_currency import create_df_dim_currency
    from dim_location import create_dim_location
    from dim_design import create_df_dim_design
    from dim_counterparty import create_df_dim_counterparty
    from get_arguments import get_arguments
    from get_data import get_data_from_ingestion_bucket
    from json_to_panda_func import json_to_panda_df
    from panda_df_to_parq import convert_dataframe_to_parquet
    from upload_to_processed_bucket import upload_to_processed_bucket

import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

# event = {
#     "counterparty": "counterparty/2024/08/26/10-36-18.json",
#     "currency": "currency/2024/08/26/10-36-18.json",
#     "department": "department/2024/08/26/10-36-18.json",
#     "design": "design/2024/08/26/10-36-18.json",
#     "staff": "staff/2024/08/26/10-36-18.json",
#     "sales_order": "sales_order/2024/08/26/10-36-18.json",
#     "address": "address/2024/08/26/10-36-18.json",
#     "payment": "payment/2024/08/26/10-36-18.json",
#     "purchase_order": "purchase_order/2024/08/26/10-36-18.json",
#     "payment_type": "payment_type/2024/08/26/10-36-18.json",
#     "transaction": "transaction/2024/08/26/10-36-18.json"
# }

# -------------------------------------------------------------------------- #

def lambda_handler(event, context) -> None:
    """TRANSFORM"""

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
        processed_dataframes["df_fact_sales_order"] = df_fact_sales_order

    if "staff" in table_list and "department" in table_list:
        logger.info("Creating df_dim_staff")
        df_dim_staff = create_df_dim_staff(
            tables_with_dataframes["staff"],
            tables_with_dataframes["department"]
            )
        processed_dataframes["df_dim_staff"] = df_dim_staff
    
    if "address" in table_list:
        logger.info("Creating df_dim_location")
        df_dim_location = create_dim_location(
            df_fact_sales_order,
            tables_with_dataframes["address"]
            )
        processed_dataframes["df_dim_location"] = df_dim_location
    
    if "sales_order" in table_list:
        logger.info("Creating df_dim_date")
        df_dim_date = create_df_dim_date(
            df_fact_sales_order
            )
        processed_dataframes["df_dim_date"] = df_dim_date

    if "currency" in table_list:
        logger.info("Creating df_dim_currency")
        df_dim_currency = create_df_dim_currency(
            tables_with_dataframes["currency"]
            )
        processed_dataframes["df_dim_currency"] = df_dim_currency
        
    if "address" in table_list:
        logger.info("Creating df_dim_loaction")
        df_dim_loaction = create_dim_location(
            df_fact_sales_order,
            tables_with_dataframes["address"]
            )
        processed_dataframes["df_dim_loaction"] = df_dim_loaction

    if "design" in table_list:
        logger.info("Creating df_dim_design")
        df_dim_design = create_df_dim_design(
            tables_with_dataframes["design"]
            )
        processed_dataframes["df_dim_loaction"] = df_dim_loaction

    if "counterparty" in table_list and "address" in table_list:
        logger.info("Creating dim_counterparty_df")
        df_dim_counterparty = create_df_dim_counterparty(
            tables_with_dataframes["counterparty"],
            tables_with_dataframes["address"]
        )
        processed_dataframes["df_dim_counterparty"] = df_dim_counterparty

    processed_dataframe_list = processed_dataframes.keys()
    dataframe_parquet_filepaths = {}

    logger.info(f"Processed tables: {processed_dataframe_list}")

    logger.info("Converting dataframes to parquet files")
    for df in processed_dataframe_list:
        logger.info(f"Converting {df}_df to parquet file")
        dataframe_parquet_filepaths[df] = convert_dataframe_to_parquet(
            processed_dataframes[df]
            )

    logger.info("Uploading parquet files to Processed S3 Bucket")
    for df in processed_dataframe_list:
        logger.info(f"Uploading {df}...")
        upload_to_processed_bucket(
            dataframe_parquet_filepaths[df],
            f"{df}.pq"
            )
        logger.info("Upload complete!")

    logger.info("Transform Lambda ended execution")
