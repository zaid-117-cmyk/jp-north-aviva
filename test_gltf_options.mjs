// test_gltf_options.mjs
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

await send('Runtime.enable');

// Test exporting without embedImages: false
const result = await send('Runtime.evaluate', {
    expression: `
        new Promise((resolve, reject) => {
            console.log("Testing GLTFExporter parse with binary: true, embedImages: true...");
            const exporter = new (window.THREE_GLTFExporter || class {})();
            // Let's create an export root containing procedural geometry
            const exportGroup = new THREE_SCENE_GROUP();
        })
    `,
    returnByValue: true
});
console.log('Result:', result);
ws.close();
