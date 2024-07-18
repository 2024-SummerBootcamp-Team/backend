from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    trim_messages,
)

llm = ChatOpenAI(model="gpt-3.5-turbo")

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_DBNAME = os.environ.get('DATABASE_DBNAME')


SQLALCHEMY_DATABASE_URL = f'mysql+aiomysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_DBNAME}'


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id=session_id,
                                 connection=SQLALCHEMY_DATABASE_URL,
                                 async_mode=True,
                                 )

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{prompt}"),  # 시스템 메시지를 템플릿에 추가
        MessagesPlaceholder(variable_name="chat_history"), # 메시지 히스토리
        ("human", "{input}")  # 사용자 메시지
    ]
)

# 토큰 제한 트리머 설정
trimmer = trim_messages(
    strategy="last",      # 최근 메시지를 기준으로 토큰 제한
    max_tokens=20,        # 최대 20토큰까지 제한
    token_counter=len,    # 토큰의 길이를 계산, 임시적으로 길이 계산 적용
    include_system=True,  # 시스템 메시지도 포함
)

# 트리밍이 적용된 체인 설정
chain_with_trimming = (
    RunnablePassthrough.assign(chat_history=itemgetter("chat_history") | trimmer)
    | prompt
    | llm
)

# 메시지 히스토리를 포함하여 넣어주는 러너블 생성
runnable_with_history = RunnableWithMessageHistory(
    chain_with_trimming,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
