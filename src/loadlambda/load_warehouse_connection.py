import pg8000.native
from src.loadlambda.load_secrets import get_warehouse_secret

def warehouse_connection():
    secrets = get_warehouse_secret()
    conn = pg8000.native.Connection( 
            user=secrets["username"], 
            password=secrets["password"],
            database=secrets["dbname"],
            host=secrets["host"],
            port=int(secrets["port"])
            )

    conn.run(f'SET search_path TO {secrets["username"]}')

    return conn

        
def close_warehouse_connection(conn):
    conn.close()