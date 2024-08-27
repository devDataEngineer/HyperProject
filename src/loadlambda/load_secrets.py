import boto3
from botocore.exceptions import ClientError
import json

def get_warehouse_secret(name_secret="Data_Warehouse_Credentials"):

    secret_name = name_secret
    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        json_secret = get_secret_value_response['SecretString'] 
        warehouse_secret = json.loads(json_secret)
        return warehouse_secret 
    except ClientError as e:
        raise e
    

