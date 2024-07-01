# app.py

from flask import Flask, render_template_string
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
    return "Hello, World!"

@app.route('/news')
def get_news():
    try:
        url = f'https://newsapi.org/v2/everything?q=ai&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])

        # Simple HTML template
        template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI News</title>
        </head>
        <body>
            <h1>AI News</h1>
            <ul>
                {% for article in articles %}
                <li>
                    <a href="{{ article.url }}" target="_blank">{{ article.title }}</a><br>
                    <p>{{ article.description }}</p>
                </li>
                {% endfor %}
            </ul>
        </body>
        </html>
        '''
        return render_template_string(template, articles=articles)
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return "An error occurred while fetching news", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
