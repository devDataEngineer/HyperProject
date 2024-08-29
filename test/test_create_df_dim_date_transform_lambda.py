from src.transformlambda.create_df_dim_date import create_df_dim_date
import pytest
from datetime import datetime
import pandas as pd
import datatest as dt
import pandas.api.types as ptypes
from pandas._libs.tslibs.parsing import DateParseError

#-----test for formating dim_date data frame-------#
def test_df_dim_date_has_correct_cos():
    data = { 
        'created_date':[datetime.now()],
        'agreed_payment_date':[datetime.now()],
        'agreed_delivery_date':[datetime.now()],
        'name': "abcde"
    }
    df = pd.DataFrame(data)
    result = create_df_dim_date(df)
    dt.validate(
        result.columns, {'date_id', 'year','month','day','day_of_week','day_name','month_name','quarter'}
    )
    assert 'created_date' not in result.columns

def test_df_dim_date_has_correct_cols_type():
    data = { 
        'created_date':[datetime.now()],
        'agreed_payment_date':[datetime.now()],
        'agreed_delivery_date':[datetime.now()],
        'name': "abcde"
    }
    df = pd.DataFrame(data)
    result = create_df_dim_date(df)
    assert ptypes.is_datetime64_any_dtype(result['date_id']) == True

def test_df_dim_date_raise_error():
    data = { 
        'created_date':["string"],
        'agreed_payment_date': ['string'],
        'agreed_delivery_date':['string'],

        'name': "abcde"
    }
    df = pd.DataFrame(data)
    with pytest.raises(DateParseError):
        create_df_dim_date(df)

