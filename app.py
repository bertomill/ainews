from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import logging
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__, static_folder='static')

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

notes = []

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
    notes.append(note_data)
    return jsonify({"message": "Note saved successfully!"})

@app.route('/notes')
def view_notes():
    return render_template('notes.html', notes=notes)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
