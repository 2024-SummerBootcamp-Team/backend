#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c)

EXIST_DOCKER_APP = $(docker ps -a | grep $DOCKER_APP_NAME)

# docker-compose 파일 실행
# docker compose가 실행 중이면 종료
if [ -z "EXIST_DOCKER_APP" ]; then

# docker-compose 파일 실행
echo "$TIME_NOW > @PROJECT_ROOT docker-compose 파일 실행" >> $DEPLOY_LOG
docker-compose -p ${DOCKER_APP_NAME} -f docker-compose.yml up -d --build

sleep 10

else

# docker-compose 파일 종료
echo "$TIME_NOW > @PROJECT_ROOT docker-compose 파일 종료" >> $DEPLOY_LOG
docker-compose -p ${DOCKER_APP_NAME} -f docker-compose.yml down

# docker-compose 파일 실행
echo "$TIME_NOW > @PROJECT_ROOT docker-compose 파일 실행" >> $DEPLOY_LOG
docker-compose -p ${DOCKER_APP_NAME} -f docker-compose.yml up -d --build

fi

CURRENT_PID=$(pgrep -f DOCKER_APP_NAME)
echo "$TIME_NOW > 실행된 프로세스 아이디 $CURRENT_PID 입니다." >> $DEPLOY_LOG

echo "$TIME_NOW > 배포 종료" >> $DEPLOY_LOG

echo "===================== 배포 완료 =====================" >> $DEPLOY_LOG

echo >> /home/ec2-user/deploy.log