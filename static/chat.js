document.addEventListener('DOMContentLoaded', function() {
    const saveNoteButton = document.querySelector('.save-note-btn');
    const notesColumn = document.getElementById('notes-column');

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
});
