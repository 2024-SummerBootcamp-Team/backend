#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c)

EXIST_DOCKER_APP=$(docker ps -a | grep $DOCKER_APP_NAME)

log_message() {
    local message=$1
    echo "$TIME_NOW > $message" | tee -a $DEPLOY_LOG
}

execute_and_log() {
    local command=$1
    log_message "실행: $command"
    eval $command >> $DEPLOY_LOG 2>> $ERROR_LOG
    if [ $? -eq 0 ]; then
        log_message "성공: $command"
    else
        log_message "실패: $command"
    fi
}

execute_and_log "docker ps -a"

if [ -z "$EXIST_DOCKER_APP" ]; then
    log_message "docker compose 파일 실행"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
else
    log_message "docker compose 파일 종료"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml down"

    log_message "docker-compose 파일 재실행"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
fi

CURRENT_PID=$(docker ps | grep $DOCKER_APP_NAME | awk '{print $1}')
if [ -z "$CURRENT_PID" ]; then
    log_message "실행된 프로세스를 찾을 수 없습니다."
else
    log_message "실행된 프로세스 아이디는 $CURRENT_PID 입니다."
fi

log_message "배포 종료"
log_message "===================== 배포 완료 ====================="