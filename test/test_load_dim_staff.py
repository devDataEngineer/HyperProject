from src.loadlambda.load_dim_staff import load_dim_staff_to_warehouse
from dfmock import DFMock
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch
from dfmock import DFMock

@patch('src.loadlambda.load_dim_staff.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_load_dim_staff_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    colum = { "staff_id": "integer",
            "first_name": "string",
            "last_name": "string",
            "department_name": "string",
            "location": "string",
            "email_address": "string"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

     # Act
    load_dim_staff_to_warehouse(df)

    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_dim_staff.warehouse_connection")
def test_successful_insert_five_staff_data(mock_warehouse_connection):
   
     # Arrange
    colum = { "staff_id": "integer",
            "first_name": "string",
            "last_name": "string",
            "department_name": "string",
            "location": "string",
            "email_address": "string"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    load_dim_staff_to_warehouse(df)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 5