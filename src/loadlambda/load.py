try:
    from src.loadlambda.get_pq_from_bucket import get_pq_from_bucket
    from src.loadlambda.load_dim_date import load_dim_date_to_warehouse
    from src.loadlambda.load_dim_design import load_dim_design_to_warehouse
    from src.loadlambda.load_dim_location import load_dim_location_to_warehouse
    from src.loadlambda.load_fact_sales_order import load_fact_sales_to_warehouse
    from src.loadlambda.load_dim_staff import load_dim_staff_to_warehouse
    from src.loadlambda.load_dim_currency import load_dim_currency_to_warehouse
    from src.loadlambda.load_dim_counterparty import load_dim_counterparty_to_warehouse
except:
    from get_pq_from_bucket import get_pq_from_bucket
    from load_dim_date import load_dim_date_to_warehouse
    from load_dim_design import load_dim_design_to_warehouse
    from load_dim_location import load_dim_location_to_warehouse
    from load_fact_sales_order import load_fact_sales_to_warehouse
    from load_dim_staff import load_dim_staff_to_warehouse
    from load_dim_currency import load_dim_currency_to_warehouse
    from load_dim_counterparty import load_dim_counterparty_to_warehouse
    

import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def get_arguments(event) -> dict:
    df_list = [ 'fact_sales_order', 'dim_staff',
                'dim_location','dim_design', 'dim_date',
                'dim_currency', 'dim_counterparty'
        ]
    
    dfs_with_filepaths = {}

    received_dfs = event.keys()
    if len(received_dfs) == 0:
        logging.error("Lambda invoked with nothing to load")

    for df in received_dfs:
        if df in df_list:
            dfs_with_filepaths[df] = event[df]

    return dfs_with_filepaths


def lambda_handler(event, context):
    logger.info("Load lambda beginning execution")

    logger.info("Retrieving arguments from Transform lambda")
    tables_with_filenames = get_arguments(event) # returns dict

    table_list = list(tables_with_filenames.keys())
    logger.info(f"To be updated: {table_list}")

    tables_with_df = {}

    logger.info(f"Processing parquet files")
    for table in table_list:
        logger.info(f"Retrieving: {table}")
        tables_with_df[table] = get_pq_from_bucket(tables_with_filenames[table])
        logger.info(f"{table} successfully retrieved and converted to dataframe")

    for table in table_list:
        logger.info(f"Uploading {table}...")
        match table:
            case "dim_date":
                load_dim_date_to_warehouse(tables_with_df[table])
            case "dim_design":
                load_dim_design_to_warehouse(tables_with_df[table])
            case "dim_location":
                load_dim_location_to_warehouse(tables_with_df[table])
            case "dim_staff":
                load_dim_staff_to_warehouse(tables_with_df[table])
            case "dim_currency":
                load_dim_currency_to_warehouse(tables_with_df[table])
            case "dim_counterparty":
                load_dim_counterparty_to_warehouse(tables_with_df[table])
        logger.info(f"Upload of {table} complete!")

    if "fact_sales_order" in table_list:
        logger.info("Uploading fact_sales_order...")
        load_fact_sales_to_warehouse(tables_with_df["fact_sales_order"])
        logger.info(f"Upload of fact_sales_order complete!")

        logger.info("End of Load lambda execution")
