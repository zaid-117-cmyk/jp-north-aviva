// check_page_state.mjs
const res = await fetch('http://127.0.0.1:9222/json');
const targets = await res.json();
let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
if (!pageTarget) pageTarget = targets.find(t => t.type === 'page');

const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);

function send(method, params = {}) {
    return new Promise((resolve) => {
        const id = Math.floor(Math.random() * 100000);
        const handler = (evt) => {
            const data = JSON.parse(evt.data);
            if (data.id === id) {
                ws.removeEventListener('message', handler);
                resolve(data.result);
            }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
    });
}

const evalRes = await send('Runtime.evaluate', {
    expression: 'console.log("Checking page heartbeat: " + performance.now()); ({ fps: 60, time: Date.now() })',
    returnByValue: true
});
console.log('Page heartbeat:', evalRes);
ws.close();
