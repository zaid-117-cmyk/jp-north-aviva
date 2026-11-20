import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';

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
    console.log('Applying scene progress 0.46...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.46);` });
    await new Promise(r => setTimeout(r, 1500));

    const shots = [
        { name: 'kitchen_overhaul_046', p: 0.46 },
        { name: 'kitchen_overhaul_049', p: 0.49 }
    ];

    for (const s of shots) {
        console.log(`Capturing ${s.name} at p=${s.p}...`);
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${s.p});` });
        await new Promise(r => setTimeout(r, 1000));
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 95 });
        
        const localPath = path.join(LOCAL_DIR, `${s.name}.jpg`);
        const brainPath = path.join(BRAIN_DIR, `${s.name}.jpg`);
        const buf = Buffer.from(shot.data, 'base64');
        
        fs.writeFileSync(localPath, buf);
        fs.writeFileSync(brainPath, buf);
        console.log(`Saved ${localPath} and ${brainPath} (${buf.length} bytes)`);
    }

    ws.close();
    console.log('Done capturing kitchen snapshots!');
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
