from src.loadlambda.get_pq_from_bucket import get_pq_from_bucket
import pytest
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from moto import mock_aws
import io


@pytest.fixture
def mock_s3_resource():
    with mock_aws():
        yield boto3.resource('s3')

def test_get_pq_from_bucket_reads_the_parquet_file(mock_s3_resource, mocker):
    
    bucket_name = 'fake-bucket'
    key = 'fake-file.parquet'
    
    s3 = mock_s3_resource
    s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    
    fake_data = {'column_1': [1, 2, 3], 'column_2': ['a', 'b', 'c']}
    mock_df = pd.DataFrame(fake_data)
    parquet_buffer = io.BytesIO()
    mock_df.to_parquet(parquet_buffer)
    
    s3_object = s3.Object(bucket_name, key)
    s3_object.put(Body=parquet_buffer.getvalue())
    
    mocker.patch('pandas.read_parquet', return_value=mock_df)
    
    result = get_pq_from_bucket(bucket_name, key)
    
    assert isinstance(result, pd.DataFrame)
    assert result is (mock_df)    


def test_get_pq_from_bucket_results_in_error_when_incorrect_bucket_name_passed(mocker):
    mock_s3_client = mocker.Mock()
    mock_s3_client.get_object.side_effect = ClientError(
        {'Error': {'Code': 'NoSuchBucket', 'Message': 'The specified bucket does not exist'}},
        'GetObject'
    )
    mocker.patch('boto3.client', return_value=mock_s3_client)
    # Call the function
    with pytest.raises(ClientError):
        result = get_pq_from_bucket('non-existent-bucket', 'non-existent-key')
    
    # # Assert the result
    # assert result is None
