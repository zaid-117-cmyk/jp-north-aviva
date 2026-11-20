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

    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
            window.applyProgressToScene(0.76);
        `
    });

    async function testBed(posX, posY, posZ, targetX, targetY, targetZ, fov, name) {
        await send('Runtime.evaluate', {
            expression: `
                camera.position.set(${posX}, ${posY}, ${posZ});
                camera.fov = ${fov};
                camera.updateProjectionMatrix();
                camera.lookAt(${targetX}, ${targetY}, ${targetZ});
                composer.render();
            `
        });
        await new Promise(r => setTimeout(r, 200));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(shot.data, 'base64');
        fs.writeFileSync(path.join(LOCAL_DIR, name), buf);
        fs.writeFileSync(path.join(BRAIN_DIR, name), buf);
        console.log(`Saved ${name}`);
    }

    // Angle A: foot of bed looking toward headboard
    await testBed(-2.10, 1.45, -1.85, -3.05, 1.15, 0.15, 62, 'test_bed_headboard_view.png');
    // Angle B: wider diagonal
    await testBed(-2.00, 1.45, -1.60, -3.15, 1.15, 0.15, 65, 'test_bed_diagonal_wide.png');

    ws.close();
}

main().catch(console.error);
