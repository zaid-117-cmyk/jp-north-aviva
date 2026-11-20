import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    console.log('Connecting to Chrome on port 9222...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found on port 9222');
        process.exit(1);
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
    });

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

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Warmup
    console.log('Applying scene progress 0.74...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.74);` });
    await new Promise(r => setTimeout(r, 1200));

    const shots = [
        { name: 'bedroom_overhaul_074', p: 0.74 },
        { name: 'bedroom_overhaul_076', p: 0.76 },
        { name: 'balcony_overhaul_088', p: 0.88 },
        { name: 'balcony_overhaul_090', p: 0.90 },
        { name: 'sunset_finale_096', p: 0.96 }
    ];

    for (const s of shots) {
        console.log(`Capturing ${s.name} at p=${s.p}...`);
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${s.p});` });
        await new Promise(r => setTimeout(r, 800));
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 95 });
        const outPath = path.join(BRAIN_DIR, `${s.name}.jpg`);
        fs.writeFileSync(outPath, Buffer.from(shot.data, 'base64'));
        console.log(`Saved ${outPath} (${fs.statSync(outPath).size} bytes)`);
    }

    ws.close();
    console.log('Done capturing bedroom and balcony snapshots!');
}

main().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
