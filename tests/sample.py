import sqlite3
from app import config
conn = sqlite3.connect(config.DB_PATH)
for row in conn.execute("SELECT product_id, product_name, effective_from, effective_to FROM products"):
    print(row)
conn.close()