"""Ingestion pipeline: load both sources -> split into chunks -> embed -> store in Chroma.

Run:  python -m app.ingest
"""

import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config
from app.loaders import load_all


def split_documents(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    # Give every chunk a stable, readable ID: "<source>::<n>"
    counters: dict[str, int] = {}
    for chunk in chunks:
        source = chunk.metadata["source"]
        counters[source] = counters.get(source, 0) + 1
        chunk.metadata["chunk_id"] = f"{source}::{counters[source]}"
    return chunks


def build_vectorstore(chunks: list[Document], embeddings=None) -> Chroma:
    """Rebuild the vector store from scratch so every run is reproducible."""
    if config.VECTORSTORE_DIR.exists():
        shutil.rmtree(config.VECTORSTORE_DIR)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings or config.get_embeddings(),
        ids=[c.metadata["chunk_id"] for c in chunks],
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.VECTORSTORE_DIR),
    )


def main() -> None:
    docs = load_all()
    chunks = split_documents(docs)
    build_vectorstore(chunks)

    print(f"Loaded {len(docs)} source records -> {len(chunks)} chunks")
    for chunk in chunks:
        print(f"  {chunk.metadata['chunk_id']:<42} {len(chunk.page_content):>4} chars")
    print(f"Vector store saved to: {config.VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()