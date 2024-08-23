from src.transformlambda.dim_location import create_dim_location
from datetime import datetime
import pandas as pd
import datatest as dt
import pandas.api.types 


def test_create_dim_location_creates_correct_columns():
    address_data = {
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
    sales_order_data = {
  'sales_order_id': [1,2],
  'created_at': datetime.now(),
  'last_updated': datetime.now(),
  'design_id': int,
  'staff_id': int,
  'counterparty_id': int,
  'units_sold': int,
  'unit_price': int,
  'currency_id': int,
  'agreed_delivery_date': str,
  'agreed_payment_date': str,
  'agreed_delivery_location_id': int 
}

    
    df_address = pd.DataFrame(address_data)
    df_sales_order_data = pd.DataFrame(sales_order_data)

    result = create_dim_location(df_sales_order_data, df_address)
   
    assert 'location_id' in result.columns
    assert 'created_at' not in result.columns
    assert 'location_id' in result.columns



def test_create_dim_location_column_validation():

    address_data = {
  'address_id': [1,2],
  'address_line_1': str, 
  'address_line_2': str,
  'district': str,
  'city': str ,
  'postal_code': str,
  'country':str,
  'phone': str,
  'created_at': datetime.now(),
  'last_updated': datetime.now()
}
    sales_order_data = {
  'sales_order_id':[1,2],
  'created_at': datetime.now(),
  'last_updated': datetime.now(),
  'design_id': int,
  'staff_id': int,
  'counterparty_id': int,
  'units_sold': int,
  'unit_price': int,
  'currency_id': int,
  'agreed_delivery_date': str,
  'agreed_payment_date': str,
  'agreed_delivery_location_id': int
}

    
    df_address = pd.DataFrame(address_data)
    df_sales_order_data = pd.DataFrame(sales_order_data)

    result = create_dim_location(df_sales_order_data, df_address)
    
    dt.validate(result.columns,{'location_id','address_line_1','address_line_2',
                                'district', 'city', 'postal_code', 'country','phone'}
    )


def test_create_dim_location_column_values_are_of_the_correct_type():
     address_data = {
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
     sales_order_data = {
  'sales_order_id': [1,2],
  'created_at': datetime.now(),
  'last_updated': datetime.now(),
  'design_id': int,
  'staff_id': int,
  'counterparty_id': int,
  'units_sold': int,
  'unit_price': int,
  'currency_id':int,
  'agreed_delivery_date': str,
  'agreed_payment_date': str,
  'agreed_delivery_location_id': 1
}

    
     df_address = pd.DataFrame(address_data)
     df_sales_order_data = pd.DataFrame(sales_order_data)

     result = create_dim_location(df_sales_order_data, df_address)
    

     assert pd.api.types.is_string_dtype(result['country'].dtype) == True

     assert result['location_id'].dtypes == int
     assert pd.api.types.is_string_dtype(result['address_line_1'].dtype) == True
     assert pd.api.types.is_string_dtype(result['address_line_2'].dtype) == True
     assert pd.api.types.is_string_dtype(result['district'].dtype) == True
     assert pd.api.types.is_string_dtype(result['city'].dtype) == True
     assert pd.api.types.is_string_dtype(result['postal_code'].dtype) == True
     assert pd.api.types.is_string_dtype(result['country'].dtype) == True
     assert pd.api.types.is_string_dtype(result['phone'].dtype) == True
