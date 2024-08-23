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

# example_argument = {
#     "counterparty": "counterparty/2024/08/20/12-00-00.json",
#     "currency": "currency/2024/08/20/12-00-00.json"
# }

do_it = {
    "counterparty": "counterparty/2024/08/23/13-49-02.json",
    "currency": "currency/2024/08/23/13-49-02.json",
    "department": "department/2024/08/23/13-49-02.json",
    "design": "design/2024/08/23/13-49-02.json",
    "staff": "staff/2024/08/23/13-49-02.json",
    "sales_order": "sales_order/2024/08/23/13-49-02.json",
    "address": "address/2024/08/23/13-49-02.json",
    # "payment": "payment/2024/08/23/13-49-02.json",
    # "purchase_order": "purchase_order/2024/08/23/13-49-02.json",
    # "payment_type": "payment_type/2024/08/23/13-49-02.json",
    # "transaction": "transaction/2024/08/23/13-49-02.json"
}

    #     'counterparty', 'currency', 'department', 'design',
    #     'staff', 'sales_order', 'address', 'payment',
    #     'purchase_order', 'payment_type', 'transaction'
    #     ]

# -------------------------------------------------------------------------- #

# def get_arguments(event) -> dict:
#     """Retrieves passed dictionary from AWS event object
#     """
#     pass

# def get_data(filepath: str) -> str:
#     """Retrieves a single file from s3 ingestion bucket
#     Extracts and returns json file data"""
#     pass

# def json_to_panda_df(data: str) -> pd.DataFrame:
#     """Converts json data into pandas Dataframe
#     Returns that dataframe"""
#     pass

# def convert_dataframe_to_parquet(dataframe: pd.DataFrame) -> bytes:
#     """Takes a transformed Dataframe and converts it to parquet format
#     Returns that parquet in the form of bytes
#     """
#     pass

# def upload_to_processed_bucket(parquet_file: bytes, filename: str) -> None:
#     """Takes parquet as bytes and a filename
#     Puts parquet into Processed S3 Bucket named as filename"""
#     pass

# -------------------------------------------------------------------------- #

# def create_df_fact_sales_order(df_sales_order: pd.DataFrame) -> pd.DataFrame:
#     """ DOCSTRING GOES HERE"""
#     pass

# def create_df_dim_staff(df_fact_sales_order: pd.DataFrame, staff: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
#     """DOCSTRING GOES HERE"""
#     pass

# def create_df_dim_location(df_fact_sales_order: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
#     """DOCSTRING GOES HERE"""
#     pass

# def create_df_dim_date(df_fact_sales_order: pd.DataFrame) -> pd.DataFrame:
#     """DOCSTRING GOES HERE"""
#     pass

# def create_df_dim_currency(df_currency: pd.DataFrame) -> pd.DataFrame:
#     """DOCSTRING GOES HERE"""
#     pass

# def create_df_dim_counterparty(df_fact_sales_order: pd.DataFrame, counterparty: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
#     """DOCSTRING GOES HERE"""
#     pass

# -------------------------------------------------------------------------- #

def lambda_handler(event, context) -> None:
    """TRANSFORM"""

    print("Transform Lambda beggining execution")

    print("Retrieving arguments from previous Extract Lambda")
    tables_with_filepaths = get_arguments(event)
    tables_with_json_data = {}

    table_list = list(tables_with_filepaths.keys())
    print(f"Tables to update: {table_list}")
    # table_list = [
    #     'counterparty', 'currency', 'department', 'design',
    #     'staff', 'sales_order', 'address', 'payment',
    #     'purchase_order', 'payment_type', 'transaction'
    #     ]

    print("Retrieving json files from Extract S3 Bucket")
    for table in table_list:
        print(f"Retrieving {tables_with_filepaths[table]}...")
        tables_with_json_data[table] = get_data_from_ingestion_bucket(
            tables_with_filepaths[table]
            )
        print(f"{table} file retrieved")

    tables_with_dataframes = {}

    print(f"Converting tables from json to dataframe")
    for table in table_list:
        tables_with_dataframes[table] = json_to_panda_df(
            tables_with_json_data[table]
            )
        print(f"Table [{table}] converted")

    processed_dataframes = {}
    processed_dataframe_list = []

    if "sales_order" in table_list:
        print("Creating df_fact_sales_order")
        df_fact_sales_order = create_df_fact_sales_order(
            tables_with_dataframes["sales_order"]
            )
        processed_dataframes["df_fact_sales_order"] = df_fact_sales_order

    if "staff" in table_list and "department" in table_list:
        print("Creating df_dim_staff")
        df_dim_staff = create_df_dim_staff(
            tables_with_dataframes["staff"],
            tables_with_dataframes["department"]
            )
        processed_dataframes["df_dim_staff"] = df_dim_staff
    
    # if "address" in table_list:
    #     print("Creating df_dim_location")
    #     df_dim_location = create_dim_location(
    #         df_fact_sales_order,
    #         tables_with_dataframes["address"]
    #         )
    #     processed_dataframes["df_dim_location"] = df_dim_location
    
    # if "sales_order" in table_list:
    #     print("Creating df_dim_date")
    #     df_dim_date = create_df_dim_date(df_fact_sales_order)
    #     processed_dataframes["df_dim_date"] = df_dim_date

    # if "currency" in table_list:
    #     print("Creating df_dim_currency")
    #     df_dim_currency = create_df_dim_currency(
    #         tables_with_dataframes["currency"]
    #         )
    #     processed_dataframes["df_dim_currency"] = df_dim_currency
        
    # if "location" in table_list:
    #     print("Creating df_dim_loaction")
    #     df_dim_loaction = create_dim_location(
    #         df_fact_sales_order,
    #         tables_with_dataframes["location"]
    #         )
    #     processed_dataframes["df_dim_loaction"] = df_dim_loaction

    if "counterparty" in table_list and "address" in table_list:
        print("Creating dim_counterparty_df")
        df_dim_counterparty = create_df_dim_counterparty(
            tables_with_dataframes["counterparty"],
            tables_with_dataframes["address"]
        )
        processed_dataframes["df_dim_counterparty"] = df_dim_counterparty
    
    # dataframes = {
    #     "fact_sales_order": df_fact_sales_order,
    #     "df_dim_staff": df_dim_staff,
    #     "df_dim_location": df_dim_location,
    #     "df_dim_date": df_dim_date,
    #     "df_dim_currency": df_dim_currency,
    #     "df_dim_counterparty": df_dim_counterparty,
    #     "df_dim_currency": df_dim_currency,
    #     "df_dim_loaction": df_dim_loaction
    # }

    processed_dataframe_list = processed_dataframes.keys()
    dataframe_parquet_filepaths = {}

    print(f"Processed tables: {processed_dataframe_list}")

    print("Converting dataframes to parquet files")
    for df in processed_dataframe_list:
        print(f"Converting {df}_df to parquet file")
        dataframe_parquet_filepaths[df] = convert_dataframe_to_parquet(
            processed_dataframes[df]
            )
        print(f"File created: {dataframe_parquet_filepaths[df]}")

    print("Uploading parquet files to Processed S3 Bucket")
    for df in processed_dataframe_list:
        print(f"Uploading {df}...")
        upload_to_processed_bucket(
            dataframe_parquet_filepaths[df],
            f"FILENAME_GOES_HERE_{df}"
            )
        print("Upload complete!")

    print("Transform Lambda ended execution")

lambda_handler(event=do_it, context=None)