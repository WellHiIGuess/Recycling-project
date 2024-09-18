const WebSocket = require('ws');

const server = new WebSocket.Server({ port: 8080 });

const bins = {}; // Store clients as bins with address and status

server.on('connection', (ws) => {
    // Assign a unique ID to each client
    const id = generateUniqueID();
    bins[id] = {
        address: null,
        status: 'empty'
    };

    ws.on('message', (message) => {
        // Parse the incoming message
        try {
            const data = JSON.parse(message);
            
            if (data.address) {
                bins[id].address = data.address;
            }

            if (data.status) {
                bins[id].status = data.status;
            }

            console.log(`Bin ${id}:`, bins[id]);
        } catch (e) {
            console.error('Invalid message format:', message);
        }
    });

    ws.on('close', () => {
        delete bins[id];
        console.log(`Bin ${id} disconnected.`);
    });
});

// Helper function to generate a unique ID for each bin
function generateUniqueID() {
    return Math.random().toString(36).substr(2, 9);
}

console.log('WebSocket server is running on ws://localhost:8080');
