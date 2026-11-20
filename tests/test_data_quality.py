import pytest

from app import config
from app.ingest import split_documents
from app.loaders import load_policy_documents


def test_every_policy_file_produces_chunks():
    docs = load_policy_documents()
    assert len(docs) == len(list(config.RAW_DATA_DIR.glob("*.md")))
    for doc in docs:
        chunks = split_documents([doc])
        assert len(chunks) >= 1, f"{doc.metadata['source']} produced 0 chunks"


@pytest.mark.parametrize("content", ["", "   \n\n  "])
def test_empty_policy_file_is_rejected(tmp_path, monkeypatch, content):
    (tmp_path / "empty.md").write_text(content, encoding="utf-8")
    monkeypatch.setattr(config, "RAW_DATA_DIR", tmp_path)
    with pytest.raises(ValueError):
        load_policy_documents()