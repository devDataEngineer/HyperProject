import os, pytest, boto3
from moto import mock_aws
from unittest.mock import patch
from datetime import datetime
from src.extractlambda.time_param_funcs import update_time_param
from botocore.exceptions import ClientError

@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture
def aws_client(aws_credentials):
    with mock_aws():
        yield boto3.client('ssm')

def test_returns_tuple_containing_two_datetime_objects(aws_client):
    with patch ("src.extractlambda.time_param_funcs.datetime") as p:
        p.now.return_value = datetime(2005,1,1,0,0,0,111111)
        p.strptime.return_value = datetime(2000,1,1,0,0,0,111111)
        aws_client.put_parameter(
            Name = 'dragons_time_param',
            Value = str(datetime(2000,1,1,0,0,0,111111)),
            Type = 'String',
            Overwrite = True
            )
        result = update_time_param()
        assert isinstance(result, tuple)
        assert result[0] == datetime(2005,1,1,0,0,0,111111)
        assert result[1] == datetime(2000,1,1,0,0,0,111111)

def test_parameter_is_stored(aws_client):
    with patch ("src.extractlambda.time_param_funcs.datetime") as p:
        p.now.return_value = datetime(2000,1,1,0,0,0,111111)
        aws_client.put_parameter(
            Name = 'dragons_time_param',
            Value = str(datetime(2000,1,1,0,0,0,111111)),
            Type = 'String',
            Overwrite = True
            )
        update_time_param()
        result = aws_client.get_parameter(Name = "dragons_time_param")
        assert result['Parameter']['Value'] == "2000-01-01 00:00:00.111111"

def test_paramater_updates_each_invocation(aws_client):
    with patch ("src.extractlambda.time_param_funcs.datetime") as p:
        p.now.side_effect = [
            datetime(1993, 1, 1, 1, 1, 1, 1),
            datetime(1996, 1, 1, 1, 1, 1, 1),
            datetime(1999, 1, 1, 1, 1, 1, 1)
            ]
        p.strptime.side_effect = [
            datetime(1990, 1, 1, 0, 0, 0, 111111),
            datetime(1993, 1, 1, 1, 1, 1, 1),
            datetime(1996, 1, 1, 1, 1, 1, 1)
            ]
        aws_client.put_parameter(
            Name = 'dragons_time_param',
            Value = str(datetime(2000,1,1,0,0,0,111111)),
            Type = 'String',
            Overwrite = True
            )
        result = update_time_param()
        assert result[0] == datetime(1993, 1, 1, 1, 1, 1, 1)
        assert result[1] == datetime(1990, 1, 1, 0, 0, 0, 111111)
        result = update_time_param()
        assert result[0] == datetime(1996, 1, 1, 1, 1, 1, 1)
        assert result[1] == datetime(1993, 1, 1, 1, 1, 1, 1)
        result = update_time_param()
        assert result[0] == datetime(1999, 1, 1, 1, 1, 1, 1)
        assert result[1] == datetime(1996, 1, 1, 1, 1, 1, 1)
        
def test_function_results_in_an_error_if_no_parameter_is_found(aws_client):
    with pytest.raises(ClientError):
        update_time_param()