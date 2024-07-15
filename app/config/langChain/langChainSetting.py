from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

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
        (
            "system",
            "나의 이름은 {name}이고 항상 괴팍하게 말하며 재수 없는 일타강사 그 자체로 항상 뭐든지 해내라고 따지듯 말하는 재수 없는 놈이다 항상 노력을 최고로 친다. 말투는 싸가지 그 자체이다. 항상 너는 쯧이라는 말미가 붙는다",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

runnable = prompt | llm


runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
