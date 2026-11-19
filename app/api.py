"""FastAPI service exposing the Northbridge assistant over HTTP.

Run:   uvicorn app.api:app --reload
Docs:  http://127.0.0.1:8000/docs
"""

import time
from functools import lru_cache

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from app.rag import RagAssistant

app = FastAPI(title="Northbridge Bank Assistant", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, examples=["What is the overdraft interest rate?"])


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    latency_ms: int


@lru_cache
def get_assistant() -> RagAssistant:
    """Create the assistant once and reuse it for every request."""
    return RagAssistant()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, assistant: RagAssistant = Depends(get_assistant)) -> AskResponse:
    start = time.perf_counter()
    result = assistant.ask(request.question)
    latency_ms = int((time.perf_counter() - start) * 1000)
    return AskResponse(answer=result["answer"], sources=result["sources"], latency_ms=latency_ms)