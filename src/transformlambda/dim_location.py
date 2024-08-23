import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def create_dim_location(df_fact_sales_order, df_dim_address):
    logger.info("Started processing dim_location DataFrame")

    dim_location = df_dim_address
    dim_location['location_id'] = df_fact_sales_order[ "agreed_delivery_location_id"]
    dim_location.set_index = dim_location['location_id']
    dim_location = dim_location.drop(columns=['created_at', 'last_updated','address_id'])
    dim_location.name = "dim_location"

    print(dim_location)
    return dim_location
    