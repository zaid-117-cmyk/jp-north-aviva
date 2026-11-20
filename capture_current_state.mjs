import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found');
        process.exit(1);
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((r, e) => { ws.onopen = r; ws.onerror = e; });

    let id = 1;
    const pending = new Map();
    ws.onmessage = (evt) => {
        const d = JSON.parse(evt.data);
        if (d.id && pending.has(d.id)) {
            const { resolve, reject } = pending.get(d.id);
            pending.delete(d.id);
            if (d.error) reject(d.error);
            else resolve(d.result);
        }
    };
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const reqId = id++;
            pending.set(reqId, { resolve, reject });
            ws.send(JSON.stringify({ id: reqId, method, params }));
        });
    }

    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 3000));

    async function capture(p, filename) {
        await send('Runtime.evaluate', {
            expression: `window.applyProgressToScene(${p});`,
            returnByValue: true
        });
        await new Promise(r => setTimeout(r, 400));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(shot.data, 'base64');
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        fs.writeFileSync(path.join('D:\\floor plans\\jp-aviva-3d', filename), buf);
        console.log(`Saved ${filename} at progress ${p}`);
    }

    await capture(0.35, 'diag_trans_19s.png');
    await capture(0.48, 'diag_trans_26s.png');
    await capture(0.62, 'diag_stop4_bathroom.png');
    await capture(0.68, 'diag_trans_34s.png');
    await capture(0.81, 'diag_trans_44s.png');

    ws.close();
}

main().catch(console.error);
