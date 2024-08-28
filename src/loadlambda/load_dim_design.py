from src.loadlambda.load_warehouse_connection import warehouse_connection
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_date_to_warehouse(dim_design_df, table_name):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing {dim_design_df} DataFrame to warehouse")
    try:
        for _, row in dim_design_df.iterrows():
            cur.execute(
                f"""INSERT INTO {table_name} (
                "design_id",
                "design_name",
                "file_location",
                "file_name",
                ") 
                        VALUES (%s, %s, %s, %s)""",
                (
                row['design_id'],row['design_name'],row['file_location'],row['file_name'] 
                ),
            )
            
        # committing the current transaction to the database
        conn.commit()

        # closing the cursor
        cur.close()
        # closing the connection
        conn.close()
    except Exception as e:
        logger.error(f"Error occured during processing {dim_design_df}. More info:" + str(e))
        raise e
