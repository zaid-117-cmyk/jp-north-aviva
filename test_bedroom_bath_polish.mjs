import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';

async function main() {
    console.log('Connecting to Chrome on port 9222...');
    let targets = null;
    for (let attempt = 0; attempt < 20; attempt++) {
        try {
            const res = await fetch('http://127.0.0.1:9222/json');
            targets = await res.json();
            if (targets && targets.length > 0) break;
        } catch (e) {
            await new Promise(r => setTimeout(r, 500));
        }
    }

    if (!targets) {
        console.error('No page target found on port 9222');
        process.exit(1);
    }

    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

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
    console.log('Warming up shaders at p = 0.60...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.60);` });
    await new Promise(r => setTimeout(r, 1200));

    const shots = [
        { name: 'bathroom_overhaul_060', p: 0.60 },
        { name: 'bathroom_overhaul_062', p: 0.625 },
        { name: 'bedroom_entry_068', p: 0.68 },
        { name: 'bedroom_overhaul_074', p: 0.74 },
        { name: 'bedroom_overhaul_076', p: 0.76 }
    ];

    for (const s of shots) {
        console.log(`Capturing ${s.name} at p=${s.p}...`);
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${s.p});` });
        await new Promise(r => setTimeout(r, 800));
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 95 });
        
        const localPath = path.join(LOCAL_DIR, `${s.name}.jpg`);
        const brainPath = path.join(BRAIN_DIR, `${s.name}.jpg`);
        const buf = Buffer.from(shot.data, 'base64');
        
        fs.writeFileSync(localPath, buf);
        fs.writeFileSync(brainPath, buf);
        console.log(`Saved ${s.name}.jpg (${buf.length} bytes)`);
    }

    ws.close();
    console.log('All snapshots captured successfully!');
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
