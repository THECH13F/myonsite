import sqlite3
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)

MODEL_NAME = 'distilbert-base-uncased-finetuned-sst-2-english'

class SentimentAnalyzer:
    def __init__(self, db_path='app.db'):
        self.db_path = db_path
        self.analyzer = pipeline('sentiment-analysis', model=MODEL_NAME)

    def fetch_reviews(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, review_text FROM reviews WHERE sentiment IS NULL')
        reviews = c.fetchall()
        conn.close()
        return reviews

    def analyze_and_update(self):
        reviews = self.fetch_reviews()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for review_id, text in reviews:
            try:
                result = self.analyzer(text[:512])[0]  # Truncate for model
                sentiment = result['label']
                c.execute('UPDATE reviews SET sentiment=? WHERE id=?', (sentiment, review_id))
            except Exception as e:
                logging.error(f"Sentiment analysis failed for review {review_id}: {e}")
        conn.commit()
        conn.close()
        logging.info('Sentiment analysis complete.')

if __name__ == "__main__":
    SentimentAnalyzer().analyze_and_update()
