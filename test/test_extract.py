from src.extractlambda.extract import load_table, load_all_tables, read_table, lambda_handler
from src.extractlambda.connection import close_db_connection, db_connection
import pytest
import os
from moto import mock_aws
from unittest.mock import patch
import boto3
from datetime import datetime
from pg8000 import DatabaseError

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
def s3_client(aws_creds):
    with mock_aws():
        s3_client = boto3.client("s3")
        yield s3_client

@pytest.fixture
def ssm_client(aws_creds):
    with mock_aws():
        sm_client = boto3.client("ssm")
        yield sm_client

# @pytest.fixture
# def resource_client(aws_creds):
#     with mock_aws():
#         s3_resource = boto3.resource("s3")


@patch('src.extractlambda.extract.db_connection')
def test_function_returns_correctly_formatted_table(mock_conn):
    mock_conn.return_value.run.return_value = [["a","b","c", "d"],[1, 2, 3, 4]]
    mock_conn.return_value.columns = [{"name": "a"}, {"name": "b"}, {"name": "c"}, {"name": "d"} ]
    result = read_table("counterparty", datetime(2024, 8, 15, 13, 21, 10), datetime(1990, 8, 15, 13, 21, 10))
    assert isinstance(result, list)
    assert result == [{'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'}, {'a': 1, 'b': 2, 'c': 3, 'd': 4}]

def test_function_raises_ValueError_for_non_whitelist_table():
    with pytest.raises(ValueError):
        read_table("nonexist", datetime(2024, 8, 15, 13, 21, 10), datetime(1990, 8, 15, 13, 21, 10))

# @pytest.mark.xfail(reason="This isn't raising DB error - related to finally?")
@patch('src.extractlambda.extract.db_connection')
def test_function_correctly_raises_DatabaseError(mock_conn):
        mock_conn.return_value.run.side_effect = DatabaseError
        with pytest.raises(DatabaseError):
            read_table("department", datetime(2024, 8, 15, 13, 21, 10), datetime(1990, 8, 15, 13, 21, 10))

def test_load_table_create_json_file(s3_client):
    fake_data = [{'id': 1, "name": "G"}]
    date_to_compare = datetime(1990, 8, 15, 13, 21, 10)
    date_to_compare2 = datetime(1990, 8, 15, 13, 21, 12)
    db_name = "staff"
    bucket_name = 'team-hyper-accelerated-dragon-bucket-ingestion'
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
    load_table(db_name, fake_data, date_to_compare)
    load_table(db_name, fake_data, date_to_compare2)
    obj = s3_client.list_objects(Bucket=bucket_name)
    assert obj['Contents'][0]['Key'] == "staff/1990/08/15/13-21-10.json"
    assert obj['Contents'][1]['Key'] == "staff/1990/08/15/13-21-12.json"

def test_load_all_tables_returns_dict(s3_client):
    date_to_compare = datetime(1990, 8, 15, 13, 21, 10)
    date_to_compare2 = datetime(1990, 8, 15, 13, 21, 12)
    with patch ("src.extractlambda.extract.load_table") as pl:
        with patch ("src.extractlambda.extract.read_table") as pr:
            pr.return_value = [
                {'column1': 'value1', 'column2': 'value2'}, 
                {'column1': 'value3', 'column2': 'value4'}, 
                {'column1': 'value5', 'column2': 'value6'}
                ]
            pl.return_value = None
            assert isinstance(load_all_tables(date_to_compare, date_to_compare2), dict)


def test_lambda_handler_returns_dict(s3_client, ssm_client):
    with patch ("src.extractlambda.extract.load_all_tables") as p:
        p.return_value = {
            'counterparty': "link", 'currency': "link", 'department': "link"
                            }
        bucket_name = 'team-hyper-accelerated-dragon-bucket-ingestion'
        # s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
        ssm_client.put_parameter(
            Name = 'dragons_time_param',
            Value = str(datetime(2000,1,1,0,0,0,111111)),
            Type = 'String',
            Overwrite = True
            )
        assert isinstance(lambda_handler("", ""), dict)
