from src.transform_lambda.get_data import get_data_from_ingestion_bucket
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
    result = get_data_from_ingestion_bucket(f's3://team-hyper-accelerated-dragon-bucket-ingestion/{KEY}.json') 
    result_body = result['Body'].read().decode('utf-8')
    assert result_body == CONTENT
    assert result['ResponseMetadata']['HTTPStatusCode'] == 200

def test_get_data_empty_file(s3_client):
    file_path = 'empty_file.json'
    file_content = b''  # Empty content
    s3_client.put_object(Bucket=BUCKET1, Key=file_path, Body=file_content)
    result = get_data_from_ingestion_bucket(file_path)
    assert result['Body'].read() == file_content
    assert result['ContentLength'] == 0
    assert result['ResponseMetadata']['HTTPStatusCode'] == 200

def test_get_data_from_ingestion_bucket_lambda_when_bucket_is_empy(s3_client):
    with pytest.raises(ClientError) as excinfo:
        get_data_from_ingestion_bucket("file_path")


