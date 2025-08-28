import asyncio
from dotenv import load_dotenv
import logging
import random
from typing import List, Dict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import sqlite3
import time
import requests
import os
import google.generativeai as genai


PROXIES = [
    # Add your proxy URLs here
    'http://proxy1.example.com:8000',
    'http://proxy2.example.com:8000',
]

logging.basicConfig(level=logging.INFO)
load_dotenv()

class ProductCrawler:
    def __init__(self, retailer_url: str, db_path: str = 'app.db', use_proxy: bool = False):
        self.retailer_url = retailer_url
        self.db_path = db_path
        self.use_proxy = use_proxy

    async def fetch(self, url: str, proxy: str | None = None) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(proxy={"server": proxy} if proxy else None)
            page = await context.new_page()
            try:
                await page.goto(url, timeout=60000)
                await asyncio.sleep(random.uniform(2, 5))  # Anti-bot
                html = await page.content()
                await browser.close()
                return html
            except Exception as e:
                logging.error(f"Failed to fetch {url}: {e}")
                await browser.close()
                return ""

    def parse_products(self, html: str) -> List[Dict]:
        """
        Use Gemini API to extract product details from HTML dynamically.
        Set GEMINI_API_KEY in your environment.
        """
        import json as _json
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logging.error("No Gemini API key found in environment.")
            return []
        # Truncate HTML for prompt size
        html_snippet = html[:6000]
        prompt = (
            "Extract the product name, price, and specifications from the following HTML. "
            "Return a JSON list with keys: name, price, specs.\nHTML:\n" + html_snippet
        )
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            content = response.text
            # Try to extract JSON from response
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1:
                products = _json.loads(content[start:end+1])
                return products
            else:
                logging.error("No JSON list found in Gemini model response.")
                return []
        except Exception as e:
            logging.error(f"Gemini AI extraction failed: {e}")
            return []

    def save_products(self, products: List[Dict]):
        import json
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for prod in products:
            specs_str = json.dumps(prod['specs']) if isinstance(prod['specs'], list) else str(prod['specs'])
            c.execute('INSERT OR IGNORE INTO products (name, specs, retailer_id) VALUES (?, ?, ?)',
                      (prod['name'], specs_str, 1))
            conn.commit()
        conn.close()

    async def crawl(self):
        proxy = random.choice(PROXIES) if self.use_proxy else None
        html = await self.fetch(self.retailer_url, proxy)
        if html:
            products = self.parse_products(html)
            self.save_products(products)
            logging.info(f"Saved {len(products)} products from {self.retailer_url}")
        else:
            logging.error(f"No HTML fetched for {self.retailer_url}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--retailer', required=True, help='Retailer URL to crawl')
    parser.add_argument('--use-proxy', action='store_true', help='Enable proxy rotation')
    args = parser.parse_args()
    crawler = ProductCrawler(args.retailer, use_proxy=args.use_proxy)
    asyncio.run(crawler.crawl())
