from connection import conn, close_db_connection

def get_transactions_data():
    
    try:
        query = "SELECT * FROM transaction;"
        result = conn.run(query)
        return result
    finally:
        close_db_connection(conn)

print(get_transactions_data())