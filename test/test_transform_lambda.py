from src.transform_lambda.transform_lambda import get_data, create_df_dim_currency, create_df_dim_date
from moto import mock_aws
import pytest
import boto3
import os
from botocore.exceptions import ClientError
from dfmock import DFMock
from datetime import datetime
import pandas as pd
import datatest as dt

@pytest.fixture
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

BUCKET1 ="Ingestion_bucket"
BUCKET2 = 'Transform_bucket'
KEY = "TEST_KEY"
CONTENT = '''[{"id":1,"first_name":"Reinaldo","last_name":"Pinchbeck","email":"rpinchbeck0@alexa.com","gender":"Male","ip_address":"237.188.238.35"},
{"id":2,"first_name":"Joshuah","last_name":"Reyes","email":"jreyes1@taobao.com","gender":"Male","ip_address":"242.77.75.252"}]'''
 

@pytest.fixture
def s3_client(aws_creds):
    with mock_aws():
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=BUCKET1, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
        yield s3_client

@pytest.fixture
def resource_client(aws_cred):
    with mock_aws():
        s3_resource = boto3.resource("s3")



def test_get_data_func_get_file_from_ingestion(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
    result = get_data(f'S3://Ingestion_bucket/{KEY}.json') 
    result_body = result['Body'].read().decode('utf-8')
    assert result_body == CONTENT
    assert result['ResponseMetadata']['HTTPStatusCode'] == 200

def test_get_data_empty_file(s3_client):
    file_path = 'empty_file.json'
    file_content = b''  # Empty content
    s3_client.put_object(Bucket=BUCKET1, Key=file_path, Body=file_content)
    result = get_data(file_path)
    assert result['Body'].read() == file_content
    assert result['ContentLength'] == 0
    assert result['ResponseMetadata']['HTTPStatusCode'] == 200

# @pytest.mark.skip("need Mick to help us")
def test_get_data_from_ingestion_bucket_lambda_when_bucket_is_empy(s3_client):
    
    with pytest.raises(ClientError) as excinfo:
        get_data("file_path")



# #--------------test for convert function------------------#

# def test_convert_json_to_df(s3_client):
#     s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
#     json_file = get_data(f'{KEY}.json')
#     convert_json_to_df(json_file)
    
#-----test for formating dim_currency data frame-------#
def test_df_dim_currency(s3_client):
    # columns = { "currency_id":"integer",
    #            "currency_code": "string",
    #            "created_at": "datetime",
    #         "last_update":"datetime"
    #       }
    # dfmock = DFMock(count=5, columns=columns)
    # dfmock.generate_dataframe()
    # my_mocked_dataframe = dfmock.dataframe
    data = {'currency_id':[1,2,3,4],
        'currency_code':['GBP','USD','EUR','CHF'],
        'created_at': [datetime.now(),datetime.now(),datetime.now(),datetime.now()],
        'last_update':[datetime.now(),datetime.now(),datetime.now(),datetime.now()]
                       }
    df = pd.DataFrame(data)
    result = create_df_dim_currency(df)
    assert "last_update" not in result.columns
    assert "currency_id" in result.columns


#-----test for formating dim_date data frame-------#
def test_df_dim_date(s3_client):
    data = { 
        'created_date':[datetime.now()]
    }
    df = pd.DataFrame(data)
    result = create_df_dim_date(df)
    dt.validate(
        result.columns, {'date_id', 'year','month','day','day_of_week','day_name','month_name','quarter'}
    )
    assert 'created_date' not in result.columns



