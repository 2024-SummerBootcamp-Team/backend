#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log"

MAX_RETRY_COUNT=15 #health check 최대 시도 횟수


#로그 메시지 기록 함수
#메시지를 받아서 현재 시간과 함께 배포 로그 파일에 기록
log_message() {
    local message=$1
    local TIME_NOW=$(date +%c) #현재 시간
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
        exit 1
    fi
}

# jq 설치 확인 및 설치
if ! command -v jq &> /dev/null; then
    log_message "jq가 설치되어 있지 않습니다. 설치를 진행합니다."
    execute_and_log "sudo yum update -y && sudo yum install -y jq"
fi

# 컨테이너가 없다면 실행할 함수
init_container() {
    log_message "### INITIALIZING CONTAINER ###"
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml up -d --build --scale fastapi-blue=0"
}

# 컨테이너 스위칭 함수
switch_container() {
    local IS_BLUE=$(docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml ps | grep fastapi-blue)
    # IS_BLUE 변수에 fastapi-blue가 없다면
    if [ -z "$IS_BLUE" ]; then
        log_message "### GREEN => BLUE ###"
        execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml up -d --build fastapi-blue"
        BEFORE_COMPOSE_COLOR="green"
        AFTER_COMPOSE_COLOR="blue"

        sleep 30

        health_check "http://127.0.0.1:8001/healthcheck"
        execute_and_log "cp ${PROJECT_ROOT}/nginx/configs/nginx-blue.conf ${PROJECT_ROOT}/nginx/nginx.conf"
        execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml restart nginx"

    else
        log_message "### BLUE => GREEN ###"
        execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml up -d --build fastapi-green"
        BEFORE_COMPOSE_COLOR="blue"
        AFTER_COMPOSE_COLOR="green"

        sleep 30

        health_check "http://127.0.0.1:8000/healthcheck"

        execute_and_log "cp ${PROJECT_ROOT}/nginx/configs/nginx-green.conf ${PROJECT_ROOT}/nginx/nginx.conf"
        execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml restart nginx"
    fi
}

# 헬스 체크 함수
health_check() {
    local RETRIES=0
    local URL=$1
    while [ $RETRIES -lt $MAX_RETRY_COUNT ]; do
        log_message "Checking service at $URL... (attempt: $((RETRIES+1)))"
        sleep 3

        local RESPONSE=$(curl -s "$URL")
        if [ -n "$RESPONSE" ]; then
            local STATUS=$(echo "$RESPONSE" | jq -r '.status')
            if [ "$STATUS" = "ok" ]; then
                log_message "health check success"
                return 0
            fi
        fi

        RETRIES=$((RETRIES+1))
    done;

    log_message "Failed to check service after $MAX_RETRY_COUNT attempts."
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml down fastapi-${AFTER_COMPOSE_COLOR}"
    log_message "### DEPLOY FAILED ###"
    exit 1
}

# 이전 컨테이너 종료 함수
down_container() {
    execute_and_log "docker compose -p ${DOCKER_APP_NAME} -f ${PROJECT_ROOT}/docker-compose-deploy.yml down fastapi-${BEFORE_COMPOSE_COLOR}"
    log_message "### $BEFORE_COMPOSE_COLOR DOWN ###"
}

# 메인 스크립트 실행
log_message "배포 시작"

# docker compose로 실행된 컨테이너 이름이 fastapi가 없으면 초기 설정으로 새로 서버 생성
EXIST_DOCKER_APP=$(docker ps -a | grep $DOCKER_APP_NAME)

if [ -z "$EXIST_DOCKER_APP" ]; then
    log_message "컨테이너가 없습니다. 컨테이너를 생성합니다."
    init_container
else
    log_message "컨테이너가 이미 실행 중 임으로 컨테이너 스위칭을 진행합니다."

    # 현재 실행되는 컨테이너 확인
    execute_and_log "docker ps -a"

    switch_container
fi

# 현재 실행중인 컨테이너 확인
CURRENT_PID=$(docker ps | grep $DOCKER_APP_NAME | awk '{print $1}')
if [ -z "$CURRENT_PID" ]; then
    log_message "실행된 프로세스를 찾을 수 없습니다."
else
    log_message "실행된 프로세스 아이디는 $CURRENT_PID 입니다."
fi

# 이전 컨테이너 종료
down_container

log_message "배포 종료"
log_message "===================== 배포 완료 ====================="
