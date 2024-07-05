document.addEventListener('DOMContentLoaded', function() {
    const saveNoteButton = document.querySelector('.save-note-btn');
    const notesColumn = document.getElementById('notes-column');
    const articlesContainer = document.getElementById('articles-container');
    const searchButton = document.getElementById('search-button');
    const viewNotesButton = document.getElementById('view-notes-btn');
    const sidebarLinks = document.querySelectorAll('.sidebar-links a');
    const noteModal = document.getElementById('note-modal');

    // Function to fetch and display notes
    function fetchNotes() {
        fetch('/notes')
            .then(response => response.text())
            .then(data => {
                notesColumn.innerHTML = data;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to fetch and display articles by topic
    function fetchArticlesByTopic(topic) {
        fetch(`/api/articles?topic=${topic}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(articles => {
                articlesContainer.innerHTML = '';
                articles.forEach(article => {
                    const articleElement = document.createElement('div');
                    articleElement.className = 'grid-item';
                    articleElement.innerHTML = `
                        <div class="article-header">
                            <h2>${article.title}</h2>
                            <button class="note-btn" data-title="${article.title}">✏️</button>
                        </div>
                        ${article.urlToImage ? `<img src="${article.urlToImage}" alt="${article.title}">` : ''}
                        <p class="description">${article.description}</p>
                        <p class="meta">
                            <strong>Source:</strong> ${article.source.name}<br>
                            <strong>Author:</strong> ${article.author}<br>
                            <strong>Published At:</strong> ${article.publishedAt}
                        </p>
                        <p><a href="${article.url}" target="_blank">Read more</a></p>
                    `;
                    articlesContainer.appendChild(articleElement);
                });

                // Add event listeners for the dynamically created note buttons
                document.querySelectorAll('.note-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        openNoteModal(button.getAttribute('data-title'));
                    });
                });
            })
            .catch(error => console.error('Error fetching articles:', error));
    }

    // Function to search for articles
    function searchArticles() {
        const query = document.getElementById('search-query').value;
        fetch(`/api/search?query=${query}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(articles => {
                articlesContainer.innerHTML = '';
                articles.forEach(article => {
                    const articleElement = document.createElement('div');
                    articleElement.className = 'grid-item';
                    articleElement.innerHTML = `
                        <div class="article-header">
                            <h2>${article.title}</h2>
                            <button class="note-btn" data-title="${article.title}">✏️</button>
                        </div>
                        ${article.urlToImage ? `<img src="${article.urlToImage}" alt="${article.title}">` : ''}
                        <p class="description">${article.description}</p>
                        <p class="meta">
                            <strong>Source:</strong> ${article.source.name}<br>
                            <strong>Author:</strong> ${article.author}<br>
                            <strong>Published At:</strong> ${article.publishedAt}
                        </p>
                        <p><a href="${article.url}" target="_blank">Read more</a></p>
                    `;
                    articlesContainer.appendChild(articleElement);
                });

                // Add event listeners for the dynamically created note buttons
                document.querySelectorAll('.note-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        openNoteModal(button.getAttribute('data-title'));
                    });
                });
            })
            .catch(error => console.error('Error fetching articles:', error));
    }

    // Save note button event listener
    if (saveNoteButton) {
        saveNoteButton.addEventListener('click', function() {
            const noteTitle = document.getElementById('note-title').innerText.replace('Notes for: ', '');
            const noteText = document.getElementById('note-text').value;

            fetch('/save_note', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: noteTitle, note: noteText })
            })
            .then(response => response.json())
            .then(data => {
                alert('Note saved successfully!');
                closeNoteModal();
                fetchNotes(); // Fetch and display notes after saving
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Fetch notes on page load
    fetchNotes();

    // Event listeners for topic links
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const topic = this.getAttribute('data-topic');
            fetchArticlesByTopic(topic);
        });
    });

    // Event listener for search button
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            searchArticles();
        });
    }

    if (viewNotesButton) {
        viewNotesButton.addEventListener('click', function() {
            toggleNotes();
        });
    }
});

function openAssistant() {
    const assistant = document.getElementById('ai-assistant');
    assistant.style.right = '0';
}

function closeAssistant() {
    const assistant = document.getElementById('ai-assistant');
    assistant.style.right = '-100%';
}

async function handlePrompt(prompt) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: prompt })
    });
    const data = await response.json();
    const chatResponse = data.response;

    const responseContainer = document.getElementById('ai-output');
    responseContainer.innerHTML = `<p class="chat-message bot">${chatResponse}</p>` + responseContainer.innerHTML;
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

document.getElementById('ai-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const aiInput = document.getElementById('ai-input');
    const prompt = aiInput.value;
    aiInput.value = '';
    const responseContainer = document.getElementById('ai-output');
    responseContainer.innerHTML = `<p class="chat-message user">${prompt}</p>` + responseContainer.innerHTML;
    responseContainer.scrollTop = responseContainer.scrollHeight;
    handlePrompt(prompt);
    
});
function toggleNotes() {
    const notesColumn = document.getElementById('notes-column');
    const mainContent = document.querySelector('.main-content');
    if (notesColumn.style.transform === 'translateX(0px)') {
        notesColumn.style.transform = `translateX(-300px)`; // Match the new width
        mainContent.style.marginLeft = '250px'; // Reset to initial margin
    } else {
        notesColumn.style.transform = 'translateX(0px)';
        mainContent.style.marginLeft = '300px'; // Adjust according to the new notes column width
    }
}


function openNoteModal(title) {
    document.getElementById('note-title').innerText = `Notes for: ${title}`;
    const noteModal = document.getElementById('note-modal');
    noteModal.style.display = 'block';
}

function closeNoteModal() {
    const noteModal = document.getElementById('note-modal');
    noteModal.style.display = 'none';
}

async function saveNote() {
    const title = document.getElementById('note-title').innerText.replace('Notes for: ', '');
    const noteText = document.getElementById('note-text').value;
    const response = await fetch('/save_note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, note: noteText })
    });
    if (response.ok) {
        alert('Note saved successfully!');
        closeNoteModal();
    } else {
        alert('Failed to save note.');
    }
}
