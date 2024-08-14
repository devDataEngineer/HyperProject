from src.connection import close_db_connection, db_connection
from pg8000 import DatabaseError

def read_table(db_table):

    table_whitelist = ['counterparty', 'currency', 'department', 'design', 'staff', 
                       'sales_order', 'address', 'payment', 'purchase_order', 'payment_type', 'transaction']
    
    if db_table not in table_whitelist:
        raise ValueError(f"Invalid table name: {db_table}")
    
    try:
        conn = db_connection()
        staff_query = f"SELECT * FROM {db_table};"
        staff_table = conn.run(staff_query)
        return staff_table
    
    except DatabaseError as e:
        raise e
    
    finally:
       close_db_connection(conn)