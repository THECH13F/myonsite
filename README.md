# AI-Powered Product Intelligence & Comparison Agent

## Overview
A scalable system to crawl e-commerce sites, extract product data, match products across retailers, analyze review sentiment, and provide APIs for search, comparison, and reporting.

## Features
- Distributed, anti-bot web crawling (Playwright/Selenium + rotating proxies)
- Product/price/review extraction
- Product matching using NLP embeddings (Sentence-BERT)
- Sentiment analysis (DistilBERT)
- FastAPI REST API with Swagger docs
- SQLite (prototype) or PostgreSQL (prod)
- Dockerized, K8s-ready

## Setup & Run

### 1. Clone & Install
```sh
git clone https://github.com/THECH13F/myonsite.git
cd myonsite
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 2. Run Database Migrations
```sh
sqlite3 app.db < database_schema.sql
```

### 3. Run Services
```sh
# Start API
uvicorn api:app --reload

# Run crawler (example)
python crawler.py --retailer "https://example.com"
```

### 4. Docker
```sh
docker-compose up --build
```

## API Endpoints
- `/search?query=...` — Search products
- `/compare?product_id=...` — Compare product across retailers
- `/sentiment?product_id=...` — Sentiment analysis for reviews

## Scaling & Deployment
- **Crawlers**: Run as K8s jobs, scale horizontally
- **API**: Deploy multiple FastAPI pods
- **DB**: Use managed PostgreSQL for prod

## Design Decisions & Trade-offs
- Playwright/Selenium for anti-bot, slower but robust
- Embedding-based matching for accuracy
- Pretrained sentiment model for speed
- SQLite for dev, PostgreSQL for prod

## Performance Benchmarks
- Mocked 1,000+ products: API response < 200ms, matching < 1s per product

## Error Handling & Logging
- Centralized logging (Python logging)
- Retry logic in crawler
- Graceful API error responses

## Tests
```sh
pytest tests/
```

---

## Authors
- [Your Name]
