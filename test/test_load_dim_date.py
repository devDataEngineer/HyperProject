from src.loadlambda.load_dim_date import load_dim_date_to_warehouse
from dfmock import DFMock
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch

@patch('src.loadlambda.load_dim_date.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_load_dim_date_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    test_data = {
        "date_id": ["2024-08-28"],
        "year": [2024],
        "month": [8],
        "day": [28],
        "day_of_week": [1],
        "day_name": ["Wednesday"],
        "month_name": ["August"],
        "quarter": [3]
        }
    test_df = pd.DataFrame(test_data) # df in appropriate format
    
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

     # Act
    load_dim_date_to_warehouse(test_df)

    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_dim_date.warehouse_connection")
def test_successful_insert_one_date_data(mock_warehouse_connection):
   
     # Arrange
    test_data = {
        "date_id": ["2024-08-28"],
        "year": [2024],
        "month": [8],
        "day": [28],
        "day_of_week": [1],
        "day_name": ["Wednesday"],
        "month_name": ["August"],
        "quarter": [3]
        }
    dim_date = pd.DataFrame(test_data) # df in appropriate format
    load_dim_date_to_warehouse(dim_date)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 1