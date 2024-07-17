from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
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
        ("system", "{prompt}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ]
)


trimmer = trim_messages(
    strategy="last",
    max_tokens=500,
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,
)


runnable_with_history = RunnableWithMessageHistory(
    prompt | trimmer | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
