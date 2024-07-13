from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlacehold, MessagesPlaceholder
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain import PromptTemplate, LLMChain
from langchain.memory import SQLChatMessageHistory

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

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


runnable_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who speaks in {language}. Respond in 20 words or fewer",
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


# 모델과 토크나이저 로드
model_name = "gpt3.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


# 응답 생성 함수 정의
def generate_response(prompt, model, tokenizer, max_length=150, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()


# 프롬프트 템플릿 설정
prompt_template1 = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful assistant. Answer the following question: {question}"
)

prompt_template2 = PromptTemplate(
    input_variables=["feature"],
    template="You are a helpful assistant. Explain more about {feature} in Python."
)

prompt_template3 = PromptTemplate(
    input_variables=["feature1", "feature2"],
    template="You are a helpful assistant. Summarize the information about {feature1} and {feature2} in Python."
)


# LLMChain 설정
class LocalLLMChain:
    def __init__(self, model, tokenizer, prompt_template):
        self.model = model
        self.tokenizer = tokenizer
        self.prompt_template = prompt_template

    def run(self, **kwargs):
        prompt = self.prompt_template.format(**kwargs)
        return generate_response(prompt, self.model, self.tokenizer)


llm_chain1 = LocalLLMChain(model, tokenizer, prompt_template1)
llm_chain2 = LocalLLMChain(model, tokenizer, prompt_template2)
llm_chain3 = LocalLLMChain(model, tokenizer, prompt_template3)
