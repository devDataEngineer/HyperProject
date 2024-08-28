from src.loadlambda.load_secrets import get_warehouse_secret
from botocore.exceptions import ClientError
from moto import mock_aws
import boto3
import pytest
import json

@pytest.fixture(scope="function")
def aws_credentials():
    pass

@pytest.fixture
def aws_client(aws_credentials):
    with mock_aws():
        yield boto3.client('secretsmanager')

# def test_get_secret_returns_correct_secret():
#     result = get_warehouse_secret()
#     assert isinstance(result, dict)
#     assert result['engine'] == 'postgres'

def test_doesnt_reach_client_error_when_provided_correct_Secret_name(aws_client):
    mock_secret_name = 'mock_secret'
    mock_username = 'mock_user'
    mock_password = 'mock_password'
    aws_client.create_secret(Name=mock_secret_name, SecretString=json.dumps({'username':mock_username, 'password':mock_password}))
    result = get_warehouse_secret(mock_secret_name)
    assert result['username'] == mock_username
    assert result['password'] == mock_password

def test_reaches_client_error_when_provided_invalid_Secret_name(aws_client):
    with pytest.raises(ClientError):
        get_warehouse_secret("nonsense")
