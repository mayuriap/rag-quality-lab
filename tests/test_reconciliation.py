import sqlite3
from datetime import date

import pytest

from app import config
from app.ingest import build_vectorstore, split_documents
from app.loaders import load_all

TODAY = date.today().isoformat()


@pytest.fixture
def store(tmp_path, monkeypatch):
    # Point the build at a temp folder so the real vectorstore is never deleted
    monkeypatch.setattr(config, "VECTORSTORE_DIR", tmp_path / "vs")
    return build_vectorstore(split_documents(load_all()))


def _db_ids(where: str) -> set[str]:
    conn = sqlite3.connect(config.DB_PATH)
    try:
        rows = conn.execute(f"SELECT product_id FROM products WHERE {where}", {"t": TODAY})
        return {r[0] for r in rows}
    finally:
        conn.close()


def _store_product_ids(store) -> set[str]:
    metas = store.get(include=["metadatas"])["metadatas"]
    return {m["product_id"] for m in metas if m.get("source_type") == "product_db"}


def test_active_products_match_vector_store(store):
    active = _db_ids("effective_from <= :t AND (effective_to IS NULL OR effective_to >= :t)")
    assert _store_product_ids(store) == active


def test_expired_products_are_not_in_vector_store(store):
    expired = _db_ids("effective_to IS NOT NULL AND effective_to < :t")
    assert expired.isdisjoint(_store_product_ids(store))