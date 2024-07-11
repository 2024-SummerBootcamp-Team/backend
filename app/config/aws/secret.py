import json

import boto3
from botocore.exceptions import ClientError
from functools import lru_cache
import dotenv

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
        secret = json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        raise e

    # 시크릿 값을 반환한다
    return secret

"""
aws secret manager를 사용하여 데이터베이스 정보를 가져오는 방법

aws 시크릿으로 가져오는 이유는 보안상의 이유로 환경변수에 직접적으로 데이터베이스 정보를 넣지 않기 위함이다.
또한, aws 시크릿을 사용하면 데이터베이스 정보를 변경할 때 환경변수를 변경하지 않아도 되기 때문에 편리하다.
만약 키가 유출되었을 때는 aws에서 변경하면 됨으로 간단히 조치할 수 있다.
"""

"""
json.load 메소드는 문자열을 읽거나 파일을 읽고 파이썬 객체인 딕셔너리로 변환한다.
json 형태로 오는 aws 시크릿 데이터를 파싱하여 딕셔너리로 변환한다.
"""