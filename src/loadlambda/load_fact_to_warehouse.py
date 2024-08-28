import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from src.loadlambda.load_warehouse_connection import warehouse_connection




# from src.loadlambda.load_warehouse_connection  import warehouse_connection as conn
def load_fact_to_warehouse(fact_df, table_name):
    conn = warehouse_connection()
    
    cursor = conn.cursor()

    for _, row in fact_df.iterrows():
        cursor.execute(
            f"""INSERT INTO {table_name} ("sales_record_id",
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id") 
                    VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)""",
            (
            row['sales_record_id'],row['sales_order_id'],row['created_date'],row['created_time'], 
            row['last_updated_date'], row['last_updated_time'],row['sales_staff_id'],row['counterparty_id'],
                 row['units_sold'],row['unit_price'],row['currency_id'],row['design_id'],
                 row['agreed_payment_date'],row['agreed_delivery_date'],row['agreed_delivery_location_id']),
        )

    # committing the current transaction to the database
    conn.commit()

    # closing the cursor
    cursor.close()
    # closing the connection
    conn.close()




    # for i in range(0 ,len(df)):
    #     values = (df['sales_record_id'][i],row['sales_order_id'][i],row['created_date'][i],row['created_time'][i], 
    #              row['last_updated_date'][i],df['last_updated_time'][i],df['sales_staff_id'][i],df['counterparty_id'][i],
    #              row['units_sold'][i],df['unit_price'][i],df['currency_id'][i],df['design_id'][i],
    #              row['agreed_payment_date'][i],df['agreed_delivery_date'][i],df['agreed_delivery_location_id'][i])
    #     cur.execute(f"""INSERT INTO {table_name} ('sales_record_id','sales_order_id', 'created_date', 'created_time', 'last_updated_date',
    #                 'last_updated_time', 'sales_staff_id', 'counterparty_id', 'units_sold',
    #                 'unit_price', 'currency_id', 'design_id', 'agreed_payment_date',
    #                 'agreed_delivery_date', 'agreed_delivery_location_id') 
    #                 VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)""",
    #                 values)

    # conn.commit()
    # print("Records created successfully")
    # conn.close()




