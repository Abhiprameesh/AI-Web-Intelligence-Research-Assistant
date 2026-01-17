from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import LLMService
from app.services.scraping_service import ScrapingService

app = FastAPI()

llm_service = LLMService()
scraping_service = ScrapingService()


class ChatRequest(BaseModel):
    prompt: str


class ScrapeRequest(BaseModel):
    url: str


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


@app.post("/chat", tags=["LLM"])
def chat(request: ChatRequest):
    response = llm_service.generate_response(request.prompt)
    return {"response": response}


@app.post("/scrape", tags=["Scraping"])
def scrape(request: ScrapeRequest):
    text = scraping_service.scrape_text(request.url)
    return {
        "url": request.url,
        "length": len(text),
        "preview": text[:500]
    }
