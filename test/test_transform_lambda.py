from src.transform_lambda.transform_lambda import get_data, create_df_dim_currency, create_df_dim_date, create_df_fact_sales_order
from moto import mock_aws
import pytest
import boto3
import os
from botocore.exceptions import ClientError
from dfmock import DFMock
from datetime import datetime
import pandas as pd
import datatest as dt

    
#-----test for formating dim_currency data frame-------#
def test_df_dim_currency():
    data = {'currency_id':[1,2,3,4],
        'currency_code':['GBP','USD','EUR','CHF'],
        'created_at': [datetime.now(),datetime.now(),datetime.now(),datetime.now()],
        'last_update':[datetime.now(),datetime.now(),datetime.now(),datetime.now()]
                       }
    df = pd.DataFrame(data)
    result = create_df_dim_currency(df)
    assert "last_update" not in result.columns
    assert "currency_id" in result.columns


#-----test for formating dim_date data frame-------#
def test_df_dim_date():
    data = { 
        'created_date':[datetime.now()],
        'name': "abcde"
    }
    df = pd.DataFrame(data)
    result = create_df_dim_date(df)
    dt.validate(
        result.columns, {'date_id', 'year','month','day','day_of_week','day_name','month_name','quarter'}
    )
    assert 'created_date' not in result.columns

#-----test for formating fact_sales data frame-------#

def test_fact_sales_order_data():
    colum = { "sales_order_id": "integer",
            "created_at": "datetime",
            "last_updated": "datetime",
            "design_id": "integer",
            "staff_id": "integer",
            "counterparty_id": "integer",
            "units_sold": "integer",
            "unit_price": "integer",
            "currency_id": "integer",
            "agreed_delivery_date": "datetime",
            "agreed_payment_date": "datetime",
            "agreed_delivery_location_id": "integer"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    my_mocked_dataframe = dfmock.dataframe
    result = create_df_fact_sales_order(my_mocked_dataframe) 
    dt.validate(
        result.columns, {'sales_record_id','sales_order_id', 'created_date', 'created_time', 'last_updated_date',
       'last_updated_time', 'sales_staff_id', 'counterparty_id', 'units_sold',
       'unit_price', 'currency_id', 'design_id', 'agreed_payment_date',
       'agreed_delivery_date', 'agreed_delivery_location_id'}
    )




