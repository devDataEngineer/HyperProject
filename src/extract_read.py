from src.connection import close_db_connection, db_connection
#import src.connection
from pg8000 import DatabaseError

def read_staff_table(db_table):

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
       #print(conn.close())
       #staff_table = conn.run(staff_query)      

#print(read_staff_table("staff"))

# counterparty, 
# currency, 
# department, 
# design, 
# staff, 
# sales_order, 
# address, 
# payment, 
# purchase_order, 
# payment_type, 
# transaction