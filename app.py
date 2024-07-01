# app.py

from flask import Flask, render_template
import os
import logging
import requests
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def is_valid_article(article):
    return (
        article.get('title') and 
        article.get('description') and 
        article.get('urlToImage') and 
        'removed' not in article.get('title').lower()
    )

@app.route('/')
def home():
    try:
        if not NEWS_API_KEY:
            logger.error("NEWS_API_KEY is not set")
            return "NEWS_API_KEY is not set", 500
        
        url = f'https://newsapi.org/v2/everything?q=ai&apiKey={NEWS_API_KEY}'
        logger.info("Fetching news from URL: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        valid_articles = [article for article in articles if is_valid_article(article)]

        # Log the number of valid articles fetched
        logger.info("Number of valid articles fetched: %d", len(valid_articles))

        return render_template('index.html', articles=valid_articles)
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return "An error occurred while fetching news", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
