import fs from 'fs';
import path from 'path';

const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';
const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

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

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1280,
        height: 720,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            if (window.closeRoomCard) window.closeRoomCard();
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        `
    });

    console.log('Warming up shaders at p=0.32...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.32);` });
    await new Promise(r => setTimeout(r, 1500));

    async function snap(p, filename) {
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p});` });
        await new Promise(r => setTimeout(r, 400));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(shot.data, 'base64');
        fs.writeFileSync(path.join(LOCAL_DIR, filename), buf);
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        console.log(`Saved ${filename} (progress ${p})`);
    }

    await snap(0.05, 'snap_stop0_blueprint.png');
    await snap(0.32, 'snap_stop2_living.png');
    await snap(0.48, 'snap_stop3_kitchen.png');
    await snap(0.62, 'snap_stop4_bathroom.png');
    await snap(0.76, 'snap_stop5_bedroom.png');
    await snap(0.90, 'snap_stop6_balcony.png');
    await snap(0.98, 'snap_stop7_sunset.png');

    ws.close();
}

main().catch(console.error);
