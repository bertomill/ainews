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
    try:
        if not NEWS_API_KEY:
            logger.error("NEWS_API_KEY is not set")
            return "NEWS_API_KEY is not set", 500
        
        url = f'https://newsapi.org/v2/everything?q=ai&apiKey={NEWS_API_KEY}'
        logger.info("Fetching news from URL: %s", url)
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])

        # Log the number of articles fetched
        logger.info("Number of articles fetched: %d", len(articles))

        # HTML template with basic styling
        template = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI News</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                .container {
                    width: 80%;
                    margin: auto;
                    overflow: hidden;
                }
                header {
                    background: #333;
                    color: #fff;
                    padding-top: 30px;
                    min-height: 70px;
                    border-bottom: #0779e4 3px solid;
                }
                header h1 {
                    text-align: center;
                    text-transform: uppercase;
                    margin: 0;
                    font-size: 24px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    background: #fff;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                li img {
                    max-width: 100%;
                    height: auto;
                    display: block;
                }
                li a {
                    color: #333;
                    text-decoration: none;
                }
                li a:hover {
                    color: #0779e4;
                }
                .description {
                    margin: 10px 0;
                }
                .meta {
                    color: #666;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>AI News</h1>
            </header>
            <div class="container">
                <ul>
                    {% for article in articles %}
                    <li>
                        {% if article.urlToImage %}
                        <img src="{{ article.urlToImage }}" alt="{{ article.title }}">
                        {% endif %}
                        <a href="{{ article.url }}" target="_blank"><h2>{{ article.title }}</h2></a>
                        <p class="description">{{ article.description }}</p>
                        <p class="meta">
                            <strong>Source:</strong> {{ article.source.name }}<br>
                            <strong>Author:</strong> {{ article.author }}<br>
                            <strong>Published At:</strong> {{ article.publishedAt }}
                        </p>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
        '''
        return render_template_string(template, articles=articles)
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return "An error occurred while fetching news", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
