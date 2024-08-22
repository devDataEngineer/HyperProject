from src.transformlambda.dim_design import create_df_dim_design



import pytest
import pandas.api.types as ptypes
from dfmock import DFMock
from datetime import datetime
import pandas as pd
import datatest as dt



def test_create_df_dim_design_creates_correct_dataframe():
    data = {'design_id':[1,2],
        'created_at': [datetime.now(), datetime.now()],
        'last_updated':[datetime.now(), datetime.now()],
        'design_name' : str,
        'file_location':  str,
        'file_name' : str
                       }
    df = pd.DataFrame(data)
    

    result = create_df_dim_design(df)

    assert 'created_at' not in result.columns
    assert 'last_updated' not in result.columns
    assert 'design_id' in result.columns
    

def test_create_df_dim_design_column_validation():

    data = {'design_id':[1,2],
        'created_at': [datetime.now(), datetime.now()],
        'last_updated':[datetime.now(), datetime.now()],
        'design_name' : str,
        'file_location':  str,
        'file_name' : str
                       }
    df_design = pd.DataFrame(data)

    result = create_df_dim_design(df_design)
    
    dt.validate(
        result.columns,
        {'design_id', 'design_name', 'file_location', 'file_name' },
    )


def test_create_df_dim_design_file_location_column_values_are_of_the_type():
    data = {'design_id':[1,2],
        'created_at': [datetime.now(), datetime.now()],
        'last_updated':[datetime.now(), datetime.now()],
        'design_name' : str,
        'file_location':  str,
        'file_name' : str
                       }
    df_design = pd.DataFrame(data)

    result = create_df_dim_design(df_design)
    
    assert result['design_id'].dtypes == int
    assert pd.api.types.is_string_dtype(result['file_location'].dtype) == True
    assert pd.api.types.is_string_dtype(result['design_name'].dtype) == True
    assert pd.api.types.is_string_dtype(result['file_name'].dtype) == True
    
    
    
    

