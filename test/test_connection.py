import pytest
import os
import json
import boto3
from moto import mock_aws
from src.extractlambda.connection import db_connection

@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture
def aws_client(aws_credentials):
    with mock_aws():
        yield boto3.client('secretsmanager')

# def test_connection_to_DB_is_established(aws_client):
#     mock_secret_name = 'Tote_Db_Credentials'
#     mock_username = 'mock_user'
#     mock_password = 'mock_password'
#     mock_db = 'mock_db'
#     mock_host = 'mock_host'
#     mock_port = '5432'
#     aws_client.create_secret(Name=mock_secret_name, SecretString=json.dumps({'username':mock_username, 'password':mock_password, 'dbname':mock_db, 'host':mock_host, 'port':mock_port}))

#     conn1=db_connection()
#     result = conn1.run("Select * FROM design;")
#     assert result