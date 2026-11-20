// test_parse_simple.mjs
const res = await fetch('http://127.0.0.1:9222/json');
const targets = await res.json();
let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
if (!pageTarget) pageTarget = targets.find(t => t.type === 'page');

const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);

ws.onmessage = (evt) => {
    const msg = JSON.parse(evt.data);
    if (msg.method === 'Runtime.consoleAPICalled') {
        const vals = (msg.params.args || []).map(a => a.value || a.description || '');
        console.log('BROWSER CONSOLE:', vals.join(' '));
    } else if (msg.method === 'Runtime.exceptionThrown') {
        console.error('BROWSER EXCEPTION:', JSON.stringify(msg.params.exceptionDetails, null, 2));
    }
};

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

await send('Runtime.enable');

const evalRes = await send('Runtime.evaluate', {
    expression: `
        (() => {
            console.log("Checking why GLTFExporter hasn't finished...");
            // Let's inspect the export function directly
            return {
                hasExportFn: typeof window.exportSceneToGLTF === 'function',
                hasExporter: typeof THREE_GLTFExporter !== 'undefined'
            };
        })()
    `,
    returnByValue: true
});
console.log('Eval result:', evalRes);
ws.close();
