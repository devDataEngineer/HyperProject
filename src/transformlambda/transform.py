
import pandas as pd

# example_argument = {
#     "counterparty": "counterparty/2024/08/20/12-00-00.json",
#     "currency": "currency/2024/08/20/12-00-00.json"
# }

def transform_counterparty(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_currency(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_department(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_design(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_staff(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_sales_order(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_address(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_payment(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_purchase_order(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_payment_type(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

def transform_transaction(data: pd.DataFrame) -> pd.DataFrame:
    """DOCSTRING GOES HERE"""
    pass

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