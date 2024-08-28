try:
    from src.loadlambda.load_warehouse_connection import warehouse_connection
except:
    from load_warehouse_connection import warehouse_connection

import logging


logger = logging.getLogger()
logger.setLevel("INFO")

def load_dim_design_to_warehouse(dim_design_df):
    conn = warehouse_connection()
    cur = conn.cursor()
    logger.info(f"Started processing {dim_design_df} DataFrame to warehouse")
    try:
        for _, row in dim_design_df.iterrows():
            cur.execute(
                """INSERT INTO dim_design (
                    design_id,
                    design_name,
                    file_location,
                    file_name
                    ) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (design_id) DO NOTHING;""",
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
