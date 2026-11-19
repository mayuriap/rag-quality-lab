"""Try the retriever on its own, before any LLM is involved.

Run:  python -m app.search "How much is a CHAPS payment?"
"""

import sys

from langchain_chroma import Chroma

from app import config


def get_vectorstore(embeddings=None) -> Chroma:
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings or config.get_embeddings(),
        persist_directory=str(config.VECTORSTORE_DIR),
    )


def main() -> None:
    question = " ".join(sys.argv[1:]) or "How much is a CHAPS payment?"
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(question, k=config.TOP_K)

    print(f"\nQuestion: {question}\n")
    for rank, (chunk, distance) in enumerate(results, start=1):
        preview = chunk.page_content.replace("\n", " ")[:90]
        print(f"{rank}. {chunk.metadata['chunk_id']:<32} distance={distance:.3f}")
        print(f"   {preview}...\n")


if __name__ == "__main__":
    main()