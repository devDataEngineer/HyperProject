from src.transformlambda.dim_design import create_df_dim_design


from moto import mock_aws
import pytest
import boto3
import os
from botocore.exceptions import ClientError
from dfmock import DFMock
from datetime import datetime
import pandas as pd
import datatest as dt



def test_create_df_dim_design():
    data = {'design_id':[1,2],
        'created_at': [datetime.now(), datetime.now()],
        'last_updated':[datetime.now(), datetime.now()],
        'design_name' : 'string',
        'file_location':  'string',
        'file_name' : 'string'
                       }
    df = pd.DataFrame(data)

    result = create_df_dim_design(df)
    print(result)
    assert 'created_at' not in result.columns
    assert 'last_updated' not in result.columns
    assert 'design_id' in result.columns
    

def test_create_df_dim_design_column_validation():
    data = {'design_id':[1,2],
        'created_at': [datetime.now(), datetime.now()],
        'last_updated':[datetime.now(), datetime.now()],
        'design_name' : 'string',
        'file_location':  'string',
        'file_name' : 'string'
                       }
    df_design = pd.DataFrame(data)

    result = create_df_dim_design(df_design)
    
    dt.validate(
        result.columns,
        {'design_id', 'design_name', 'file_location', 'file_name' },
    )



