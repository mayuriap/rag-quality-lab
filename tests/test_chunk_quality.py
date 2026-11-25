from collections import Counter

import pytest

from app.ingest import split_documents
from app.loaders import load_all

MIN_CHARS = 50


@pytest.fixture(scope="module")
def chunks():
    return split_documents(load_all())




def test_no_empty_chunks(chunks):
    empty = [c.metadata["chunk_id"] for c in chunks if not c.page_content.strip()]
    assert empty == []


def test_no_tiny_chunks(chunks):
    tiny = [(c.metadata["chunk_id"], len(c.page_content.strip()))
            for c in chunks if len(c.page_content.strip()) < MIN_CHARS]
    assert tiny == []


def test_no_duplicate_chunks(chunks):
    
    counts = Counter(c.page_content.strip() for c in chunks)
    duplicates = [text[:40] for text, n in counts.items() if n > 1]
    assert duplicates == []


def test_chunk_ids_are_unique(chunks):
    ids = [c.metadata["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids))