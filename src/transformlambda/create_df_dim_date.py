import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#----------formate dim_date_df data frame----------------------#
def create_df_dim_date(df_fact_sales_order): # get df_fact_sale as argument
    try:
        logger.info("Started processing dim_date DataFrame")

        dim_date = df_fact_sales_order[['created_date']].copy()
        created_date = pd.to_datetime(dim_date['created_date'])

        dim_date['year'] = pd.DatetimeIndex(created_date).year
        dim_date['month'] = pd.DatetimeIndex(created_date).month
        dim_date['day'] = pd.DatetimeIndex(created_date).day
        dim_date['day_of_week'] = pd.DatetimeIndex(created_date).day_of_week
        dim_date['day_name'] = created_date.dt.day_name()
        dim_date['month_name'] = created_date.dt.month_name()
        dim_date['quarter'] = pd.DatetimeIndex(created_date).quarter
        dim_date = dim_date.rename(columns = {'created_date': "date_id"})
        dim_date.set_index = dim_date['date_id']
        dim_date.name = 'dim_date'

        logger.info("Finishing processing dim_date DataFrame")
        return dim_date

    except Exception as e:
        logger.error(f"Error occured during formating {dim_date}. More info:" + str(e))
        raise e
