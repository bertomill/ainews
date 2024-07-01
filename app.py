# app.py

from flask import Flask, jsonify
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

@app.route('/')
def home():
    try:
        return "Hello, World!"
    except Exception as e:
        logger.error("Error in home route: %s", e)
        return "An error occurred", 500

@app.route('/news')
def get_news():
    try:
        url = f'https://newsapi.org/v2/everything?q=ai&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return jsonify(articles)
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return "An error occurred while fetching news", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
