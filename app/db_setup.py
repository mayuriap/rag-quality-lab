"""Build the Northbridge product database from SQL files.

Run:  python -m app.db_setup
"""

import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = ROOT_DIR / "data" / "db"
DB_PATH = DB_DIR / "northbridge.db"


def build_database(db_path: Path = DB_PATH) -> None:
    if db_path.exists():
        db_path.unlink()  # rebuild from scratch so every run is reproducible
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript((DB_DIR / "schema.sql").read_text(encoding="utf-8"))
        conn.executescript((DB_DIR / "seed.sql").read_text(encoding="utf-8"))
        conn.commit()
        products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        active = conn.execute("SELECT COUNT(*) FROM products WHERE effective_to IS NULL").fetchone()[0]
        fees = conn.execute("SELECT COUNT(*) FROM fees").fetchone()[0]
    finally:
        conn.close()
    print(f"Built {db_path.name}: {products} product rows ({active} active), {fees} fee rows")


if __name__ == "__main__":
    build_database()