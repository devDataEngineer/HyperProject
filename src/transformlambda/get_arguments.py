import boto3

import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def get_arguments(event) -> dict:

    table_list = [
        'counterparty', 'currency', 'department', 'design',
        'staff', 'sales_order', 'address', 'payment',
        'purchase_order', 'payment_type', 'transaction'
        ]
    
    tables_with_filepaths = {}

    recieved_tables = event.keys()

    for table in recieved_tables:
        if table in table_list:
            tables_with_filepaths[table] = event[table]
        else:
            logging.error("Lambda invoked with no tables to transform")

    return tables_with_filepaths
