import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

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
    await new Promise(r => setTimeout(r, 4500));

    async function evaluate(expr) {
        return (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).value;
    }

    async function capture(filename) {
        const r = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(r.data, 'base64');
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        console.log(`Saved ${filename}`);
    }

    await evaluate(`
        window.isCapturing = true;
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    const tests = [
        { name: 'bed_entrance_optA', posX: -1.55, posY: 1.50, posZ: -0.20, targetX: -3.10, targetY: 1.10, targetZ: -1.05, fov: 52.0 },
        { name: 'bed_entrance_optB', posX: -1.65, posY: 1.50, posZ: -0.28, targetX: -3.15, targetY: 1.10, targetZ: -1.15, fov: 52.0 },
        { name: 'bed_entrance_optC', posX: -1.50, posY: 1.50, posZ: -0.15, targetX: -3.05, targetY: 1.10, targetZ: -0.95, fov: 52.0 }
    ];

    for (const t of tests) {
        await evaluate(`
            window.applyProgressToScene(0.76);
            camera.fov = ${t.fov};
            camera.updateProjectionMatrix();
            camera.position.set(${t.posX}, ${t.posY}, ${t.posZ});
            camera.lookAt(${t.targetX}, ${t.targetY}, ${t.targetZ});
            composer.render();
        `);
        await new Promise(r => setTimeout(r, 600));
        await capture(`${t.name}.png`);
    }

    ws.close();
}

main().catch(console.error);
