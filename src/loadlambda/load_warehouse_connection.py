import pg8000.dbapi
from src.loadlambda.load_secrets import get_warehouse_secret

def warehouse_connection():
    secrets = get_warehouse_secret()
    conn = pg8000.dbapi.connect( 
            user=secrets["username"], 
            password=secrets["password"],
            database=secrets["dbname"],
            host=secrets["host"],
            port=int(secrets["port"])
            )


    return conn
        
def close_warehouse_connection(conn):
    conn.close()
