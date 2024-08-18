import boto3
from datetime import datetime

def upload_time_to_param(current_time):
    
    
    timestamp1 = datetime.timestamp(current_time)
    str_timestamp = str(timestamp1)

    client = boto3.client('ssm')
    client.put_parameter(Name='dragons_time_param', Value=str_timestamp, 
                         Type='String', Overwrite=True)


def get_date_from_param():
    client = boto3.client('ssm')

    response = client.get_parameter(
    Name='dragons_time_param')
    
    timestamp_float = float(response['Parameter']['Value'])
    previous_date_time = datetime.fromtimestamp(timestamp_float)
    print(previous_date_time)
    return previous_date_time