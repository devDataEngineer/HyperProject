
from src.transformlambda.get_arguments import get_arguments
from moto import mock_aws
import pytest, boto3, os

@pytest.fixture
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    BUCKET = "TEST_BUCKET"
    KEY = "TEST_KEY"
    CONTENT = "TEST_CONTENT"

@pytest.fixture
def lambda_client(aws_creds):
    with mock_aws():
        s3_client = boto3.client("lambda")
        yield s3_client

def test_returns_dict():
    result = get_arguments({})
    assert isinstance(result, dict)

def test_no_arguments_returns_empty_dict():
    result = get_arguments({})
    assert len(result) == 0

def test_return_dict_correlates_with_arguments(lambda_client):
    example_argument = {
        "counterparty": "counterparty/2024/08/20/12-00-00.json",
        "currency": "currency/2024/08/20/12-00-00.json"
        }
    result = get_arguments(example_argument)
    assert "counterparty" in result
    assert "currency" in result
    assert len(result) == 2
    