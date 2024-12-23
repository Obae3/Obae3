const WebSocket = require('ws');
const os = require('os');
const networkInterfaces = os.networkInterfaces();

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    ws.on('message', (message) => {
        const data = JSON.parse(message);
        if (data.type === 'fetchNetworkStats') {
            const networkStats = {
                bytesSent: networkInterfaces['eth0'][0].mac, // Example, update with actual data
                bytesReceived: networkInterfaces['eth0'][1].mac, // Example, update with actual data
            };
            ws.send(JSON.stringify({ type: 'networkStats', data: networkStats }));
        } else if (data.type === 'message') {
            ws.send(JSON.stringify({ type: 'message', data: `Hello, you sent -> ${data.data}` }));
        }
    });

    ws.send(JSON.stringify({ type: 'message', data: 'Welcome to the WebSocket server' }));
});

console.log('WebSocket server is running on ws://localhost:8080');
