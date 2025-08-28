import pytest
from matcher import ProductMatcher
import sqlite3

def test_matcher_runs(tmp_path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, specs TEXT)')
    c.execute('CREATE TABLE matches (id INTEGER PRIMARY KEY, product_id INTEGER, matched_product_id INTEGER, similarity REAL, UNIQUE(product_id, matched_product_id))')
    c.execute('INSERT INTO products (id, name, specs) VALUES (1, "A", "spec1"), (2, "A", "spec1")')
    conn.commit()
    conn.close()
    matcher = ProductMatcher(str(db))
    matcher.match(threshold=0.5)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM matches')
    assert c.fetchone()[0] > 0
    conn.close()
