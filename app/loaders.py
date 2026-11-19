"""Load the two knowledge sources and turn them into LangChain Documents.

1. Policy documents (data/raw)  -> one Document per file
2. Product database (SQLite)    -> one Document per ACTIVE product, with its fees

Run:  python -m app.loaders
"""

import sqlite3
from datetime import date

from langchain_core.documents import Document

from app import config

ACTIVE_PRODUCTS_SQL = """
SELECT * FROM products
WHERE effective_from <= :today
  AND (effective_to IS NULL OR effective_to >= :today)
ORDER BY product_id
"""

ACTIVE_FEES_SQL = """
SELECT * FROM fees
WHERE product_id = :product_id
  AND effective_from <= :today
  AND (effective_to IS NULL OR effective_to >= :today)
ORDER BY fee_id
"""


def load_policy_documents() -> list[Document]:
    docs = []
    for path in sorted(config.RAW_DATA_DIR.glob("*.md")):
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source_type": "policy_document", "source": path.name},
            )
        )
    return docs


def product_to_text(p: sqlite3.Row, fees: list[sqlite3.Row]) -> str:
    """Turn one database row into a short, readable description the LLM can quote."""
    lines = [f"Product: {p['product_name']} (product ID {p['product_id']})"]
    if p["interest_rate"]:
        lines.append(f"Interest rate: {p['interest_rate']:.2f}% {p['rate_basis']} ({p['rate_type']})")
    else:
        lines.append("Interest rate: this product pays no interest")
    if p["term_months"]:
        lines.append(f"Term: {p['term_months']} months")
    if p["min_deposit"] is not None:
        lines.append(f"Minimum deposit: £{p['min_deposit']:,.2f}")
    if p["max_balance"] is not None:
        lines.append(f"Maximum balance: £{p['max_balance']:,.2f}")
    lines.append(f"Monthly fee: £{p['monthly_fee']:,.2f}")
    if p["eligibility"]:
        lines.append(f"Eligibility: {p['eligibility']}")
    if p["features"]:
        lines.append(f"Features: {p['features']}")
    for f in fees:
        amount = f"{f['amount']:.2f}%" if f["unit"] == "percent" else f"£{f['amount']:,.2f}"
        lines.append(f"Fee - {f['fee_name']}: {amount}. {f['description'] or ''}".strip())
    lines.append(f"Rate effective from: {p['effective_from']}")
    return "\n".join(lines)


def load_product_records(as_of: date | None = None) -> list[Document]:
    today = (as_of or date.today()).isoformat()
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        docs = []
        for p in conn.execute(ACTIVE_PRODUCTS_SQL, {"today": today}):
            fees = conn.execute(ACTIVE_FEES_SQL, {"product_id": p["product_id"], "today": today}).fetchall()
            docs.append(
                Document(
                    page_content=product_to_text(p, fees),
                    metadata={
                        "source_type": "product_db",
                        "source": f"products/{p['product_id']}",
                        "product_id": p["product_id"],
                        "effective_from": p["effective_from"],
                        "last_updated": p["last_updated"],
                    },
                )
            )
        return docs
    finally:
        conn.close()


def load_all() -> list[Document]:
    return load_policy_documents() + load_product_records()


if __name__ == "__main__":
    policies = load_policy_documents()
    products = load_product_records()
    print(f"Policy documents: {len(policies)}")
    for d in policies:
        print(f"  - {d.metadata['source']}")
    print(f"Active products: {len(products)}")
    for d in products:
        print(f"  - {d.metadata['product_id']}")
    print("\nExample product record as the assistant will see it:\n")
    print(products[0].page_content)