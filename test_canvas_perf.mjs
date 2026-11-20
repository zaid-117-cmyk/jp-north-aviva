import fs from 'fs';

async function testCanvasPerf() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    const pending = new Map();
    let msgId = 1;
    ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        if (data.id && pending.has(data.id)) {
            const { resolve, reject } = pending.get(data.id);
            pending.delete(data.id);
            if (data.error) reject(data.error);
            else resolve(data.result);
        }
    };
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = msgId++;
            pending.set(id, { resolve, reject });
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    const perf = await send('Runtime.evaluate', {
        expression: `
            (async () => {
                const canvas = document.getElementById('webgl-canvas');
                const times = [];
                for (let i = 0; i < 5; i++) {
                    const t0 = performance.now();
                    window.applyProgressToScene(0.2 + i * 0.1);
                    const t1 = performance.now();
                    const data = canvas.toDataURL('image/jpeg', 0.85);
                    const t2 = performance.now();
                    times.push({ render: t1 - t0, toDataURL: t2 - t1, bytes: data.length });
                }
                return times;
            })()
        `,
        awaitPromise: true,
        returnByValue: true
    });
    console.log('In-browser performance:', JSON.stringify(perf.result.value, null, 2));
    ws.close();
}
testCanvasPerf().catch(console.error);
