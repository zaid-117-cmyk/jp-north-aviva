// test_export_step_by_step.mjs
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

const result = await send('Runtime.evaluate', {
    expression: `
        (async () => {
            console.log("Calling window.exportSceneToGLTF step-by-step...");
            try {
                const res = await window.exportSceneToGLTF({ binary: true });
                console.log("Finished exportSceneToGLTF:", JSON.stringify(res));
                return res;
            } catch(e) {
                console.error("Export failed with error:", e.message, e.stack);
                return { error: e.message };
            }
        })()
    `,
    awaitPromise: true,
    returnByValue: true
});

console.log('Final Result:', result);
ws.close();
