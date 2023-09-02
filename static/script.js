document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const socket = new WebSocket("ws://localhost/ws");

    socket.addEventListener("message", (event) => {
        const response = event.data;
        appendMessage('Bot', response)
        messageInput.removeAttribute("disabled");
    });

    socket.addEventListener("open", (event) => {
        appendMessage('Server', "Connected to Chat Bot!")
        messageInput.removeAttribute("disabled");
    });

    socket.addEventListener("close", (event) => {
        appendMessage('Server', "Chat Bot Disconnected!")
        messageInput.setAttribute("disabled", true);
    });

    sendButton.addEventListener('click', () => {
        const userMessage = messageInput.value.trim();
        if (userMessage) {
            messageInput.setAttribute("disabled", true);
            appendMessage('You', userMessage);
            messageInput.value = '';
            socket.send(userMessage);
        }
    });

    document.addEventListener("keyup", function(event) {
        if (event.key === 'Enter') {
            const userMessage = messageInput.value.trim();
            if (userMessage) {
                messageInput.setAttribute("disabled", true);
                appendMessage('You', userMessage);
                messageInput.value = '';
                socket.send(userMessage);
            }
        }
    });

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender.toLowerCase()}`;
        messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        messageInput.setAttribute("disabled", true);
    }
});