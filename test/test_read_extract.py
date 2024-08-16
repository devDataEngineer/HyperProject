from src.read_extract import read_table, load_table
import pytest
import os
from moto import mock_aws
import boto3
from datetime import datetime


@pytest.mark.skip("Skip now ")
def test_function_returns_counterparty_table():
    result = read_table("counterparty")
    assert isinstance(result, list)
    assert result[0]['commercial_contact'] == 'Micheal Toy'

@pytest.mark.skip("Skip now ")
def test_function_returns_currency_table():
    result = read_table("currency")
    assert isinstance(result, list)
    assert result[0]['currency_id'] == 1

@pytest.mark.skip("Skip now ")
def test_function_returns_department_table():
    result = read_table("department")
    assert isinstance(result, list)
    assert result[0]['department_name'] == 'Sales'

@pytest.mark.skip("Skip now ")
def test_function_returns_staff_table():
    result = read_table("staff")
    assert isinstance(result, list)
    assert result[0]['department_id'] == 2


@pytest.mark.skip("Skip now ")
def test_function_returns_design_table():
    result = read_table("design")
    assert isinstance(result, list)
    assert result[0]['design_id'] == 8   

@pytest.mark.skip("Skip now ")
def test_function_returns_sales_order_table():
    result = read_table("sales_order")
    assert isinstance(result, list)
    assert result[0]['agreed_delivery_location_id'] == 8   

@pytest.mark.skip("Skip now ")
def test_function_returns_address_table():
    result = read_table("address")
    assert isinstance(result, list)
    assert result[0]['address_line_1'] == '6826 Herzog Via'   

@pytest.mark.skip("Skip now ")
def test_function_returns_payment_table():
    result = read_table("payment")
    assert isinstance(result, list)
    assert result[0]['counterparty_ac_number'] == 31622269      

@pytest.mark.skip("Skip now ")
def test_function_returns_purchase_order_table():
    result = read_table("purchase_order")
    assert isinstance(result, list)
    assert result[0]['agreed_delivery_date'] == '2022-11-09'    

@pytest.mark.skip("Skip now ")
def test_function_returns_payment_type_table():
    result = read_table("payment_type")
    assert isinstance(result, list)
    assert result[0]['payment_type_id'] == 1

@pytest.mark.skip("Skip now ")
def test_function_returns_transaction_table():
    result = read_table("transaction")
    assert isinstance(result, list)
    assert result[0]['purchase_order_id'] == 2                     


@pytest.mark.skip("Skip now ")
def test_function_non_whitelist_string(): 
    with pytest.raises(ValueError):
        read_table("nonexist")
       
# ----- TESTING LOADING FUNCIOTN -------------

@pytest.fixture
def secretsmanager_client(aws_creds):
    with mock_aws():

        sm_client = boto3.client("secretsmanager")
        yield sm_client


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
        # s3_client.create_bucket(Bucket=BUCKET)
        # s3_client.put_object(Bucket=BUCKET, Key=KEY, Body=CONTENT)
        # s3_client.get_objects(Bucket=BUCKET)
        yield s3_client

@pytest.fixture
def resource_client(aws_cred):
    with mock_aws():
        s3_resource = boto3.resource("s3")


def test_load_fun_create_json_file(s3_client):
    fake_data = [{'id': 1, "name": "G"}]
    date_to_compare = datetime(1990, 8, 15, 13, 21, 10)
    date_to_compare2 = datetime(1990, 8, 15, 13, 21, 12)

    db_name = "staff"

    bucket_name = 'team-hyper-accelerated-dragon-bucket-ingestion'
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
    load_table(db_name, fake_data, date_to_compare)
    load_table(db_name, fake_data, date_to_compare2)
    # Verify the file was uploaded correctly
    obj = s3_client.list_objects(Bucket=bucket_name)
    print(obj['Contents'])
    assert obj['Contents'][0]['Key'] == "staff/1990/08/15/13-21-10.json"




