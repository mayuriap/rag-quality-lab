import sqlite3
from datetime import datetime

from app import config


def _last_db_update() -> datetime:
    conn = sqlite3.connect(config.DB_PATH)
    try:
        value = conn.execute("SELECT MAX(last_updated) FROM products").fetchone()[0]
    finally:
        conn.close()
    return datetime.fromisoformat(value)


def _store_built_at() -> datetime:
    store_file = config.VECTORSTORE_DIR / "chroma.sqlite3"
    return datetime.fromtimestamp(store_file.stat().st_mtime)


def is_fresh(db_updated: datetime, store_built: datetime) -> bool:
    return store_built >= db_updated


def test_vector_store_is_newer_than_last_db_update():
    db_updated, store_built = _last_db_update(), _store_built_at()
    assert is_fresh(db_updated, store_built), (
        f"Stale store: database updated {db_updated}, store built {store_built}. "
        "Re-run: python -m app.ingest"
    )


def test_freshness_rule_detects_a_stale_store():
    assert is_fresh(datetime(2026, 10, 1), datetime(2026, 9, 1)) is False
    assert is_fresh(datetime(2026, 9, 1), datetime(2026, 10, 1)) is True