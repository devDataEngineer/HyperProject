from connection import conn, close_db_connection
from pg8000 import DatabaseError

def read_staff_table(var):
    try:
        staff_query = "SELECT * FROM (:table);"

        staff_table = conn.run(staff_query, table=var)
        return staff_table
    except DatabaseError as e:
        raise e
    finally:
        close_db_connection(conn)

print(read_staff_table("staff"))