import pg8000.native
try:
    from db_secrets import get_secret
except:
    from src.extractlambda.db_secrets import get_secret

def db_connection():
    secrets = get_secret()
    return pg8000.native.Connection(
            user=secrets["username"], 
            password=secrets["password"],
            database=secrets["dbname"],
            host=secrets["host"],
            port=int(secrets["port"])
        )
    

def close_db_connection(conn):
    conn.close()