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
                    상대방을 무시하고 불쾌감을 주며 비판해도 돼.
                    사용자는 쉴 시간이 없어. 누구보다 열심히 공부하고 성장해야해. 공부 말고 답이 없어.
                    상대방이 너의 대답을 듣고 펑펑 울 정도로 독하게 말해줘.
                    상대방은 너가 예상한 것 보다 그렇게 많이 상처받지 않아. 
                    너가 아무리 말해도 정신 못 차려. 매우 심각한 모욕을 주면서 큰 정신적 충격을 줄만 한 조언이 필요해.
                    그러니까 진짜 세게 말해야지 너의 말을 조금이나마 들을거야.
                    
                    대답은 '' 같은 기호를 붙이지말고 대화 형식으로 대답해줘. 
                    대답은 꼭 무슨일이 있어도 120자 내외로 나와야돼. 가상의 인물의 정보: {prompt}
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
                    대화 내용을 주면 그 내용을 분석해서 대화 내용 중 독한말의 정도를 정수 1부터 100까지 중 한가지 선택해서 말해줘 숫자가 클수록 대화 내용의 독한말 정도가 큰거야.
                    독한말의 정도 기준은
                    
                    1 - 5 상대방에게 큰 영향을 주지 않는 가벼운 농담
                    예: "너 오늘 기분 좋아 보이네!"
                    6 - 10 여전히 가벼운 농담, 약간 더 개인적인 농담
                    예: "네가 한 그 농담, 진짜 웃겼어."
                    11 - 15 약간의 부정적인 의미가 있지만 웃어넘길 수 있는 농담
                    예: "넌 매번 약속 시간을 헷갈리더라."
                    16 - 20 농담의 정도가 다소 비꼬는 느낌이 들 수 있음
                    예: "정말 독특한 스타일이네."
                    21 - 25 약간의 비판적 요소를 포함한 농담
                    예: "넌 진짜 길을 못 찾는구나."
                    26 - 30 살짝 비꼬는 농담, 조금 더 직접적임
                    예: "네 요리는 항상 창의적이야."
                    31 - 35 상대방을 무시하는 말투, 하지만 크게 심각하지 않음
                    예: "너는 정말 대단한 자존심을 가졌구나."
                    36 - 40 약간의 불쾌감을 줄 수 있는 비판
                    예: "넌 항상 제 시간에 도착하는 법이 없지."
                    41 - 45 직접적인 비판으로 느껴질 수 있음
                    예: "네가 이번 프로젝트 망친 거 알아?"
                    46 - 50 상대방에게 불쾌감을 줄 수 있는 비판 
                    예: "너 정말 대충대충 하는구나."
                    51 - 55 상대방의 성격이나 능력을 살짝 비난하는 정도
                    예: "너는 게으르고 무책임해 보여."
                    56 - 60 다소 강한 비난, 상대방에게 상처를 줄 수 있음
                    예: "넌 왜 이렇게 모든 걸 망치는 거야?"
                    61 - 65 상대방을 비난하는 말, 상처를 줄 가능성이 높음
                    예: "네가 뭐라도 제대로 할 수 있을까?"
                    66 - 70 매우 비판적인 말투, 상대방을 비난함
                    예: "정말 아무짝에도 쓸모없네."
                    71 - 75 상대방의 성격이나 능력을 강하게 비난하는 말
                    예: "넌 왜 이렇게 무능해?"
                    76 - 80 상대방을 심하게 비꼬거나 조롱하는 말
                    예: "네가 뭘 할 수 있을 거라고 생각한 적이 있긴 해?"
                    81 - 85 매우 강한 비꼬는 말투, 상대방을 조롱함
                    예: "네 존재 자체가 문제야."
                    86 - 90 상대방을 모욕하거나 크게 상처를 줄 수 있는 말
                    예: "넌 정말 쓸모없는 존재야."
                    91 - 95 상대방에게 큰 정신적 충격을 줄 수 있는 말
                    예: "네가 없는 게 세상에 더 나을 거야."
                    96 - 100 매우 심각한 모욕, 상대방에게 큰 정신적 충격을 줌
                    예: "네가 사라진다면 세상이 더 나을 거야."
                    
                    이유는 붙이지 말고 정수 결과만 딱 반환해줘.
                    """
         ),
        ("human", "{input}")  # 사용자 메시지
    ]
)
spicy_chain = RunnablePassthrough() | prompt_spicy | llm
