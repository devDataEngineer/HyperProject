import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def get_arguments() -> dict:
    # partial copy paste
    pass

def get_pq_from_bucket() -> bytes:
    # can mostly copy get_data_from_ingestion_bucket
    # uses connection.py
    # db_secret needs changing
    # can copy paste some code for bucket
    pass

def pq_to_df(parquet: bytes) -> pd.DataFrame:
    # pandas method
    # pandas.read_parquet
    pass

def load_fact_to_warehouse(fact_table: pd.DataFrame) -> None:
    """
    Your warehouse should contain a full history of all updates to facts.
    For example, if a sales order is created in totesys and then later updated
    (perhaps the units_sold field is changed),
    you should have two records in the fact_sales_order table.
    It should be possible to see both the original and changed number of units_sold.
    It should be possible to query either the current state of the sale,
    or get a full history of how it has evolved (including deletion if applicable).
    """
    pass

def load_dim_to_warehouse(dim_table: pd.DataFrame) -> None:
    """
    It is not necessary to do this for dimensions (which should not change very much anyway).
    The warehouse should just have the latest version of the dimension values.
    However, you might want to keep a full record of changes to dimensions in the S3 buckets.
    """
    pass


def lambda_handler(event, context):

    tables_with_filenames = get_arguments(event)
    tables_with_pq = {}
    tables_with_df = {}

    table_list = list(tables_with_filenames.keys())

    for table in table_list:
        tables_with_pq[table] = get_pq_from_bucket(tables_with_filenames[table])
        tables_with_df[table] = pq_to_df(tables_with_pq[table])

    if "fact_sales_order" in table_list:
        table_list.remove("fact_sales_order")
        load_fact_to_warehouse(tables_with_df["fact_sales_order"])

    for table in table_list:
        load_dim_to_warehouse(tables_with_df[table])

    






# This is a temporary lambda function to check SNS and Cloud watch services
# client = boto3.client('sns')
         
# def lambda_handler(event, context):
#    try:  
#       messege = "this is from second transform lambad messege"
#       topic_arn = os.environ.get('TOPIC_ARN')
#       one = "One"
#       two = 2
#       total = sum(one, two)
#       return total
#    except TypeError:
      
#       client.publish(TopicArn=topic_arn,Message=messege)
