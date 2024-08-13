import os
from dotenv import load_dotenv
from pg8000.native import Connection

load_dotenv()

def close_db_connection(conn):
    conn.close()

def db_connection():
    return pg8000.native.Connection(
            user=os.getenv("PG_USER"), 
            password=os.getenv("PG_PASSWORD"),
            database=os.getenv("PG_DATABASE"),
            host=os.getenv("PG_HOST"),
            port=int(os.getenv("PG_PORT"))
        )
    
conn = db_connection()

def close_db_connection(conn):
    conn.close()