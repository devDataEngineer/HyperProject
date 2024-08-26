import json
import boto3
import boto3.exceptions
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#----------formate dim_currency data frame----------------------#
def create_df_dim_currency(df_currency):
    try:
        logger.info("Started processing dim_currency DataFrame")
        dim_currency = df_currency.copy()
        currency_names = {
                    'GBP': 'British Pound',
                    'USD': 'US Dollar',
                    'EUR': 'Euro',
                    'CHF': 'Swiss Franc'
                }
        dim_currency['currency_name'] = dim_currency['currency_code'].apply(lambda x: currency_names[x])
        dim_currency = dim_currency.drop(columns = ['created_at','last_updated'])
        dim_currency.set_index= dim_currency['currency_id']
        dim_currency.name = "dim_currency"
        logger.info("Finishing processing dim_currency DataFrame")
        return dim_currency
    except Exception as e:
        logger.error(f"Error occured during formating {dim_currency.name}. More info:" + str(e))
        raise e