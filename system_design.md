# AI-Powered Product Intelligence & Comparison Agent: System Design

## High-Level Architecture

```mermaid
graph TD
    subgraph Crawling
        A1[Distributed Crawler (Playwright/Selenium)]
        A2[Proxy Pool & Rotator]
        A3[Anti-Detection Middleware]
    end
    subgraph Data Processing
        B1[Product Extractor (BS4/Regex)]
        B2[Review Extractor]
        B3[Product Matcher (NLP Embeddings)]
        B4[Sentiment Analyzer (Transformers)]
    end
    subgraph Storage
        C1[(PostgreSQL/SQLite)]
    end
    subgraph API Layer
        D1[FastAPI Service]
    end
    subgraph Reporting
        E1[Comparison Reports]
    end

    A1 -->|HTML| B1
    A1 -->|HTML| B2
    B1 -->|Products| C1
    B2 -->|Reviews| C1
    B3 -->|Matches| C1
    B4 -->|Sentiment| C1
    C1 --> D1
    D1 --> E1
    A2 --> A1
    A3 --> A1
    B1 --> B3
    B2 --> B4
```

## Component Overview
- **Crawler**: Distributed, headless browser-based, proxy-rotated, anti-bot.
- **Extractor**: Parses product, price, specs, reviews.
- **Matcher**: Embeds product info, matches via cosine similarity.
- **Sentiment**: Classifies review sentiment.
- **API**: FastAPI, RESTful, Swagger docs.
- **DB**: PostgreSQL (prod), SQLite (dev).
- **Deployment**: Docker, docker-compose, K8s-ready.

## Scaling & Deployment
- **Crawlers**: Horizontally scalable, stateless, managed by K8s jobs.
- **API**: Scalable FastAPI pods behind load balancer.
- **DB**: Managed PostgreSQL, read replicas for scale.
- **Reporting**: Batch jobs or on-demand via API.
- **Monitoring**: Logging, error tracking, health checks.

---

# API Endpoints

- `/search?query=...` → Search products across retailers
- `/compare?product_id=...` → Compare product across retailers
- `/sentiment?product_id=...` → Get sentiment analysis for product reviews

---

# Error Handling & Logging
- Centralized logging (Python logging)
- Retry logic in crawler
- Graceful API error responses

---

# Trade-offs
- SQLite for prototype, PostgreSQL for production
- Playwright/Selenium for anti-bot, slower than requests
- Embedding-based matching: robust, but needs tuning
- Sentiment: Pretrained model for speed, not domain-specific
