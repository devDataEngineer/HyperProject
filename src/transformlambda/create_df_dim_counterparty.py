import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def create_df_dim_counterparty(df_counterparty: pd.DataFrame, df_address: pd.DataFrame) -> pd.DataFrame:
    try: 
        logger.info("Started processing counterparty DataFrame")
        dim_counterparty = df_counterparty
        df_address = df_address.drop(columns = ['created_at', 'last_updated'])
        dim_counterparty = pd.merge(dim_counterparty, df_address, how='left', left_on='legal_address_id', right_on='address_id')
        dim_counterparty = dim_counterparty.drop(columns=[ 'legal_address_id', 'commercial_contact', 'delivery_contact', 'created_at', 'last_updated', 'address_id'])
        dim_counterparty.set_index = dim_counterparty['counterparty_id']
        dim_counterparty = dim_counterparty.rename(columns={"address_line_1": "counterparty_legal_address_line_1", "address_line_2": "counterparty_legal_address_line_2", "district": "counterparty_legal_district", "city": "counterparty_legal_city", "postal_code": "counterparty_legal_postal_code" , "country": "counterparty_legal_country", "phone": "counterparty_legal_phone_number"})
        dim_counterparty.name = "dim_counterparty"
        return dim_counterparty
    
    except Exception as e:
        logger.error(f"Error occured during formating {dim_counterparty.name}. More info:" + str(e))
        raise e

    
    
    

    
    
    