from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import logging

app = FastAPI(title="Product Intelligence API")
logging.basicConfig(level=logging.INFO)

DATABASE = 'app.db'

class ProductOut(BaseModel):
    id: int
    name: str
    specs: Optional[str]
    retailer_id: int

class ReviewOut(BaseModel):
    id: int
    review_text: str
    sentiment: Optional[str]
    rating: Optional[float]

@app.get("/search", response_model=List[ProductOut])
def search_products(query: str):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, name, specs, retailer_id FROM products WHERE name LIKE ?", (f"%{query}%",))
    rows = c.fetchall()
    conn.close()
    return [ProductOut(id=r[0], name=r[1], specs=r[2], retailer_id=r[3]) for r in rows]

@app.get("/compare")
def compare_product(product_id: int):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT matched_product_id, similarity FROM matches WHERE product_id=? ORDER BY similarity DESC", (product_id,))
    matches = c.fetchall()
    result = []
    for mid, sim in matches:
        c.execute("SELECT id, name, specs, retailer_id FROM products WHERE id=?", (mid,))
        prod = c.fetchone()
        if prod:
            result.append({"product": {"id": prod[0], "name": prod[1], "specs": prod[2], "retailer_id": prod[3]}, "similarity": sim})
    conn.close()
    return result

@app.get("/sentiment", response_model=List[ReviewOut])
def get_sentiment(product_id: int):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, review_text, sentiment, rating FROM reviews WHERE product_id=?", (product_id,))
    rows = c.fetchall()
    conn.close()
    return [ReviewOut(id=r[0], review_text=r[1], sentiment=r[2], rating=r[3]) for r in rows]

@app.get("/")
def root():
    return {"message": "Product Intelligence API. See /docs for Swagger UI."}
