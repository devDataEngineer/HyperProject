import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#----------formate dim_date_df data frame----------------------#
def create_df_dim_date(df_fact_sales_order: pd.DataFrame) -> pd.DataFrame: # get df_fact_sale as argument
    try:
        logger.info("Started processing dim_date DataFrame")
        dim_date = df_fact_sales_order[['created_date']].copy()

        combined_values = pd.concat([df_fact_sales_order['agreed_payment_date'], df_fact_sales_order['agreed_delivery_date']])
        new_values = combined_values[~combined_values.isin(dim_date['created_date'])]
        dim_date = pd.concat([dim_date, pd.DataFrame({'created_date': new_values})], ignore_index=True)
        dim_date = dim_date.rename(columns = {'created_date': "date_id"})

        print(dim_date)
        date_id = pd.to_datetime(dim_date['date_id'])
        dim_date['year'] = pd.DatetimeIndex(date_id).year
        dim_date['month'] = pd.DatetimeIndex(date_id).month
        dim_date['day'] = pd.DatetimeIndex(date_id).day
        dim_date['day_of_week'] = pd.DatetimeIndex(date_id).day_of_week
        dim_date['day_name'] = date_id.dt.day_name()
        dim_date['month_name'] = date_id.dt.month_name()
        dim_date['quarter'] = pd.DatetimeIndex(date_id).quarter
        dim_date.set_index = dim_date['date_id']
        dim_date.name = 'dim_date'

        logger.info("Finishing processing dim_date DataFrame")
        return dim_date

    except Exception as e:
        logger.error(f"Error occured during formating {dim_date}. More info:" + str(e))
        raise e
