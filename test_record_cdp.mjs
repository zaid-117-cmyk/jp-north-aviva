import fs from 'fs';
import path from 'path';

const FRAMES_DIR = 'D:\\floor plans\\jp-aviva-3d\\test_frames';
if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

async function test() {
    console.log('Connecting to Chrome DevTools on port 9222...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
    if (!pageTarget) pageTarget = targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found. Targets:', targets);
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

    console.log('Navigating page to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Hide unnecessary interactive buttons for presentation
    await send('Runtime.evaluate', {
        expression: `
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            const btn = document.getElementById('room-plus-btn');
            if (btn) btn.style.display = 'none';
            const card = document.getElementById('room-card');
            if (card) card.style.display = 'none';
            renderer.setSize(1920, 1080);
            composer.setSize(1920, 1080);
            camera.aspect = 1920 / 1080;
            camera.updateProjectionMatrix();
        `
    });

    console.log('Testing 5 frame captures...');
    for (let i = 0; i < 5; i++) {
        const t0 = Date.now();
        const p = i * 0.2;
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p});` });
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
        const filePath = path.join(FRAMES_DIR, `test_frame_${i}.jpg`);
        fs.writeFileSync(filePath, Buffer.from(shot.data, 'base64'));
        const dt = Date.now() - t0;
        console.log(`Frame ${i} captured at progress ${p} in ${dt}ms (${shot.data.length} bytes base64)`);
    }

    console.log('Test completed successfully!');
    ws.close();
}

test().catch(err => {
    console.error('Test error:', err);
    process.exit(1);
});
