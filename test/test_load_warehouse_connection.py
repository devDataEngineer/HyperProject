from src.loadlambda.load_warehouse_connection import warehouse_connection
import json
#import pg8000

# def test_schema_correct():
#     conn1=warehouse_connection()
#     cur = conn1.cursor()
#     result = cur.execute("select * from information_schema.tables;")
#     print(conn1)
#     print(cur)
#     assert conn1 is not None
#     assert result is not None