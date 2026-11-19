"""Central configuration: one place for paths and settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
DB_PATH = ROOT_DIR / "data" / "db" / "northbridge.db"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

VECTORSTORE_DIR = ROOT_DIR / "vectorstore"
COLLECTION_NAME = "northbridge_knowledge"

# Embedding model: runs locally, free, no API key needed
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


def get_embeddings():
    from app.embeddings import LocalEmbeddings

    return LocalEmbeddings(model_name=EMBEDDING_MODEL)

TOP_K = int(os.getenv("TOP_K", "4"))


# LLM settings
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))


def get_llm():
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(model=ANTHROPIC_MODEL, max_tokens=MAX_TOKENS)