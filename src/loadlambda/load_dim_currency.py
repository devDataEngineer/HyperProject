try:
    from src.loadlambda.load_warehouse_connection import warehouse_connection
except:
    from load_warehouse_connection import warehouse_connection
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_currency_to_warehouse(dim_currency_df):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing dim_currency_df DataFrame to warehouse")
    try:
        for _, row in dim_currency_df.iterrows():
            cur.execute(
                """INSERT INTO dim_currency (
                "currency_id",
                "currency_code",
                "currency_name") 
                VALUES (%s, %s, %s)
                ON CONFLICT (currency_id) DO NOTHING;""",
                (
                row['currency_id'],
                row['currency_code'],row['currency_name'], 
                )
            )
        # committing the current transaction to the database
        conn.commit()

        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_currency_df}. More info:" + str(e))
        raise e