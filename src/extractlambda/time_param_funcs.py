import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def update_time_param() -> tuple[datetime, datetime]:
    """
    Fetches and updates previous time from AWS SSM
    Returns tuple containing current and previous times (start and end of window)
    """

    current_time = datetime.now()
    previous_time = datetime(1990, 1, 1, 0, 0, 0, 111111)

    try:
        client = boto3.client('ssm')
        response = client.get_parameter(Name = 'dragons_time_param')
        previous_time = datetime.strptime(
            response['Parameter']['Value'],
            '%Y-%m-%d %H:%M:%S.%f'
            )
        client.put_parameter(
                Name = 'dragons_time_param',
                Value = str(current_time),
                Type = 'String',
                Overwrite = True
                )
    
    except ClientError as e: 
        logger.error(f"An error occurred: {e}")
        raise
        
    return current_time, previous_time
