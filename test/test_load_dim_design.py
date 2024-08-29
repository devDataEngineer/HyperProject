from src.loadlambda.load_dim_design import load_dim_design_to_warehouse
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch
from datetime import datetime

@patch('src.loadlambda.load_dim_design.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_load_dim_design_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    data = {
        'design_id':[1,2,3,4],
        'design_name':['name1','name2','name3','name4'],
        'file_location': ['loc1','loc2', 'loc3','loc4'],
        'file_name': ['file one','file two','file three','file four']
        }
   
    df = pd.DataFrame(data)
    load_dim_design_to_warehouse(df)
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor
     # Act
    load_dim_design_to_warehouse(df)
    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_dim_design.warehouse_connection")
def test_successful_insert_four_currency_data(mock_warehouse_connection):
   
     # Arrange
    data = {
        'design_id':[1,2,3,4],
        'design_name':['name1','name2','name3','name4'],
        'file_location': ['loc1','loc2', 'loc3','loc4'],
        'file_name': ['file one','file two','file three','file four']
        }
    df = pd.DataFrame(data)
    load_dim_design_to_warehouse(df)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 4