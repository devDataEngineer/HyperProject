from src.transformlambda.dim_counterparty import create_df_dim_counterparty
from datetime import datetime
import pandas as pd
import datatest as dt
import pandas.api.types as ptypes
import pytest

def test_create_df_counterparty_column_validation():

    data_address =  {
  'address_id': [1,2], 
  'address_line_1': str,
  'address_line_2': str,
  'district': str,
  'city': str,
  'postal_code': str,
  'country': str,
  'phone': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}

    df_address = pd.DataFrame(data_address)

    data_counterparty = {
  'counterparty_id': [1,2],
  'counterparty_legal_name': str,
  'legal_address_id':[1,2],
  'commercial_contact': str,
  'delivery_contact': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}
    df_counterparty = pd.DataFrame(data_counterparty)

    result = create_df_dim_counterparty(df_counterparty,df_address)
    
    dt.validate(
        result.columns,
        {'counterparty_id','counterparty_legal_name',"counterparty_legal_address_line_1",
         "counterparty_legal_address_line_2","counterparty_legal_district", "counterparty_legal_city",
         "counterparty_legal_postal_code", "counterparty_legal_country","counterparty_legal_phone_number"}
    )

def test_create_df_counterparty_correctly_drops_and_renames_columns():

    data_address =  {
  'address_id': [1,2], 
  'address_line_1': str,
  'address_line_2': str,
  'district': str,
  'city': str,
  'postal_code': str,
  'country': str,
  'phone': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}

    df_address = pd.DataFrame(data_address)

    data_counterparty = {
  'counterparty_id': [1,2],
  'counterparty_legal_name': str,
  'legal_address_id': [1,2],
  'commercial_contact': str,
  'delivery_contact': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}
    df_counterparty = pd.DataFrame(data_counterparty)

    result = create_df_dim_counterparty(df_counterparty,df_address)
    
    assert 'created_at' not in result.columns
    assert 'last_updated' not in result.columns
    assert "address_line_1" not in result.columns
    assert "counterparty_legal_address_line_1" in result.columns
    assert "address_line_2" not in result.columns
    assert "counterparty_legal_address_line_2" in result.columns


def test_create_df_counterparty_returns_correct_data_types():

     data_address =  {
  'address_id' : [1,2], 
  'address_line_1':str,
  'address_line_2': str,
  'district' : str,
  'city': str,
  'postal_code':str,
  'country' :str,
  'phone': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}

     df_address = pd.DataFrame(data_address)

     data_counterparty = {
  'counterparty_id : [1,2],
  'counterparty_legal_name': str,
  'legal_address_id': [1,2] ,
  'commercial_contact': str ,
  'delivery_contact': str ,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}
     df_counterparty = pd.DataFrame(data_counterparty)

     result = create_df_dim_counterparty(df_counterparty,df_address)

     assert result['counterparty_id'].dtypes == int
     assert pd.api.types.is_string_dtype(result['counterparty_legal_name'].dtype) == True
     assert pd.api.types.is_string_dtype(result["counterparty_legal_address_line_1"].dtype) == True
     assert pd.api.types.is_string_dtype(result["counterparty_legal_address_line_2"].dtype) == True
     assert pd.api.types.is_string_dtype(result["counterparty_legal_city"].dtype) == True
    
    
def test_create_df_counterparty_raises_error():
     data_counterparty = {
  'counterparty_id': [1,2],
  'counterparty_legal_name': str,
  'legal_address_id': [1,2],
  'commercial_contact': str,
  'delivery_contact': str,
  'created_at':datetime.now(),
  'last_updated': datetime.now()
}
     df_counterparty = pd.DataFrame(data_counterparty)
     with pytest.raises( TypeError):
        create_df_dim_counterparty(df_counterparty)
