import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def create_df_dim_design(df_design):
    
    try:
        logger.info("Started processing dim_date DataFrame")
        dim_design = df_design
        dim_design = dim_design.drop(columns=['created_at', 'last_updated'])
        dim_design.set_index = dim_design['design_id']
        dim_design.name = "dim_design"
        return dim_design   
    
    except Exception as e:
      logger.error(f"Error occured during formating {dim_design.name}. More info:" + str(e))
      raise e
   
   
    