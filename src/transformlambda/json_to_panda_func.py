import pandas as pd
import json
import logging
from io import StringIO

logger = logging.getLogger()
logger.setLevel("INFO")

def json_to_panda_df(json_bytes_object): #json object
    
    try:
        panda_df = pd.read_json(StringIO(json_bytes_object))
        
        if panda_df.empty == True:
            logger.info("The DataFrame is empty.")
        else:
            return panda_df
        
    except ValueError:
        logger.error("The input is not a JSON object.")   

   
    

    