const statusDiv = document.getElementById('status');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messagesDiv = document.getElementById('messages');
const networkStatsDiv = document.getElementById('networkStats');

const ws = new WebSocket('ws://localhost:8080');

ws.onopen = () => {
    statusDiv.textContent = 'Connected to the server';
    fetchNetworkStats();
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === 'networkStats') {
        updateNetworkStats(message.data);
    } else {
        displayMessage(`Received: ${message.data}`);
    }
};

ws.onclose = () => {
    statusDiv.textContent = 'Disconnected from the server';
};

ws.onerror = (error) => {
    statusDiv.textContent = `Error: ${error.message}`;
};

sendButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (message) {
        ws.send(JSON.stringify({ type: 'message', data: message }));
        displayMessage(`Sent: ${message}`);
        messageInput.value = '';
    }
});

function displayMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
}

function fetchNetworkStats() {
    ws.send(JSON.stringify({ type: 'fetchNetworkStats' }));
}

function updateNetworkStats(stats) {
    networkStatsDiv.innerHTML = '';
    const statsDiv = document.createElement('div');
    statsDiv.textContent = `Bytes Sent: ${stats.bytesSent}, Bytes Received: ${stats.bytesReceived}`;
    networkStatsDiv.appendChild(statsDiv);
  }
