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

    console.log('Navigating to http://localhost:8080...');
    await send('Page.navigate', { url: 'http://localhost:8080' });
    await new Promise(r => setTimeout(r, 4500));

    console.log('Warming up shaders...');
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            if (window.closeRoomCard) window.closeRoomCard();
            if (window.jumpToStop) window.jumpToStop(5, true);
            if (window.applyProgressToScene) window.applyProgressToScene(0.74);
        `
    });
    await new Promise(r => setTimeout(r, 1500));

    const bedroomProgresses = [
        { name: 'verify_bedroom_074', p: 0.74, desc: 'Master Bedroom Suite 74% - Drapery, Reclined Pillows, Draped Knit Throw, Clean Wall' },
        { name: 'verify_bedroom_076', p: 0.76, desc: 'Master Bedroom Suite 76% - Full Architectural View' }
    ];

    for (const s of bedroomProgresses) {
        console.log(`Setting progress to ${s.p} (${s.name})...`);
        await send('Runtime.evaluate', {
            expression: `
                if (window.applyProgressToScene) {
                    window.applyProgressToScene(${s.p});
                }
            `
        });
        await new Promise(r => setTimeout(r, 1200));

        const snap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 94 });
        const buf = Buffer.from(snap.data, 'base64');

        const localFile = path.join(LOCAL_DIR, `${s.name}.jpg`);
        const brainFile = path.join(BRAIN_DIR, `${s.name}.jpg`);

        fs.writeFileSync(localFile, buf);
        fs.writeFileSync(brainFile, buf);
        console.log(`[OK] Saved ${s.name}.jpg (${s.desc})`);
    }

    ws.close();
    console.log('Bedroom snapshot capture complete!');
}

main().catch(err => {
    console.error('Error during bedroom snapshot capture:', err);
    process.exit(1);
});
