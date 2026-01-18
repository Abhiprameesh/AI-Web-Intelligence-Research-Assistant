from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import LLMService
from app.services.scraping_service import ScrapingService
from app.services.nlp_service import NLPCleaningService
from app.services.vector_store_service import VectorStoreService


app = FastAPI()

llm_service = LLMService()
scraping_service = ScrapingService()
nlp_service = NLPCleaningService()
vector_store_service = VectorStoreService()


class ChatRequest(BaseModel):
    prompt: str


class ScrapeRequest(BaseModel):
    url: str

class RAGQueryRequest(BaseModel):
    question: str


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

@app.post("/rag-query", tags=["RAG"])
def rag_query(request: RAGQueryRequest):
    context, sources = vector_store_service.retrieve_context(request.question)

    prompt = f"""
You are a research assistant.

Answer the question ONLY using the context provided below.
If the answer is not present in the context, say:
"I don't have enough information from the given sources."

Context:
{context}

Question:
{request.question}

Answer:
"""

    answer = llm_service.generate_response(prompt)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }

