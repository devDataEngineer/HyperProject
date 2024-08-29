from src.extractlambda.db_secrets import get_secret
from botocore.exceptions import ClientError
from moto import mock_aws
import boto3
import pytest
import json
import os

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

def test_get_secret_returns_correct_secret(aws_client):
    result = get_secret()
    assert isinstance(result, dict)
    # assert result['engine'] == 'postgres'

def test_doesnt_reach_client_error_when_provided_correct_Secret_name(aws_client):
    mock_secret_name = 'mock_secret'
    mock_username = 'mock_user'
    mock_password = 'mock_password'
    aws_client.create_secret(Name=mock_secret_name, SecretString=json.dumps({'username':mock_username, 'password':mock_password}))
    result = get_secret(mock_secret_name)
    assert result['username'] == mock_username
    assert result['password'] == mock_password

def test_reaches_client_error_when_provided_invalid_Secret_name(aws_client):
    with pytest.raises(ClientError):
        get_secret("nonsense")