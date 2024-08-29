from src.loadlambda.load_warehouse_connection import warehouse_connection
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_staff_to_warehouse(dim_staff_df, table_name="dim_staff"):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing {dim_staff_df} DataFrame to warehouse")
    try:
        for _, row in dim_staff_df.iterrows():
            cur.execute(
                f"""INSERT INTO {table_name} (
                "staff_id", "first_name", "last_name", 
                "department_name", "location",
                "email_address") 
                VALUES (%s, %s, %s,%s, %s, %s)""",
                (
                row['staff_id'],row['first_name'],row['last_name'], 
                row['department_name'],row['location'],row['email_address']
                )
            )
        # committing the current transaction to the database
        conn.commit()
        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_staff_df}. More info:" + str(e))
        raise e