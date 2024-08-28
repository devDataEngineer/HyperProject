try:
    from src.loadlambda.load_warehouse_connection import warehouse_connection
except:
    from load_warehouse_connection import warehouse_connection

import logging


logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_date_to_warehouse(dim_date_df, table_name="dim_date"):
    conn = warehouse_connection()
    cur = conn.cursor()
    try:
        logger.info(f"Started processing {dim_date_df} DataFrame to warehouse")
        for _, row in dim_date_df.iterrows():
            cur.execute(
                """INSERT INTO dim_date (
                    date_id,
                    year,
                    month,
                    day,
                    day_of_week,
                    day_name,
                    month_name,
                    quarter") 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (date_id) DO NOTHING;""",
                (
                row['date_id'],row['year'],row['month'],row['day'], 
                row['day_of_week'], row['day_name'],row['month_name'],row['quarter'])
            )

        # committing the current transaction to the database
        conn.commit()

        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_date_df}. More info:" + str(e))
        raise e
