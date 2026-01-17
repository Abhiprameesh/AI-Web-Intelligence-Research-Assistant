from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import LLMService
from app.services.scraping_service import ScrapingService
from app.services.nlp_service import NLPCleaningService

app = FastAPI()

llm_service = LLMService()
scraping_service = ScrapingService()
nlp_service = NLPCleaningService()


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

@app.post("/scrape-clean", tags=["Scraping + NLP"])
def scrape_and_clean(request: ScrapeRequest):
    raw_text = scraping_service.scrape_text(request.url)
    clean_text = nlp_service.clean_text(raw_text)

    return {
        "url": request.url,
        "raw_length": len(raw_text),
        "clean_length": len(clean_text),
        "preview": clean_text[:500]
    }
