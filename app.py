from flask import Flask
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    try:
        return "Hello, World!"
    except Exception as e:
        logger.error("Error in home route: %s", e)
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
