document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatOutput = document.getElementById('chat-output');

    if (chatForm && chatInput && chatOutput) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const userMessage = chatInput.value;
            chatInput.value = '';

            const userMessageElement = document.createElement('div');
            userMessageElement.textContent = `You: ${userMessage}`;
            userMessageElement.classList.add('chat-message', 'user');
            chatOutput.appendChild(userMessageElement);

            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                const botMessageElement = document.createElement('div');
                botMessageElement.textContent = `ChatGPT: ${data.response}`;
                botMessageElement.classList.add('chat-message', 'bot');
                chatOutput.appendChild(botMessageElement);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    } else {
        console.error('Chat form, input, or output not found.');
    }
});
