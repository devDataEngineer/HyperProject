import pandas as pd
import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def create_dim_location(df_fact_sales_order: pd.DataFrame, df_dim_address: pd.DataFrame) -> pd.DataFrame:
    try : 
        logger.info("Started processing dim_location DataFrame")
        dim_location = df_dim_address
        dim_location['location_id'] = df_fact_sales_order[ "agreed_delivery_location_id"]
        dim_location.set_index = dim_location['location_id']
        dim_location = dim_location.drop(columns=['created_at', 'last_updated','address_id'])
        dim_location.name = "dim_location"
        return dim_location
    except Exception as e:
      logger.error(f"Error occured during formating {dim_location.name}. More info:" + str(e))
      raise e
    

   
    
