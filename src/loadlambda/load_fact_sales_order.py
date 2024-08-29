from src.loadlambda.load_warehouse_connection import warehouse_connection
import logging

logger = logging.getLogger()
logger.setLevel("INFO")


# from src.loadlambda.load_warehouse_connection  import warehouse_connection as conn
def load_fact_sales_to_warehouse(fact_df, table_name="fact_sales_order"):
    conn = warehouse_connection()
    cursor = conn.cursor()
    logger.info(f"Started processing {fact_df} DataFrame to warehouse")

    try:
        for _, row in fact_df.iterrows():
            cursor.execute(
                f"""INSERT INTO {table_name} (
                "sales_record_id",
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
    except Exception as e:
        logger.error(f"Error occured during processing {fact_df}. More info:" + str(e))
        raise e

