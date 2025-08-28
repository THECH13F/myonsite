import pytest
from crawler import ProductCrawler
import sqlite3

class DummyCrawler(ProductCrawler):
    async def fetch(self, url, proxy=None):
        # Return static HTML for test
        return '''<div class="product-card"><span class="product-title">Test Product</span><span class="product-price">$10</span><span class="product-specs">Specs</span></div>'''

def test_parse_and_save(tmp_path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, specs TEXT, retailer_id INTEGER)')
    conn.commit()
    conn.close()
    crawler = DummyCrawler("http://dummy", str(db))
    products = crawler.parse_products(crawler.fetch("", None).send(None))
    crawler.save_products(products)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT name FROM products')
    assert c.fetchone()[0] == "Test Product"
    conn.close()
