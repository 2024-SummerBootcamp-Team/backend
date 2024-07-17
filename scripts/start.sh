#!/usr/bin/env bash

PROJECT_ROOT="/home/ec2-user/app"
DOCKER_APP_NAME="teamh-backend"

APP_LOG="$PROJECT_ROOT/application.log"
ERROR_LOG="$PROJECT_ROOT/error.log"
DEPLOY_LOG="$PROJECT_ROOT/deploy.log" #배포 로그

TIME_NOW=$(date +%c) #현재 시간

BLUE_DOCKER_COMPOSE_FILE_NAME="docker-compose.blue"
GREEN_DOCKER_COMPOSE_FILE_NAME="docker-compose.green"

CONTAINER_SETUP_DELAY_SECOND=10 #컨테이너 실행 지연 시간
MAX_RETRY_COUNT=15 #health check 최대 시도 횟수
RETRY_DELAY_SECOND=2 #지연 시간

#EXIST_DOCKER_APP=$(docker ps -a | grep $DOCKER_APP_NAME) #teamh-backend라는 이름을 가진 애플리케이션이 있는지 확인

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

# Health Check 함수
health_check() {
    local REQUEST_URL=$1
    local RETRY_COUNT=0
    while [ $RETRY_COUNT -lt $MAX_RETRY_COUNT ]; do
        log_message "상태 검사 ( $REQUEST_URL )  ...  $(( RETRY_COUNT + 1 ))"
        sleep $RETRY_DELAY_SECOND
        REQUEST=$(curl -o /dev/null -s -w "%{http_code}\n" $REQUEST_URL)
        if [ "$REQUEST" -eq 200 ]; then
            log_message "상태 검사 성공"
            return 0
        fi
        RETRY_COUNT=$(( RETRY_COUNT + 1 ))
    done
    return 1
}

# 현재 실행 중인 컨테이너 확인
EXIST_DOCKER_APP=$(docker ps -a | grep $DOCKER_APP_NAME)

if [ "$(docker ps -q -f name=${DOCKER_APP_NAME}-blue)" ]; then #blue 컨테이너가 실행 중인지 확인, 실행 중이면 green 배포, green 환경이 정상적으로 동작하면 nginx 설정 업데이트 하고 blue 환경 종료
    log_message "blue >> green"
    execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-green -f ${PROJECT_ROOT}/${GREEN_DOCKER_COMPOSE_FILE_NAME}.yml up -d --build"
    log_message "${CONTAINER_SETUP_DELAY_SECOND}초 대기"
    sleep $CONTAINER_SETUP_DELAY_SECOND
    if health_check "$GREEN_SERVER_URL$HEALTH_END_POINT"; then
        log_message "green 배포 성공"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-blue -f ${PROJECT_ROOT}/${BLUE_DOCKER_COMPOSE_FILE_NAME}.yml down"
    else
        log_message "green 배포 실패"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-green -f ${PROJECT_ROOT}/${GREEN_DOCKER_COMPOSE_FILE_NAME}.yml down"
        exit 1
    fi
else
    log_message "green >> blue"
    execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-blue -f ${PROJECT_ROOT}/${BLUE_DOCKER_COMPOSE_FILE_NAME}.yml up -d --build"
    log_message "${CONTAINER_SETUP_DELAY_SECOND}초 대기"
    sleep $CONTAINER_SETUP_DELAY_SECOND
    if health_check "$BLUE_SERVER_URL$HEALTH_END_POINT"; then
        log_message "blue 배포 성공"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-green -f ${PROJECT_ROOT}/${GREEN_DOCKER_COMPOSE_FILE_NAME}.yml down"
    else
        log_message "blue 배포 실패"
        execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-blue -f ${PROJECT_ROOT}/${BLUE_DOCKER_COMPOSE_FILE_NAME}.yml down"
        exit 1
    fi
fi


#execute_and_log "docker ps -a"

##현재 Docker 상태 확인하는 명령어를 실행하고 그 결과를 로그에 기록
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

## 현재 버전 중지
#log_message "현재 버전 중지: ${CURRENT_VERSION}"
#execute_and_log "docker-compose -p ${DOCKER_APP_NAME}-${CURRENT_VERSION} -f ${DOCKER_COMPOSE_FILE} down"

#실행 중인 Docker 컨테이너 확인
CURRENT_PID=$(docker ps | grep $DOCKER_APP_NAME | awk '{print $1}')
if [ -z "$CURRENT_PID" ]; then
    log_message "실행된 프로세스를 찾을 수 없습니다."
else
    log_message "실행된 프로세스 아이디는 $CURRENT_PID 입니다."
fi

log_message "배포 종료"
log_message "===================== 배포 완료 ====================="