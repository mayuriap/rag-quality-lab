
-- Northbridge Bank product catalogue (FICTIONAL).
-- In production this would live in Postgres/Oracle/Snowflake; SQLite uses the same SQL.

DROP TABLE IF EXISTS fees;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id      TEXT PRIMARY KEY,
    product_name    TEXT NOT NULL,
    product_type    TEXT NOT NULL CHECK (product_type IN ('current_account', 'savings', 'isa')),
    interest_rate   REAL CHECK (interest_rate >= 0),
    rate_basis      TEXT CHECK (rate_basis IN ('AER', 'gross', 'none')),
    rate_type       TEXT CHECK (rate_type IN ('fixed', 'variable', 'none')),
    term_months     INTEGER,
    min_deposit     REAL,
    max_balance     REAL,
    monthly_fee     REAL NOT NULL DEFAULT 0,
    eligibility     TEXT,
    features        TEXT,
    effective_from  DATE NOT NULL,
    effective_to    DATE,              -- NULL = currently active
    last_updated    TIMESTAMP NOT NULL
);

CREATE TABLE fees (
    fee_id          TEXT PRIMARY KEY,
    product_id      TEXT NOT NULL REFERENCES products(product_id),
    fee_name        TEXT NOT NULL,
    amount          REAL NOT NULL CHECK (amount >= 0),
    unit            TEXT NOT NULL CHECK (unit IN ('GBP', 'percent')),
    description     TEXT,
    effective_from  DATE NOT NULL,
    effective_to    DATE,
    last_updated    TIMESTAMP NOT NULL
);

