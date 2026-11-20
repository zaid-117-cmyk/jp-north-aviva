import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found');
        process.exit(1);
    }

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
    await new Promise(r => setTimeout(r, 1200));

    async function testCam(p, posX, posY, posZ, targetX, targetY, targetZ, fov, name) {
        await send('Runtime.evaluate', {
            expression: `
                window.applyProgressToScene(${p});
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

    // Bedroom options at doorway:
    // Bed is centered at x = -2.95, z = -0.95. Headboard is at z = 0.18.
    // Wardrobe is at x = -3.95, z = -1.50.
    // Window is at z = -2.36, x = -3.05.
    // Doorway is at x = -1.825, z = -0.20.
    
    // Opt 1: Right at doorway threshold, FOV 50, Y = 1.5m, looking diagonally across
    await testCam(0.76, -1.85, 1.50, -0.25, -3.40, 1.05, -1.50, 50, 'test_bed_opt1_doorway');
    
    // Opt 2: Just inside doorway at x = -1.95, z = -0.35, aiming more toward headboard & window
    await testCam(0.76, -1.95, 1.50, -0.35, -3.20, 1.05, -1.30, 50, 'test_bed_opt2_inside');

    // Opt 3: At doorway x = -1.85, z = -0.30, aiming wider target
    await testCam(0.76, -1.85, 1.50, -0.30, -3.35, 1.10, -1.40, 52, 'test_bed_opt3_wide');

    // Opt 4: Slightly back in passage looking through door arch
    await testCam(0.76, -1.65, 1.50, -0.20, -3.45, 1.05, -1.45, 52, 'test_bed_opt4_passage');

    // Balcony options:
    // Current parapet height test:
    // Opt 1: Step closer to window (posZ = -1.85), Y = 1.55m
    await testCam(0.90, 1.35, 1.55, -1.85, 1.55, 1.45, -5.5, 60, 'test_balcony_opt1_closer');

    // Opt 2: Step closer (posZ = -1.95), Y = 1.55m, level horizon
    await testCam(0.90, 1.40, 1.55, -1.95, 1.50, 1.50, -6.5, 58, 'test_balcony_opt2_level');

    ws.close();
    console.log('Testing complete!');
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
