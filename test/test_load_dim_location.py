from src.loadlambda.load_dim_location import load_dim_location_to_warehouse
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch
from datetime import datetime
from dfmock import DFMock

@patch('src.loadlambda.load_dim_location.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_load_dim_location_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    colum = { "location_id": "integer",
            "address_line_1": "string",
            "address_line_2": "string",
            "district": "string",
            "city": "string",
            "postal_code": "string",
            "country": "string",
            "phone": "string"          }
    dfmock = DFMock(count=10, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
     # Act
    load_dim_location_to_warehouse(df)
    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_dim_location.warehouse_connection")
def test_successful_insert_ten_location_data(mock_warehouse_connection):
   
     # Arrange
    colum = { "location_id": "integer",
            "address_line_1": "string",
            "address_line_2": "string",
            "district": "string",
            "city": "string",
            "postal_code": "string",
            "country": "string",
            "phone": "string"          }
    dfmock = DFMock(count=10, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    load_dim_location_to_warehouse(df)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 10