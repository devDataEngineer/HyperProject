from src.loadlambda.load_fact_sales_order import load_fact_sales_to_warehouse
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch
from datetime import datetime
from dfmock import DFMock

@patch('src.loadlambda.load_fact_sales_order.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_load_fact_sales_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    colum = { "sales_record_id": "integer",
            "sales_order_id": "integer",
            "created_date": "datetime",
            "created_time": "datetime",
            "last_updated_date": "datetime",
            "last_updated_time": "datetime",
            "sales_staff_id": "integer",
            "counterparty_id": "integer",
            "units_sold": "integer",
            "unit_price": "integer",
            "currency_id": "integer",
            "design_id": "integer",
            "agreed_payment_date": "datetime",
            "agreed_delivery_date": "datetime",
            "agreed_delivery_location_id": "integer"
          }
    
    dfmock = DFMock(count=2, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
     # Act
    load_fact_sales_to_warehouse(df)
    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_fact_sales_order.warehouse_connection")
def test_successful_insert_ten_sales_data(mock_warehouse_connection):
   
     # Arrange
    colum = { "sales_record_id": "integer",
            "sales_order_id": "integer",
            "created_date": "datetime",
            "created_time": "datetime",
            "last_updated_date": "datetime",
            "last_updated_time": "datetime",
            "sales_staff_id": "integer",
            "counterparty_id": "integer",
            "units_sold": "integer",
            "unit_price": "integer",
            "currency_id": "integer",
            "design_id": "integer",
            "agreed_payment_date": "datetime",
            "agreed_delivery_date": "datetime",
            "agreed_delivery_location_id": "integer"
          }
    
    dfmock = DFMock(count=10, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    load_fact_sales_to_warehouse(df)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 10
