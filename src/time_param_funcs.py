import boto3
from datetime import datetime

def upload_time_to_param():
    
    now = datetime.now()
    timestamp1 = datetime.timestamp(now)
    str_timestamp = str(timestamp1)

    client = boto3.client('ssm')
    response = client.put_parameter(Name='dragons_time_param', Value=str_timestamp, Type='String', Overwrite=True)


def get_date_from_param():
    client = boto3.client('ssm')

    response = client.get_parameter(
    Name='dragons_time_param',
    WithDecryption=True|False)
    
    timestamp_float = float(response['Parameter']['Value'])
    previous_date_time = datetime.fromtimestamp(timestamp_float)
    return previous_date_time  