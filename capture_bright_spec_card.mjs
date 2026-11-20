import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) process.exit(1);

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
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false
    });

    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Living Room with Spec Card Open
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            window.applyProgressToScene(0.32);
            window.setGlobalUnit('metric');
            window.openRoomCard(2);
        `
    });
    await new Promise(r => setTimeout(r, 1200));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(BRAIN_DIR, 'bright_spec_card_living.png'), Buffer.from(shot.data, 'base64'));
    fs.writeFileSync(path.join(LOCAL_DIR, 'bright_spec_card_living.png'), Buffer.from(shot.data, 'base64'));
    console.log('Saved bright_spec_card_living.png');
    ws.close();
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
