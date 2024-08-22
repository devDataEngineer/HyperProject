import pandas as pd
from src.transformlambda.json_to_panda_func import json_to_panda_df
import os
import logging
from io import BytesIO

logger = logging.getLogger()
logger.setLevel("INFO")

#either pyarrow or fastparquet must be pip installed
def convert_dataframe_to_parquet(input_df):
    try:
        df_bytes = input_df.to_parquet()
        logger.info("Df converted to parquet.")
        return df_bytes
    
    except:
        logger.info("Df failed to conversion to parquet.")

    
  



