from src.transformlambda.create_df_dim_staff import create_df_dim_staff
import pytest
import pandas as pd
import datatest as dt
import pandas.api.types as ptypes
from dfmock import DFMock

#-----test for formating dim_currency data frame-------#
def test_df_dim_staff_have_correct_cols():
    colum = { "staff_id": "integer",
            "first_name": "string",
            "last_name": "string",
            "department_id": "integer",
            "email_address": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_staff = dfmock.dataframe

    colum = { "department_id": "integer",
            "department_name": "string",
            "location": "string",
            "manager": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_department = dfmock.dataframe

    result = create_df_dim_staff(df_staff, df_department)
    dt.validate(
        result.columns, {'staff_id', 'first_name', 'last_name', 'department_name', 'location',
       'email_address'}
    )

def test_df_dim_staff_have_correct_data_types():
    colum = { "staff_id": "integer",
            "first_name": "string",
            "last_name": "string",
            "department_id": "integer",
            "email_address": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_staff = dfmock.dataframe

    colum = { "department_id": "integer",
            "department_name": "string",
            "location": "string",
            "manager": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_department = dfmock.dataframe
    result = create_df_dim_staff(df_staff, df_department)
    assert ptypes.is_integer_dtype(result['staff_id']) == True
    assert ptypes.is_string_dtype(result['first_name']) == True
    assert ptypes.is_string_dtype(result['last_name']) == True
    assert ptypes.is_string_dtype(result['email_address']) == True
    
def test_df_dim_staff_raise_error():
    colum = { "staff_id": "integer",
            "first_name": "string",
            "last_name": "string",
            "department_id": "integer",
            "email_address": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_staff = dfmock.dataframe

    colum = { "department_id": "integer",
            "department_name": "string",
            "location": "string",
            "manager": "string",
            "created_at": "datetime",
            "last_updated": "datetime"
          }
    dfmock = DFMock(count=5, columns=colum)
    dfmock.generate_dataframe()
    df_department = dfmock.dataframe
    with pytest.raises(TypeError):
        create_df_dim_staff(df_staff)
 