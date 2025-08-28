import sqlite3
import pytest
from matcher import ProductMatcher
from sentiment import SentimentAnalyzer

# Integration test: Insert products, reviews, run matcher and sentiment

def test_full_pipeline(tmp_path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, specs TEXT)')
    c.execute('CREATE TABLE matches (id INTEGER PRIMARY KEY, product_id INTEGER, matched_product_id INTEGER, similarity REAL, UNIQUE(product_id, matched_product_id))')
    c.execute('CREATE TABLE reviews (id INTEGER PRIMARY KEY, review_text TEXT, sentiment TEXT)')
    c.execute('INSERT INTO products (id, name, specs) VALUES (1, "A", "spec1"), (2, "A", "spec1")')
    c.execute('INSERT INTO reviews (id, review_text) VALUES (1, "I love this!"), (2, "Terrible product.")')
    conn.commit()
    conn.close()
    matcher = ProductMatcher(str(db))
    matcher.match(threshold=0.5)
    analyzer = SentimentAnalyzer(str(db))
    analyzer.analyze_and_update()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM matches')
    assert c.fetchone()[0] > 0
    c.execute('SELECT sentiment FROM reviews')
    sentiments = [row[0] for row in c.fetchall()]
    assert all(s in ("POSITIVE", "NEGATIVE") for s in sentiments)
    conn.close()
