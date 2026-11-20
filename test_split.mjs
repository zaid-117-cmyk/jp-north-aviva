import fs from 'fs';

async function testSplit() {
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

    for (let i = 0; i < 3; i++) {
        const p = 0.2 + i * 0.1;
        const t0 = Date.now();
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p});` });
        const t1 = Date.now();
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 80 });
        const t2 = Date.now();
        console.log(`Frame ${i}: Render = ${t1 - t0}ms, Screenshot = ${t2 - t1}ms, Total = ${t2 - t0}ms`);
    }
    ws.close();
}
testSplit().catch(console.error);
