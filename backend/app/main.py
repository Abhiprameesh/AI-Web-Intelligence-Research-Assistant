from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import LLMService

app = FastAPI()

llm_service = LLMService()


class ChatRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = llm_service.generate_response(request.prompt)
    return {"response": response}
