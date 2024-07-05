from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import os
import logging
import requests
from dotenv import load_dotenv
from openai import OpenAI
import sqlite3
from datetime import datetime

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from Vercel
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not NEWS_API_KEY or not OPENAI_API_KEY:
    logger.error("Environment variables NEWS_API_KEY or OPENAI_API_KEY are not set.")
    raise ValueError("Environment variables NEWS_API_KEY or OPENAI_API_KEY are not set.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_db_connection():
    connection = sqlite3.connect('notes.db')
    connection.row_factory = sqlite3.Row
    return connection

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
        valid_articles = [
            {
                **article,
                'publishedAt': datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y') if article.get('publishedAt') else 'Unknown date'
            }
            for article in articles if article.get('title') and article.get('description') and article.get('title') != '[Removed]' and article.get('description') != '[Removed]'
        ]

        # Log the number of valid articles fetched
        logger.info("Number of valid articles fetched: %d", len(valid_articles))

        response = make_response(render_template('index.html', articles=valid_articles))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except requests.RequestException as e:
        logger.error("Error fetching news: %s", e)
        return "An error occurred while fetching news", 500

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        chat_response = response.choices[0].message.content.strip()
        return jsonify({"response": chat_response})
    except Exception as e:
        logger.error("Error during OpenAI API call: %s", e)
        return jsonify({"response": "An error occurred while processing your request."}), 500

@app.route('/save_note', methods=['POST'])
def save_note():
    note_data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO notes (title, note) VALUES (?, ?)', (note_data['title'], note_data['note']))
    connection.commit()
    connection.close()
    return jsonify({"message": "Note saved successfully!"})

@app.route('/notes')
def view_notes():
    connection = get_db_connection()
    notes = connection.execute('SELECT * FROM notes').fetchall()
    connection.close()
    return render_template('notes.html', notes=notes)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    topic = request.args.get('topic', 'ai')  # Default to 'ai' if no topic provided
    try:
        url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return jsonify([article for article in articles if article.get('title') and article.get('description') and article.get('title') != '[Removed]' and article.get('description') != '[Removed]'])
    except requests.RequestException as e:
        logger.error("Error fetching articles: %s", e)
        return jsonify({"error": "An error occurred while fetching articles"}), 500

@app.route('/api/search', methods=['GET'])
def search_articles():
    query = request.args.get('query', '')
    try:
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return jsonify([article for article in articles if article.get('title') and article.get('description') and article.get('title') != '[Removed]' and article.get('description') != '[Removed]'])
    except requests.RequestException as e:
        logger.error("Error searching articles: %s", e)
        return jsonify({"error": "An error occurred while searching for articles"}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
