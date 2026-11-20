// debug_export.mjs
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
        (() => {
            console.log("Starting quick GLTF export test...");
            const exporter = new THREE.GLTFExporter ? new THREE.GLTFExporter() : null;
            // Test how many meshes are in materialGroup
            let count = 0;
            materialGroup.traverse((c) => { if (c.isMesh) count++; });
            console.log("Meshes in materialGroup:", count);
            return { meshCount: count };
        })()
    `,
    returnByValue: true
});
console.log('Result:', result);
await new Promise(r => setTimeout(r, 1000));
ws.close();
