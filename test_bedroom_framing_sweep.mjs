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

    async function testBed(posX, posY, posZ, targetX, targetY, targetZ, fov, name) {
        await send('Runtime.evaluate', {
            expression: `
                window.applyProgressToScene(0.76);
                camState.posX = ${posX};
                camState.posY = ${posY};
                camState.posZ = ${posZ};
                camState.targetX = ${targetX};
                camState.targetY = ${targetY};
                camState.targetZ = ${targetZ};
                camState.fov = ${fov};
                camera.position.set(${posX}, ${posY}, ${posZ});
                camera.lookAt(${targetX}, ${targetY}, ${targetZ});
                camera.fov = ${fov};
                camera.updateProjectionMatrix();
                clipHeightPlane.constant = 50.0;
                composer.render();
            `
        });
        await new Promise(r => setTimeout(r, 400));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const filePath = path.join(BRAIN_DIR, `${name}.png`);
        fs.writeFileSync(filePath, Buffer.from(shot.data, 'base64'));
        console.log(`Saved ${name}.png`);
    }

    // Test 3 subtle variations:
    await testBed(-1.92, 1.50, -0.25, -3.35, 1.15, -1.10, 52, 'test_bed_angle_A');
    await testBed(-1.88, 1.50, -0.22, -3.30, 1.15, -1.18, 52, 'test_bed_angle_B');
    await testBed(-1.95, 1.50, -0.28, -3.35, 1.15, -1.05, 54, 'test_bed_angle_C');

    ws.close();
}

main().catch(console.error);
