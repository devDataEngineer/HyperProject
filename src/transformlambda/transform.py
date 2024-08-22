
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

example_argument = {
    "counterparty": "counterparty/2024/08/20/12-00-00.json",
    "currency": "currency/2024/08/20/12-00-00.json"
}

# -------------------------------------------------------------------------- #

def get_arguments(event) -> dict:
    """Retrieves passed dictionary from AWS event object
    """
    pass

def get_data(filepath: str) -> str:
    """Retrieves a single file from s3 ingestion bucket
    Extracts and returns json file data"""
    pass

def convert_data(data: str) -> pd.DataFrame:
    """Converts json data into pandas Dataframe
    Returns that dataframe"""
    pass

def convert_dataframe_to_parquet(dataframe: pd.DataFrame) -> bytes:
    """Takes a transformed Dataframe and converts it to parquet format
    Returns that parquet in the form of bytes
    """
    pass

def upload_to_processed_bucket(parquet_file: bytes, filename: str) -> None:
    """Takes parquet as bytes and a filename
    Puts parquet into Processed S3 Bucket named as filename"""
    pass

# -------------------------------------------------------------------------- #

def create_fact_sales_order_df(sales_order: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def create_dim_staff_df(fact_sales_order: pd.DataFrame, staff: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def create_dim_location_df(fact_sales_order: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def create_dim_date_df(fact_sales_order: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def create_dim_currency_df(fact_sales_order: pd.DataFrame, currency: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def create_dim_counterparty_df(fact_sales_order: pd.DataFrame, counterparty: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

# -------------------------------------------------------------------------- #

def lambda_handler(event, context) -> None:
    """DOCSTRING GOES HERE"""

    logger.info("Transform Lambda beggining execution")

    logger.info("Retrieving arguments from previous Extract Lambda")
    tables_with_filepaths = get_arguments()
    tables_with_json_data = {}

    table_list = tables_with_filepaths.keys()
    logger.info(f"Tables to update: {table_list}")
    # table_list = [
    #     'counterparty', 'currency', 'department', 'design',
    #     'staff', 'sales_order', 'address', 'payment',
    #     'purchase_order', 'payment_type', 'transaction'
    #     ]

    logger.info("Retrieving json files from Extract S3 Bucket")
    for table in table_list:
        logger.info(f"Retrieving {tables_with_filepaths[table]}...")
        tables_with_json_data[table] = get_data(
            tables_with_filepaths[table]
            )
        logger.info(f"{table} file retrieved")

    tables_with_dataframes = {}

    logger.info(f"Converting tables from json to dataframe")
    for table in table_list:
        tables_with_dataframes[table] = convert_data(
            tables_with_json_data[table]
            )
        logger.info(f"Table [{table}] converted")

    logger.info("Creating fact_sales_order_df")
    fact_sales_order_df = create_fact_sales_order_df(
        tables_with_dataframes["sales_order"]
        )
    
    logger.info("Creating dim_staff_df")
    dim_staff_df = create_dim_staff_df(
        fact_sales_order_df,
        tables_with_dataframes["staff"],
        tables_with_dataframes["department"]
        )
    
    logger.info("Creating dim_location_df")
    dim_location_df = create_dim_location_df(
        fact_sales_order_df,
        tables_with_dataframes["address"]
        )
    
    logger.info("Creating dim_date_df")
    dim_date_df = create_dim_date_df(fact_sales_order_df)

    logger.info("Creating dim_currency_df")
    dim_currency_df = create_dim_currency_df(
        fact_sales_order_df,
        tables_with_dataframes["currency"]
        )

    logger.info("Creating dim_counterparty_df")
    dim_counterparty_df = create_dim_counterparty_df(
        fact_sales_order_df,
        tables_with_dataframes["counterparty"],
        tables_with_dataframes["address"]
    )
    
    dataframes = {
        "fact_sales_order": fact_sales_order_df,
        "dim_staff": dim_staff_df,
        "dim_location": dim_location_df,
        "dim_date": dim_date_df,
        "dim_currency": dim_currency_df,
        "dim_counterparty": dim_counterparty_df
    }
    dataframe_list = dataframes.keys()

    dataframe_parquet_filepaths = {}

    logger.info("Converting dataframes to parquet files")
    for df in dataframe_list:
        logger.info(f"Converting {df}_df to parquet file")
        dataframe_parquet_filepaths[df] = convert_dataframe_to_parquet(
            dataframes[df]
            )
        logger.info(f"File created: {dataframe_parquet_filepaths[df]}")

    logger.info("Uploading parquet files to Processed S3 Bucket")
    for df in dataframe_list:
        logger.info(f"Uploading {df}...")
        upload_to_processed_bucket(
            dataframe_parquet_filepaths[df],
            "FILENAME_GOES_HERE"
            )
        logger.info("Upload complete!")

    logger.info("Transform Lambda ended execution")
