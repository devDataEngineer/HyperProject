import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#either pyarrow or fastparquet must be pip installed
def convert_dataframe_to_parquet_bytes(input_df):
    try:
        if isinstance(input_df, pd.DataFrame):
            pq_bytes = input_df.to_parquet()
            logger.info("Df converted to parquet.")
            return pq_bytes
        else:
            logger.error("Please input a Panda Dataframe.")
            
            
    
    except:
        logger.error("Df failed to conversion to parquet.")

    
  



