import fs from 'fs';
import path from 'path';

const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';
const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

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
        return new Promise(resolve => {
            const id = msgId++;
            pending.set(id, resolve);
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    async function evaluate(expr) {
        return (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).value;
    }

    async function shot(filename) {
        const r = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(r.data, 'base64');
        fs.writeFileSync(path.join(LOCAL_DIR, filename), buf);
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        console.log(`Saved ${filename}`);
    }

    await evaluate(`
        window.isCapturing = true;
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
        window.applyProgressToScene(0.76);
    `);

    // Angle 1: posX: -2.00, posY: 1.45, posZ: -0.55 | target: -3.20, 1.15, -0.75 | fov: 66
    await evaluate(`
        camState.posX = -2.00; camState.posY = 1.45; camState.posZ = -0.55;
        camState.targetX = -3.20; camState.targetY = 1.15; camState.targetZ = -0.75;
        camState.fov = 66.0;
        camera.fov = 66.0;
        camera.updateProjectionMatrix();
        camera.position.set(-2.00, 1.45, -0.55);
        camera.lookAt(-3.20, 1.15, -0.75);
        composer.render();
    `);
    await new Promise(r => setTimeout(r, 400));
    await shot('test_bed_angle1.png');

    // Angle 2: posX: -2.05, posY: 1.45, posZ: -0.35 | target: -3.25, 1.15, -0.65 | fov: 70
    await evaluate(`
        camState.posX = -2.05; camState.posY = 1.45; camState.posZ = -0.35;
        camState.targetX = -3.25; camState.targetY = 1.15; camState.targetZ = -0.65;
        camState.fov = 70.0;
        camera.fov = 70.0;
        camera.updateProjectionMatrix();
        camera.position.set(-2.05, 1.45, -0.35);
        camera.lookAt(-3.25, 1.15, -0.65);
        composer.render();
    `);
    await new Promise(r => setTimeout(r, 400));
    await shot('test_bed_angle2.png');

    // Angle 3: posX: -2.10, posY: 1.45, posZ: -0.25 | target: -3.30, 1.10, -0.85 | fov: 68
    await evaluate(`
        camState.posX = -2.10; camState.posY = 1.45; camState.posZ = -0.25;
        camState.targetX = -3.30; camState.targetY = 1.10; camState.targetZ = -0.85;
        camState.fov = 68.0;
        camera.fov = 68.0;
        camera.updateProjectionMatrix();
        camera.position.set(-2.10, 1.45, -0.25);
        camera.lookAt(-3.30, 1.10, -0.85);
        composer.render();
    `);
    await new Promise(r => setTimeout(r, 400));
    await shot('test_bed_angle3.png');

    ws.close();
}

main();
