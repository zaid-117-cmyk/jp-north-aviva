import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

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
        console.error('Could not connect to Chrome port 9222');
        process.exit(1);
    }
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

    const checkPoints = [0.66, 0.67, 0.68, 0.69, 0.70, 0.72];

    for (const p of checkPoints) {
        const camInfo = await send('Runtime.evaluate', {
            expression: `
                window.applyProgressToScene(${p});
                JSON.stringify({
                    pos: { x: camera.position.x, y: camera.position.y, z: camera.position.z },
                    target: { x: controls.target.x, y: controls.target.y, z: controls.target.z },
                    camState: { ...camState }
                });
            `,
            returnByValue: true
        });
        console.log(`p = ${p}:`, camInfo.result.value);

        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
        const outPath = path.join(BRAIN_DIR, `entry_test_${Math.round(p * 100)}.jpg`);
        fs.writeFileSync(outPath, Buffer.from(shot.data, 'base64'));
    }

    ws.close();
    console.log('Done test_bedroom_entry');
}

main().catch(console.error);
