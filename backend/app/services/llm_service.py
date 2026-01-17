from langchain_community.llms import Ollama


class LLMService:
    def __init__(self):
        self.llm = Ollama(model="mistral")

    def generate_response(self, prompt: str) -> str:
        return self.llm.invoke(prompt)
