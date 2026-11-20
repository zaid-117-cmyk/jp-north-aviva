import fs from 'fs';

async function captureBath() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    const t = targets.find(x => x.type === 'page' && x.url.includes('8080')) || targets.find(x => x.type === 'page');
    if (!t) throw new Error('No page found');
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    let id = 1;
    const send = (m, p = {}) => new Promise((resolve, reject) => {
        const reqId = id++;
        const onm = (evt) => {
            const d = JSON.parse(evt.data);
            if (d.id === reqId) {
                ws.removeEventListener('message', onm);
                if (d.error) reject(d.error);
                else resolve(d.result);
            }
        };
        ws.addEventListener('message', onm);
        ws.send(JSON.stringify({ id: reqId, method: m, params: p }));
    });
    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Seek to 0.62
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.62);` });
    await new Promise(r => setTimeout(r, 800));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/snap_stop4_bathroom_new.png', Buffer.from(shot.data, 'base64'));
    ws.close();
    console.log('Saved snap_stop4_bathroom_new.png');
}

captureBath().catch(console.error);
