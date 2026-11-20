import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:/floor plans/jp-aviva-3d';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    const pending = new Map();
    let msgId = 1;
    ws.onmessage = evt => {
        const d = JSON.parse(evt.data);
        if (d.id && pending.has(d.id)) pending.get(d.id)(d.result);
    };
    function send(method, params = {}) {
        return new Promise((resolve) => {
            const id = msgId++;
            pending.set(id, (res) => resolve(res));
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    // Allow textures, procedural canvases, and shaders to compile
    await new Promise(r => setTimeout(r, 4500));

    async function evaluate(expr) {
        return (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).value;
    }

    async function capture(filename) {
        const r = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(r.data, 'base64');
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        fs.writeFileSync(path.join(LOCAL_DIR, filename), buf);
        console.log(`Saved ${filename}`);
    }

    // Set high quality 1280x720 capture mode
    await evaluate(`
        window.isCapturing = true;
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    // Capture Stop 4: BATH & W.C. at 62%
    await evaluate(`window.applyProgressToScene(0.62);`);
    await new Promise(r => setTimeout(r, 600));
    await capture('snap_stop4_bathroom.png');

    // Capture Stop 5: MASTER BEDROOM at 76%
    await evaluate(`window.applyProgressToScene(0.76);`);
    await new Promise(r => setTimeout(r, 600));
    await capture('snap_stop5_bedroom.png');

    // Capture Stop 6: BALCONY DECK & UTILITY at 90%
    await evaluate(`window.applyProgressToScene(0.90);`);
    await new Promise(r => setTimeout(r, 600));
    await capture('snap_stop6_balcony.png');

    // Capture Stop 7: MUMBAI GOLDEN SUNSET FINALE at 97%
    await evaluate(`window.applyProgressToScene(0.97);`);
    await new Promise(r => setTimeout(r, 600));
    await capture('snap_stop7_sunset.png');

    ws.close();
}

main().catch(console.error);
