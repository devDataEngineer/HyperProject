from src.transformlambda.create_df_dim_currency import create_df_dim_currency
import pytest
from datetime import datetime
import pandas as pd
import datatest as dt
import pandas.api.types as ptypes

#-----test for formating dim_currency data frame-------#
def test_df_dim_currency_have_correct_cols():
    data = {
        'currency_id':[1,2,3,4],
        'currency_code':['GBP','USD','EUR','CHF'],
        'created_at': [datetime.now(),datetime.now(),datetime.now(),datetime.now()],
        'last_updated':[datetime.now(),datetime.now(),datetime.now(),datetime.now()]
        }
    df = pd.DataFrame(data)
    result = create_df_dim_currency(df)
    dt.validate(
        result.columns, {'currency_id', 'currency_code', 'currency_name'}
    )
    assert "last_updated" not in result.columns
    assert "currency_id" in result.columns

def test_df_dim_currency_cols_have_correct_data_type():
    data = {'currency_id':[1,2,3,4],
        'currency_code':['GBP','USD','EUR','CHF'],
        'created_at': [datetime.now(),datetime.now(),datetime.now(),datetime.now()],
        'last_updated':[datetime.now(),datetime.now(),datetime.now(),datetime.now()]
                       }
    df = pd.DataFrame(data)
    result = create_df_dim_currency(df)
    dt.validate(
        result.columns, {'currency_id', 'currency_code', 'currency_name'}
    )
    assert ptypes.is_string_dtype(result['currency_code']) == True
    assert ptypes.is_integer_dtype(result['currency_id']) == True

def test_df_dim_currency_raise_error():
    data = {'currency_id':[1,2,3,4],
        'currency_code':['GBP','USD','EUR','AFG'],
        'created_at': [datetime.now(),datetime.now(),datetime.now(),datetime.now()],
        'last_updated':[datetime.now(),datetime.now(),datetime.now(),datetime.now()]
                       }
    df = pd.DataFrame(data)
    with pytest.raises(KeyError):
        create_df_dim_currency(df)
    