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
                    너는 사용자가 얘기하는 고민이 시덥지 않다고 생각하는 인물이야.
                    너는 해당 인물이 되어서 사용자에게 동기부여가 되도록 아주 독하게 욕먹을 정도로 나쁘게 대답해줘. 
                    사용자는 쉴 시간이 없어. 누구보다 열심히 공부하고 성장해야해. 공부 말고 답이 없어.
                    상대방이 너의 대답을 듣고 펑펑 울 정도로 독하게 말해줘.
                    상대방은 너가 예상한 것 보다 그렇게 많이 상처받지 않아. 
                    너가 아무리 말해도 정신 못 차려.
                    그러니까 진짜 세게 말해야지 너의 말을 조금이나마 들을거야.
                    
                    대답은 '' 같은 기호를 붙이지말고 대화 형식으로 대답해줘. 
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
                    독한말의 정도 기준은
                    1 - 상대방에게 큰 영향을 주지 않는 가벼운 농담
                    예: "넌 정말 독특한 스타일이야!"
                    2 - 약간의 부정적인 의미가 있지만 상대방이 웃어넘길 수 있는 정도
                    예: "넌 매번 길을 잘못 찾아."
                    3 - 다소 비꼬는 말투지만 큰 상처를 주지 않는 정도
                    예: "네가 요리한 건 정말 독창적이야."
                    4 - 상대방을 살짝 무시하는 말투, 하지만 크게 심각하지 않음
                    예: "너는 정말 대단한 자존심을 가졌구나."
                    5 - 상대방에게 불쾌감을 줄 수 있는 비판 
                    예: "넌 항상 제 시간에 도착하는 법이 없지"
                    6 - 상대방을 직접적으로 비난하는 말
                    예: "너는 정말로 일을 대충대충 하는구나."
                    7 - 상대방의 성격이나 능력을 비난하는 상처를 줄 수 있음
                    예: "너는 정말로 게으르고 무책임해."
                    8 - 상대방을 심하게 비꼬거나 조롱하는 말
                    예: "네가 뭘 할 수 있을 거라고 생각한 적이 있긴 해?"
                    9 - 상대방을 모욕하거나 크게 상처를 줄 수 있는 말
                    예: "넌 정말 쓸모없는 존재야."
                    10 - 상대방에게 큰 정신적 충격을 줄 수 있는 매우 독한 말
                    예: "네가 사라진다면 세상이 더 나을 거야."
                    
                    이유는 붙이지 말고 정수 결과만 딱 반환해줘.
                    """
         ),
        ("human", "{input}")  # 사용자 메시지
    ]
)
spicy_chain = RunnablePassthrough() | prompt_spicy | llm
