import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)

MODEL_NAME = 'all-MiniLM-L6-v2'

class ProductMatcher:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path
        self.model = SentenceTransformer(MODEL_NAME)

    def fetch_products(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, name, specs FROM products')
        products = c.fetchall()
        conn.close()
        return products

    def embed_products(self, products):
        texts = [f"{name} {specs}" for _, name, specs in products]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def match(self, threshold=0.8):
        products = self.fetch_products()
        embeddings = self.embed_products(products)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for i, (id1, _, _) in enumerate(products):
            for j, (id2, _, _) in enumerate(products):
                if i >= j:
                    continue
                sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                if sim > threshold:
                    c.execute('INSERT OR IGNORE INTO matches (product_id, matched_product_id, similarity) VALUES (?, ?, ?)',
                              (id1, id2, float(sim)))
        conn.commit()
        conn.close()
        logging.info('Product matching complete.')

if __name__ == "__main__":
    matcher = ProductMatcher()
    matcher.match()
