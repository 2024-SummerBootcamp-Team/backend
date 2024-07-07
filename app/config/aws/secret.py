import boto3
from botocore.exceptions import ClientError
from functools import lru_cache

"""
lru_cache를 사용하는 이유
호출 결과가 이미 캐시되어 있으면 함수를 실행하지 않고 캐시 결과를 반환하기 때문에
불필요하게 여러번 호출되는 것을 방지할 수 있다.

get_secret 함수는 AWS Secrets Manager 에서 비밀을 가져오는 함수이다.
비밀을 가져오는 작업은 비용이 발생함으로 최대한 실행을 줄여 호출을 줄인다!
"""
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
        # 해당 시크릿 값을 요청하여 가져온다
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        # 시크릿 값을 가져온다 JSON 형태이지만 SecretString으로 가져온다
        # 따라서 JSON 형태로 변환해야 한다.
        # 다른 정보도 같이 첨부되어 출력됨으로
        secret = get_secret_value_response['SecretString']
    except ClientError as e:
        raise e

        # 시크릿 값을 반환한다
    return secret


