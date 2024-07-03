import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logger.error("Environment variable OPENAI_API_KEY is not set.")
    raise ValueError("Environment variable OPENAI_API_KEY is not set.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def test_openai_api():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        # Corrected to access response format correctly
        chat_response = response.choices[0].message.content.strip()
        logger.info("OpenAI API call successful. Response: %s", chat_response)
        print(f"OpenAI API call successful. Response: {chat_response}")
    except Exception as e:
        logger.error("Error during OpenAI API call: %s", e)
        print(f"Error during OpenAI API call: {e}")

if __name__ == "__main__":
    test_openai_api()
