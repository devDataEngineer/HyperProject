from src.transformlambda.json_to_panda_func import json_to_panda_df
import pandas as pd
from src.transformlambda.get_data import get_data_from_ingestion_bucket
import pytest
import boto3
import os
from botocore.exceptions import ClientError
from moto import mock_aws

@pytest.fixture
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

BUCKET1 ="team-hyper-accelerated-dragon-bucket-ingestion"
KEY = "TEST_KEY"
CONTENT = '''[{"id":1,"first_name":"Reinaldo","last_name":"Pinchbeck","email":"rpinchbeck0@alexa.com","gender":"Male","ip_address":"237.188.238.35"},
{"id":2,"first_name":"Joshuah","last_name":"Reyes","email":"jreyes1@taobao.com","gender":"Male","ip_address":"242.77.75.252"}]'''
CONTENT2 =  "{}"
CONTENT3 = "hello world"

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

def test_json_obj_from_get_data_converts_to_panda_df(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    assert isinstance(resulting_df, pd.DataFrame)
    

def test_empty_json_as_arg(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT2)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    assert resulting_df == None


def test_non_json_arg(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT3)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    assert resulting_df == None

    
