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
            window.applyProgressToScene(0.50);
            pbrCeilingMat.side = THREE.FrontSide;
            camera.position.set(-0.85, 3.15, -0.20);
            camera.lookAt(-1.18, 1.15, 0.80);
            camera.fov = 58.0;
            camera.updateProjectionMatrix();
            renderer.render(scene, camera);
        `
    });

    await new Promise(r => setTimeout(r, 600));
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(BRAIN_DIR, 'test_aerial_315.png'), Buffer.from(shot.data, 'base64'));
    console.log('Saved test_aerial_315.png');
    ws.close();
}

main().catch(console.error);
