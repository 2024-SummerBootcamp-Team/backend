#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"
DOCKER_COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.yml"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log" #배포 로그

TIME_NOW=$(date +%c) #현재 시간 저장

# 현재 활성화된 애플리케이션 버전 확인
CURRENT_VERSION=$(docker ps --filter "name=${DOCKER_APP_NAME}-blue" -q)
if [ -z "$CURRENT_VERSION" ]; then
    CURRENT_VERSION="green"
    NEW_VERSION="blue"
else
    CURRENT_VERSION="blue"
    NEW_VERSION="green"
fi

#EXIST_DOCKER_APP=$(docker ps -a | grep $DOCKER_APP_NAME) #teamh-backend라는 이름을 가진 애플리케이션이 있는지 확인

#로그 메시지 기록 함수
#메시지를 받아서 현재 시간과 함께 배포 로그 파일에 기록
log_message() {
    local message=$1
    echo "$TIME_NOW > $message" | tee -a $DEPLOY_LOG
}

#명령어를 실행하고 그 결과를 로그에 기록
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

#현재 Docker 상태 확인
execute_and_log "docker ps -a"

log_message "현재 버전은 ${CURRENT_VERSION}입니다. 새로운 버전은 ${NEW_VERSION}입니다."

# 새 버전 배포
log_message "새 버전 배포: ${NEW_VERSION}"
execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-${NEW_VERSION} -f ${DOCKER_COMPOSE_FILE} up -d --build"

# 새로운 버전의 컨테이너 상태 확인
NEW_CONTAINER_ID=$(docker ps --filter "name=${DOCKER_APP_NAME}-${NEW_VERSION}" -q)
if [ -z "$NEW_CONTAINER_ID" ]; then
    log_message "새로운 버전의 컨테이너가 실행되지 않았습니다. 배포 실패."
    exit 1
else
    log_message "새로운 버전의 컨테이너 ID: ${NEW_CONTAINER_ID}"
fi

#현재 Docker 상태 확인하는 명령어를 실행하고 그 결과를 로그에 기록
if [ -z "$EXIST_DOCKER_APP" ]; then
    log_message "docker compose 파일 실행"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
else
    log_message "docker compose 파일 종료"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml down"

    log_message "docker-compose 파일 재실행"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
fi

# 현재 버전 중지
log_message "현재 버전 중지: ${CURRENT_VERSION}"
execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-${CURRENT_VERSION} -f ${DOCKER_COMPOSE_FILE} down"

#실행 중인 Docker 컨테이너 확인
CURRENT_PID=$(docker ps | grep $DOCKER_APP_NAME | awk '{print $1}')
if [ -z "$CURRENT_PID" ]; then
    log_message "실행된 프로세스를 찾을 수 없습니다."
else
    log_message "실행된 프로세스 아이디는 $CURRENT_PID 입니다."
fi

log_message "배포 종료"
log_message "===================== 배포 완료 ====================="