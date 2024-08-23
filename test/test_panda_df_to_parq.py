import pandas as pd
from src.transformlambda.json_to_panda_func import json_to_panda_df
from transformlambda.convert_df_to_pq_bytes import convert_dataframe_to_parquet_bytes
from src.transform_lambda.get_data import get_data_from_ingestion_bucket
from io import BytesIO
import pytest
import boto3
from moto import mock_aws
import os


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
# CONTENT2 =  "{}"
# CONTENT3 = "hello world"

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


def test_convert_df_to_pq_func_returns_bytes(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    resulting_pq = convert_dataframe_to_parquet_bytes(resulting_df)
    assert isinstance(resulting_pq, bytes)


def test_convert_df_to_pq_func_returns_first_par_identity_bytes(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    resulting_pq = convert_dataframe_to_parquet_bytes(resulting_df)
    byte_string = str(bytearray(resulting_pq))
    first_four_bytes = byte_string[10:16]
    assert first_four_bytes == "b'PAR1"
    

def test_convert_df_to_pq_func_returns_last_par_identity_bytes(s3_client):
    s3_client.put_object(Bucket=BUCKET1, Key=f'{KEY}.json', Body=CONTENT)
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    resulting_df = json_to_panda_df(result)
    resulting_pq = convert_dataframe_to_parquet_bytes(resulting_df)
    byte_string = str(bytearray(resulting_pq))
    final_four_bytes = byte_string[-6:-2]
    assert final_four_bytes == 'PAR1'


def test_arg_is_not_df(s3_client):
    result = convert_dataframe_to_parquet_bytes("Not a Panda!")
    assert result == None