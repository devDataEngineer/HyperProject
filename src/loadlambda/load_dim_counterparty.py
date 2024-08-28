from src.loadlambda.load_warehouse_connection import warehouse_connection
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_counterparty_to_warehouse(dim_counterpary_df, table_name="dim_counterparty"):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing {dim_counterpary_df} DataFrame to warehouse")
    try:
        for _, row in dim_counterpary_df.iterrows():
            cur.execute(
                f"""INSERT INTO {table_name} (
                "counterparty_id","counterparty_legal_name","counterparty_legal_address_line_1",
                "counterparty_legal_address_line_2","counterparty_legal_district", "counterparty_legal_city",
                "counterparty_legal_postal_code", "counterparty_legal_country","counterparty_legal_phone_number") 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                row['counterparty_id'],row['counterparty_legal_name'],row['counterparty_legal_address_line_1'],row['counterparty_legal_address_line_2'], 
                row['counterparty_legal_district'], row['counterparty_legal_city'],row['counterparty_legal_postal_code'],row['counterparty_legal_country'] ,row['counterparty_legal_phone_number'])
            )
        # committing the current transaction to the database
        conn.commit()

        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_counterpary_df}. More info:" + str(e))
        raise e
