from src.transform_lambda.create_df_fact_sales_order import create_df_fact_sales_order
import pytest
import boto3
from dfmock import DFMock
from datetime import datetime
import pandas as pd
import datatest as dt
import pandas.api.types as ptypes
from pandas._libs.tslibs.parsing import DateParseError

#-----test for formating fact_sales data frame-------#
def test_fact_sales_order_data_correct_cols():
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


def test_fact_sales_order_data_correcrt_data_type():
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
    assert ptypes.is_integer_dtype(result['sales_record_id']) == True
    assert ptypes.is_datetime64_dtype(result['agreed_payment_date']) == True


def test_fact_sales_order_data_correcrt_data_type():
    colum = { "sales_order_id": "integer",
            "created_at": "string",
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
    with pytest.raises(DateParseError):
        create_df_fact_sales_order(my_mocked_dataframe) 
    