import app.config.envSetting
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
import os

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_DBNAME = os.environ.get('DATABASE_DBNAME')


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_DBNAME}'


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id=session_id, connection_string=SQLALCHEMY_DATABASE_URL)


runnable_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history,
)

# runnable_with_history.invoke(
#     [HumanMessage(content="안녕하세요 저의 이름은 강남이 입니다.")],
#     config={"configurable": {"session_id": "1"}},
# )

runnable_with_history.invoke(
    [HumanMessage(content="hi - im bob!")],
    config={"configurable": {"session_id": "1"}},
)

runnable_with_history.invoke(
    [HumanMessage(content="whats my name?")],
    config={"configurable": {"session_id": "1"}},
)

runnable_with_history.invoke(
    [HumanMessage(content="whats my name?")],
    config={"configurable": {"session_id": "1a"}},
)