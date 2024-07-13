# LangSmith 설정 (가상의 설정 예시)
class LangSmith:
    def __init__(self):
        self.token_usage = 0
        self.chat_history = []

    def record_usage(self, tokens):
        self.token_usage += tokens

    def log_chat(self, message):
        self.chat_history.append(message)

    def debug_info(self):
        print("Total tokens used:", self.token_usage)
        print("Chat history:", self.chat_history)


# LangSmith 인스턴스 생성
langsmith = LangSmith()


# 응답 생성 시 LangSmith 사용
def generate_response_with_langsmith(prompt, model, tokenizer, max_length=150, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 토큰 사용량 기록
    langsmith.record_usage(len(outputs[0]))

    # 채팅 기록 저장
    langsmith.log_chat(response.strip())

    return response.strip()


# 기존 응답 생성 함수를 교체
class LocalLLMChainWithLangSmith(LocalLLMChain):
    def run(self, **kwargs):
        prompt = self.prompt_template.format(**kwargs)
        return generate_response_with_langsmith(prompt, self.model, self.tokenizer)


llm_chain1 = LocalLLMChainWithLangSmith(model, tokenizer, prompt_template1)
llm_chain2 = LocalLLMChainWithLangSmith(model, tokenizer, prompt_template2)
llm_chain3 = LocalLLMChainWithLangSmith(model, tokenizer, prompt_template3)
