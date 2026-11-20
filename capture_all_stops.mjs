import fs from 'fs';
import path from 'path';

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
    await new Promise(r => setTimeout(r, 1200));

    const stops = [
        { p: 0.05, name: 'snap_stop0_blueprint' },
        { p: 0.16, name: 'snap_stop1_walls_rising' },
        { p: 0.32, name: 'snap_stop2_living' },
        { p: 0.48, name: 'snap_stop3_kitchen' },
        { p: 0.62, name: 'snap_stop4_bathroom' },
        { p: 0.76, name: 'snap_stop5_bedroom' },
        { p: 0.90, name: 'snap_stop6_balcony' },
        { p: 0.98, name: 'snap_stop7_sunset' }
    ];

    for (const s of stops) {
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${s.p});` });
        await new Promise(r => setTimeout(r, 400));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const filePath = path.join(BRAIN_DIR, `${s.name}.png`);
        fs.writeFileSync(filePath, Buffer.from(shot.data, 'base64'));
        console.log(`Saved ${s.name}.png`);
    }

    ws.close();
}

main().catch(console.error);
