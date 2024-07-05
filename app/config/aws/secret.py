import boto3
from botocore.exceptions import ClientError
from functools import lru_cache


@lru_cache
def get_secret():
    secret_name = "teamh-secret"
    region_name = "ap-northeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret = get_secret_value_response['SecretString']
    except ClientError as e:
        raise e

    return secret


