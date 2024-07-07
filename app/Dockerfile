# Python 3.10 이미지 사용
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# AWS CLI 설치
RUN apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# 필요한 패키지 설치
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 애플리케이션 코드 복사
COPY ./ /app/

# 포트 오픈
EXPOSE 80

# fastapi 서버 실행
CMD ["fastapi", "run", "main.py", "--port", "80"]
