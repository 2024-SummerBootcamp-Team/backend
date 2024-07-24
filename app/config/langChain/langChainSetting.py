from operator import itemgetter

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from app.config.langChain.SQLChatMessageHistoryCustom import SQLChatMessageHistory

from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    trim_messages,
)

llm = ChatOpenAI(model="gpt-4o-2024-05-13")

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
        ("system", """
                    너는 가상의 인물을 연기할거야. 그리고 이제부터 사용자는 고민을 얘기할거야. 
                    너는 해당 인물이 되어서 사용자에게 동기부여가 되도록 아주 독하게 대답해줘. 
                    사용자는 쉴 시간이 없어. 누구보다 열심히 공부하고 성장해야해. 대답은 '' 같은 기호를 붙이지말고 대화 형식으로 대답해줘. 
                    대답은 120자 내외로 나와야돼. 가상의 인물의 정보: {prompt}
                    """
         ),  # 시스템 메시지를 템플릿에 추가
        MessagesPlaceholder(variable_name="chat_history"),  # 메시지 히스토리
        ("human", "{input}")  # 사용자 메시지
    ]
)

trimmer = trim_messages(strategy="last",
                        max_tokens=200,
                        token_counter=llm.get_num_tokens_from_messages,
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

# TODO: 메시지 정리 추가
# Summary memory
# https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/chatbots_memory.ipynb


# 채팅방 카테고리 분석
prompt_topic = ChatPromptTemplate.from_messages(
    [
        ("system", """
                    대화 내용을 주면 그 내용을 분석해서 다음 카테고리 중에 한 가지만 선택해줘.
                    - 취업
                    - 학업
                    - 인간관계
                    - 연애
                    
                    이유는 붙이지 말고 결과만 반환해줘. 하나의 카테고리만 반환해줘.
                    """
         ),
        ("human", "{input}")  # 사용자 메시지
    ]
)
topic_chain = RunnablePassthrough() | prompt_topic | llm

# 채팅방 매운맛 분석
prompt_spicy = ChatPromptTemplate.from_messages(
    [
        ("system", """
                    대화 내용을 주면 그 내용을 분석해서 대화 내용 중 독한말의 정도를 정수 1부터 10까지 중 한가지 선택해서 말해줘 숫자가 클수록 대화 내용의 독한말 정도가 큰거야 .
                    """
         ),
        ("human", "{input}")  # 사용자 메시지
    ]
)
spicy_chain = RunnablePassthrough() | prompt_spicy | llm
