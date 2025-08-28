import pytest
from sentiment import SentimentAnalyzer
import sqlite3

def test_sentiment_runs(tmp_path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE reviews (id INTEGER PRIMARY KEY, review_text TEXT, sentiment TEXT)')
    c.execute('INSERT INTO reviews (id, review_text) VALUES (1, "I love this!"), (2, "Terrible product.")')
    conn.commit()
    conn.close()
    analyzer = SentimentAnalyzer(str(db))
    analyzer.analyze_and_update()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT sentiment FROM reviews')
    sentiments = [row[0] for row in c.fetchall()]
    assert all(s in ("POSITIVE", "NEGATIVE") for s in sentiments)
    conn.close()
