import boto3

import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def get_arguments(event) -> dict:

    table_list = [
        'df_fact_sales_order'
        'df_dim_staff'
        'df_dim_location'
        'df_dim_design'
        'df_dim_date'
        'df_dim_currency'
        'df_dim_counterparty'
        ]
    
    tables_with_filepaths = {}

    recieved_tables = list(event.keys())
    if len(recieved_tables) == 0:
        logging.error("Lambda invoked with no tables to transform")

    for table in recieved_tables:
        if table in table_list:
            tables_with_filepaths[table] = event[table]

    return tables_with_filepaths
