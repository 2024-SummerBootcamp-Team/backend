#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

TIME_NOW=$(date +%c) #현재 시간

MAX_RETRY_COUNT=15 #health check 최대 시도 횟수


#로그 메시지 기록 함수
#메시지를 받아서 현재 시간과 함께 배포 로그 파일에 기록
log_message() {
    local message=$1
    echo "$TIME_NOW > $message" | tee -a $DEPLOY_LOG
}

#명령어를 실행하고 그 결과를 로그에 기록, 성공 여부도 기록
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

# 컨테이너 스위칭 함수
switch_container() {
    IS_BLUE=$(docker-compose -p "${DOCKER_APP_NAME}-blue" -f ${PROJECT_ROOT}/docker-compose.blue.yml ps | grep Up)
    if [ -z "$IS_BLUE" ]; then
        log_message "### GREEN => BLUE ###"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-blue -f ${PROJECT_ROOT}/docker-compose.blue.yml up -d"
        BEFORE_COMPOSE_COLOR="green"
        AFTER_COMPOSE_COLOR="blue"

        sleep 30

        health_check "http://127.0.0.1:8001/actuator/health"
    else
        log_message "### BLUE => GREEN ###"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-green -f ${PROJECT_ROOT}/docker-compose.green.yml up -d"
        BEFORE_COMPOSE_COLOR="blue"
        AFTER_COMPOSE_COLOR="green"

        sleep 30

        health_check "http://127.0.0.1:8002/actuator/health"
    fi
}

# 헬스 체크 함수
health_check() {
    local RETRIES=0
    local URL=$1
    while [ $RETRIES -lt $MAX_RETRY_COUNT ]; do
        log_message "Checking service at $URL... (attempt: $((RETRIES+1)))"
        sleep 3

        RESPONSE=$(curl -s "$URL")
        if [ -n "$RESPONSE" ]; then
            STATUS=$(echo "$RESPONSE" | jq -r '.status')
            if [ "$STATUS" = "UP" ]; then
                log_message "health check success"
                return 0
            fi
        fi

        RETRIES=$((RETRIES+1))
    done;

    log_message "Failed to check service after $MAX_RETRY_COUNT attempts."
    execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-${AFTER_COMPOSE_COLOR} -f ${PROJECT_ROOT}/docker-compose.${AFTER_COMPOSE_COLOR}.yml down"
    log_message "### DEPLOY FAILED ###"
    exit 1
}

# 이전 컨테이너 종료 함수
down_container() {
    execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-${BEFORE_COMPOSE_COLOR} -f ${PROJECT_ROOT}/docker-compose.${BEFORE_COMPOSE_COLOR}.yml down"
    log_message "### $BEFORE_COMPOSE_COLOR DOWN ###"
}

#execute_and_log "docker ps -a"
#
#if [ -z "$EXIST_DOCKER_APP" ]; then
#    log_message "docker compose 파일 실행"
#    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
#else
#    log_message "docker compose 파일 종료"
#    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml down"
#
#    log_message "docker-compose 파일 재실행"
#    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose.yml up -d --build"
#fi

# 메인 스크립트 실행
log_message "배포 시작"

execute_and_log "docker ps -a"

switch_containe

CURRENT_PID=$(docker ps | grep $DOCKER_APP_NAME | awk '{print $1}')
if [ -z "$CURRENT_PID" ]; then
    log_message "실행된 프로세스를 찾을 수 없습니다."
else
    log_message "실행된 프로세스 아이디는 $CURRENT_PID 입니다."
fi

down_container

log_message "배포 종료"
log_message "===================== 배포 완료 ====================="