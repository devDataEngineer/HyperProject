from src.connection import close_db_connection, db_connection
from utilities.utilities import format_extract_lambda_as_rows
from pg8000 import DatabaseError


def read_table(db_table):

    table_whitelist = ['counterparty', 'currency', 'department', 'design', 
                       'staff', 'sales_order', 'address', 'payment', 
                       'purchase_order', 'payment_type', 'transaction']
    
    if db_table not in table_whitelist:
        raise ValueError(f"Invalid table name: {db_table}")
    
    try:
        conn = db_connection()
        query = f"SELECT * FROM {db_table};"
        rows = conn.run(query)
        column_list = [conn.columns[i]['name'] for i in range(len(conn.columns))]
        formatted = format_extract_lambda_as_rows(rows,column_list)
        return formatted
    
    except DatabaseError as e:
        raise e
    
    finally:
       close_db_connection(conn)