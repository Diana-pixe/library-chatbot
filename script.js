const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

let isTyping = false;

function sendMessage() {
    const message = userInput.value;
    if (message.trim() === '') return;

    addUserMessage(message);
    userInput.value = '';
    sendButton.disabled = true;
    isTyping = true;
    chatMessages.scrollTop = chatMessages.scrollHeight;

    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        addBotMessage(data.response);
        isTyping = false;
        sendButton.disabled = false;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        addBotMessage("Sorry, I couldn't connect to the server.");
        isTyping = false;
        sendButton.disabled = false;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'user-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
}

function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bot-message');
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

userInput.addEventListener('input', () => {
    sendButton.disabled = !userInput.value.trim();
});
