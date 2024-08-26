import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

#sales_record_id [SERIAL], created_date
#----------formate dim_date_df data frame----------------------#
def create_df_dim_staff(df_staff: pd.DataFrame, df_department: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info("Started processing fact_sales DataFrame")
        dim_department = df_department
        dim_staff = df_staff
        dim_staff.set_index = dim_staff['staff_id']
        dim_staff = dim_staff.drop(columns=['created_at', 'last_updated'])
        dim_staff = pd.merge(dim_staff, dim_department, on='department_id', how='left')
        dim_staff = dim_staff.drop(columns=['created_at', 'last_updated', 'manager', 'department_id'])
        dim_staff = dim_staff.reindex(columns=['staff_id', 'first_name', 'last_name', 'department_name', 'location', 'email_address'  ])
        dim_staff.name = "dim_staff"
        return dim_staff
    except Exception as e:
        logger.error(f"Error occured during formating {dim_staff.name}. More info:" + str(e))
        raise e
