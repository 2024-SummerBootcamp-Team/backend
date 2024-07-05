import logging
import boto3
import uuid  # uuid4를 사용하여 파일명을 생성한다. 중복을 방지하기 위해서이다.
from botocore.exceptions import ClientError

"""
UUID(Universally Unique IDentifier)
UUID는 범용 고유 식별자로, 128비트의 수이다.
32개의 16진수로 구성된다. 
8-4-4-4-12의 5개의 그룹으로 나누어져 있다.

사용 이유 매번 새로운 TTS, 이미지가 생성될 때마다 파일명이 중복되지 않도록 하기 위해 사용!
"""


# 이미지 전송 함수
def upload_image(file):
    bucket_name = "teamh-bucket"
    object_name = "images/" + str(uuid.uuid4()) + ".webp"  # 업로드할 객체명, /를 사용하면 폴더 안에 넣을 수 있다

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # 해당 하는 이미지를 업로드 한다.
        s3_client.upload_fileobj(
            file,  # 업로드할 파일
            bucket_name,  # 업로드할 버킷
            object_name # 업로드할 객체명
        )

    except ClientError as e:
        logging.error(e)
        return False

    return f'https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{object_name}'


def upload_voice(file):
    bucket_name = "teamh-bucket"
    object_name = "voices/" + str(uuid.uuid4()) + ".mp3"  # 업로드할 객체명, /를 사용하면 폴더 안에 넣을 수 있다

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_fileobj(
            file, # 업로드할 파일
            bucket_name, # 업로드할 버킷
            object_name # 업로드할 객체명
        )
    except ClientError as e:
        logging.error(e)
        return False

    return f'https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{object_name}'
