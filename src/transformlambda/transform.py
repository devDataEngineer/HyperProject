
import pandas as pd

# example_argument = {
#     "counterparty": "counterparty/2024/08/20/12-00-00.json",
#     "currency": "currency/2024/08/20/12-00-00.json"
# }

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

# tables = {
#     "counterparty": pd.DataFrame(),
#     "currency": pd.DataFrame(),
#     "department": pd.DataFrame(),
#     "design": pd.DataFrame(),
#     "staff": pd.DataFrame(),
#     "sales_order": pd.DataFrame(),
#     "address": pd.DataFrame(),
#     "payment": pd.DataFrame(),
#     "purchase_order": pd.DataFrame(),
#     "payment_type": pd.DataFrame(),
#     "transaction": pd.DataFrame()
# }

def get_data(filepath: str) -> str:
    """Retrieves a single file from s3 ingestion bucket
    Extracts and returns json file data"""
    pass

def convert_data(data: str) -> pd.DataFrame:
    """Converts json data into pandas Dataframe
    Returns that dataframe"""
    pass

def get_arguments(event) -> dict:
    """Retrieves passed dictionary from AWS event object
    """
    pass

def convert_dataframe_to_parquet(dataframe: pd.DataFrame):
    """Takes a transformed Dataframe and converts it to parquet format
    """
    pass

def upload_to_transform_bucket(parquet_file):
    """DOCSTRING GOES HERE"""
    # currently unsure of transform bucket folder / file structure

    pass

def lambda_handler(event, context) -> None:
    """DOCSTRING GOES HERE"""

    pass
