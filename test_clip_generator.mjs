import fs from 'fs';
import path from 'path';

const FRAMES_DIR = 'D:\\floor plans\\jp-aviva-3d\\test_clip_frames';
if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

async function main() {
    console.log('Connecting to Chrome...');
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

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1280,
        height: 720,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 3500));

    // Setup presentation styling
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            const btn = document.getElementById('room-plus-btn');
            if (btn) btn.style.display = 'none';
            const card = document.getElementById('room-card');
            if (card) card.style.display = 'none';
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        `
    });

    // Warm-up compile frame
    console.log('Warm-up frame...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.20);` });

    const totalFrames = 30;
    console.log(`Capturing ${totalFrames} frames from p=0.16 to p=0.28 (Living Room entry)...`);
    for (let i = 0; i < totalFrames; i++) {
        const p = 0.16 + (i / (totalFrames - 1)) * (0.28 - 0.16);
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p});` });
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
        const numStr = String(i).padStart(4, '0');
        fs.writeFileSync(path.join(FRAMES_DIR, `frame_${numStr}.jpg`), Buffer.from(shot.data, 'base64'));
    }
    console.log('Capture done!');
    ws.close();
}

main().catch(console.error);
