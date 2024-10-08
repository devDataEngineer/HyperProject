import pandas as pd
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#sales_record_id [SERIAL], created_date
#----------formate dim_date_df data frame----------------------#
def create_df_fact_sales_order(df_sales_order: pd.DataFrame) -> pd.DataFrame:
   try: 
      logger.info("Started processing fact_sales DataFrame")
      fact_sales_order = df_sales_order
      fact_sales_order.name = 'fact_sales_order'
      fact_sales_order['created_at'] = pd.to_datetime(fact_sales_order['created_at'], format='mixed')
      fact_sales_order['created_date'] = fact_sales_order['created_at'].dt.date
      fact_sales_order['created_time'] = fact_sales_order['created_at'].dt.time
      fact_sales_order['last_updated'] = pd.to_datetime(fact_sales_order['last_updated'], format='mixed')
      fact_sales_order['last_updated_date'] = fact_sales_order['last_updated'].dt.date     
      fact_sales_order['last_updated_time'] = fact_sales_order['last_updated'].dt.time
      fact_sales_order = fact_sales_order.drop(columns=[ 'created_at', 'last_updated'])
      fact_sales_order = fact_sales_order.rename(columns={"staff_id": "sales_staff_id"})
      fact_sales_order['sales_record_id'] = 1
      start_value = 1
      stop_value = len(fact_sales_order) + 1  # adjust this based on your DataFrame size
      step = 1
      fact_sales_order['sales_record_id'] = np.arange(start_value, stop_value, step)

      fact_sales_order.set_index = fact_sales_order['sales_record_id']
      fact_sales_order = fact_sales_order.reindex(columns=['sales_record_id', 'sales_order_id', 'created_date', 'created_time', 'last_updated_date', 'last_updated_time', 
                                                         'sales_staff_id', 'counterparty_id', 'units_sold', 'unit_price', 'currency_id', 'design_id', 
                                                         'agreed_payment_date', 'agreed_delivery_date', 'agreed_delivery_location_id'])
      logger.info("Finishing processing fact_sales DataFrame")
      return fact_sales_order
   except Exception as e:
      logger.error(f"Error occured during formating {fact_sales_order.name}. More info:" + str(e))
      raise e
   