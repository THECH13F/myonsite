-- Database Schema for Product Intelligence System

CREATE TABLE retailers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    retailer_id INTEGER REFERENCES retailers(id),
    name TEXT NOT NULL,
    specs TEXT,
    description TEXT,
    embedding BLOB,
    UNIQUE(retailer_id, name)
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    price REAL NOT NULL,
    currency TEXT NOT NULL,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    review_text TEXT NOT NULL,
    reviewer TEXT,
    rating REAL,
    sentiment TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    matched_product_id INTEGER REFERENCES products(id),
    similarity REAL NOT NULL,
    UNIQUE(product_id, matched_product_id)
);
