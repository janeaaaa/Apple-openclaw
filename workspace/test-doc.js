const WebSocket = require('ws');

const token = 'YOUR_TOKEN_HERE';
const ws = new WebSocket(`ws://127.0.0.1:18789?auth=${token}`);

ws.on('open', () => {
  console.log('Connected to Gateway with token');
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  console.log('Received:', JSON.stringify(msg, null, 2));
  
  if (msg.event === 'connect.challenge') {
    // Token already in URL, just acknowledge
    const response = {
      jsonrpc: '2.0',
      event: 'connect.response',
      payload: {}
    };
    ws.send(JSON.stringify(response));
    console.log('Sent auth ack');
    
    // Wait a bit then send request
    setTimeout(() => {
      const request = {
        jsonrpc: '2.0',
        id: 1,
        method: 'tools/call',
        params: {
          tool: 'feishu_doc',
          action: 'create',
          title: 'Test Document',
          owner_open_id: 'ou_a9c7b81a2b296cec5faa9df7ed96a8c0'
        }
      };
      ws.send(JSON.stringify(request));
      console.log('Sent tool call request');
    }, 1000);
  }
  
  if (msg.result) {
    console.log('Got result:', msg.result);
  }
});

ws.on('error', (err) => {
  console.error('Error:', err.message);
});

ws.on('close', () => {
  console.log('Connection closed');
  process.exit(0);
});

setTimeout(() => {
  console.log('Timeout - closing');
  ws.close();
}, 15000);
