from src.loadlambda.load_dim_counterparty import load_dim_counterparty_to_warehouse
from dfmock import DFMock
import pandas as pd
from src.loadlambda.load_warehouse_connection import warehouse_connection
from unittest.mock import Mock, patch
from dfmock import DFMock

@patch('src.loadlambda.load_dim_counterparty.warehouse_connection') # patching the warehouse connection so it doesn't connect to real DB
def test_lload_dim_counterparty_to_warehouse_func_is_called_correctly(mock_warehouse_connection):
    # Arrange
    colum = { "counterparty_id": "integer",
            "counterparty_legal_name": "string",
            "counterparty_legal_address_line_1": "string",
            "counterparty_legal_address_line_2": "string",
            "counterparty_legal_district": "string",
            "counterparty_legal_city": "string",
            "counterparty_legal_postal_code": "string",
            "counterparty_legal_country": "string",
            "counterparty_legal_phone_number": "string"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    mock_conn = Mock() # result of warehouse_connection()
    mock_warehouse_connection.return_value = mock_conn
    mock_cursor = Mock() # result of conn.cursor()
    mock_conn.cursor.return_value = mock_cursor

     # Act
    load_dim_counterparty_to_warehouse(df)

    # Assert 
    mock_conn.commit.assert_called_once()

@patch("src.loadlambda.load_dim_counterparty.warehouse_connection")
def test_successful_insert_five_counterparty_data(mock_warehouse_connection):
   
     # Arrange
    colum = { "counterparty_id": "integer",
            "counterparty_legal_name": "string",
            "counterparty_legal_address_line_1": "string",
            "counterparty_legal_address_line_2": "string",
            "counterparty_legal_district": "string",
            "counterparty_legal_city": "string",
            "counterparty_legal_postal_code": "string",
            "counterparty_legal_country": "string",
            "counterparty_legal_phone_number": "string"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df = dfmock.dataframe
    load_dim_counterparty_to_warehouse(df)
    assert mock_warehouse_connection.return_value.cursor.return_value.execute.call_count == 5