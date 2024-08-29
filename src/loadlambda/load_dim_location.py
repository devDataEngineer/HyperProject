try:
    from src.loadlambda.load_warehouse_connection import warehouse_connection
except:
    from load_warehouse_connection import warehouse_connection

import logging


logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_location_to_warehouse(dim_location_df):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing dim_location_df DataFrame to warehouse")
    try:
        for _, row in dim_location_df.iterrows():
            cur.execute(
                """INSERT INTO dim_location (
                    "location_id",
                    "address_line_1",
                    "address_line_2",
                    "district",
                    "city",
                    "postal_code",
                    "country",
                    "phone") 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (location_id) DO NOTHING;""",
                (
                row['location_id'],row['address_line_1'],row['address_line_2'],row['district'], 
                row['city'], row['postal_code'],row['country'],row['phone']),
            )
        # committing the current transaction to the database
        conn.commit()

        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_location_df}. More info:" + str(e))
        raise e
