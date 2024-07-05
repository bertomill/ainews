# AI Lens

AI Lens is a web application that fetches and displays the latest news articles related to AI from various sources. Users can search for specific topics, view articles, and take notes on individual articles. The application is built with Flask for the backend and uses JavaScript for dynamic frontend interactions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Endpoints](#api-endpoints)
- [Frontend Functionality](#frontend-functionality)
- [Environment Variables](#environment-variables)
- [Notes](#notes)

## Features

- Fetch and display AI-related news articles.
- Search for articles by topic or query.
- Take and save notes on individual articles.
- Responsive design with a sidebar for navigation.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd ai-lens
    ```

2. **Set up a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```
    NEWS_API_KEY=your_news_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the application**:
    ```sh
    flask run
    ```

## Usage

- Open your browser and navigate to `http://127.0.0.1:5000/`.
- Use the sidebar to navigate between different topics.
- Use the search bar to find articles by keywords.
- Click on the pencil icon to take notes on an article.
- View and manage your notes in the "View Notes" section.

## File Structure

.
├── app.py
├── database_setup.py
├── requirements.txt
├── static
│ ├── assistant.css
│ ├── navbar.css
│ ├── sidebar.css
│ ├── style.css
│ ├── app.js
├── templates
│ ├── ai_assistant.html
│ ├── header.html
│ ├── index.html
│ ├── notes.html
├── notes.db
├── .env
├── .gitignore
└── README.md

perl
Copy code

## API Endpoints

### `GET /`

Fetches and displays the latest AI-related news articles on the homepage.

### `POST /chat`

Handles chat requests to the OpenAI API.

### `POST /save_note`

Saves a note to the SQLite database.

### `GET /notes`

Displays all saved notes.

### `GET /api/articles`

Fetches articles by a specific topic.

### `GET /api/search`

Searches for articles by a specific query.

## Frontend Functionality

- **app.js**:
  - `fetchNotes()`: Fetches and displays saved notes.
  - `fetchArticlesByTopic(topic)`: Fetches and displays articles by topic.
  - `searchArticles()`: Searches for articles by query.
  - `saveNote()`: Saves a note.
  - `toggleNotes()`: Toggles the notes column visibility.
  - `openNoteModal(title)`: Opens the note-taking modal.
  - `closeNoteModal()`: Closes the note-taking modal.

- **index.html**:
  - Displays the articles in a grid layout.
  - Includes a sidebar for navigation and search functionality.
  - Incorporates a modal for taking notes.

## Environment Variables

- `NEWS_API_KEY`: Your API key for the News API.
- `OPENAI_API_KEY`: Your API key for the OpenAI API.

## Notes

- Ensure the `.env` file contains valid API keys for the application to function correctly.
- Articles with titles or descriptions marked as "[Removed]" will not be displayed.
- The application uses the `date-fns` library for date formatting.

## Example `.env` File

NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key

csharp
Copy code

## License

This project is licensed under the MIT License.