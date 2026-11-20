// test_and_capture_photorealism.mjs
import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\ba763b61-d8cc-448d-88e4-7b9f23b03879';

async function main() {
    console.log('Connecting to Chrome DevTools...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
    if (!pageTarget) {
        pageTarget = targets.find(t => t.type === 'page');
    }

    if (!pageTarget) {
        console.error('No page target found. Targets:', targets);
        process.exit(1);
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
    });

    let msgId = 1;
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = msgId++;
            const handler = (evt) => {
                const data = JSON.parse(evt.data);
                if (data.id === id) {
                    ws.removeEventListener('message', handler);
                    if (data.error) reject(data.error);
                    else resolve(data.result);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    ws.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.method === 'Runtime.exceptionThrown') {
            console.error('BROWSER EXCEPTION:', JSON.stringify(msg.params.exceptionDetails, null, 2));
        } else if (msg.method === 'Runtime.consoleAPICalled') {
            const vals = (msg.params.args || []).map(a => a.value || a.description || '');
            console.log('BROWSER CONSOLE:', vals.join(' '));
        }
    };

    await send('Runtime.enable');
    await send('Page.enable');

    await send('Emulation.setDeviceMetricsOverride', {
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating page to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });

    // Wait 4 seconds for Three.js, textures, and GLTF models to load
    await new Promise(r => setTimeout(r, 4500));

    async function evalCode(expr) {
        return await send('Runtime.evaluate', {
            expression: expr,
            awaitPromise: true,
            returnByValue: true
        });
    }

    async function capture(filename) {
        const result = await send('Page.captureScreenshot', { format: 'png' });
        const filePath = path.join(BRAIN_DIR, filename);
        fs.writeFileSync(filePath, Buffer.from(result.data, 'base64'));
        console.log(`Saved screenshot: ${filename} (${result.data.length} bytes base64)`);
    }

    // 1. Test Blender GLB Export
    console.log('Testing Blender GLB Export...');
    await evalCode(`
        if (typeof window.exportSceneToGLTF === 'function') {
            window.exportSceneToGLTF({ binary: true });
        }
    `);
    await new Promise(r => setTimeout(r, 2000));

    // Verify export file on disk
    const exportPath = 'd:\\floor plans\\jp-aviva-3d\\jp_north_aviva_blender_export.glb';
    if (fs.existsSync(exportPath)) {
        const stats = fs.statSync(exportPath);
        console.log(`Verified Blender export: ${exportPath} (${(stats.size / 1024).toFixed(1)} KB)`);
    } else {
        console.warn('Blender export file not yet created:', exportPath);
    }

    // 2. Capture Photorealism Stops
    console.log('Capturing Stop 2: Living Room Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.30);
        window.closeRoomCard();
    `);
    await new Promise(r => setTimeout(r, 800));
    await capture('photoreal_stop2_living_hold.png');

    console.log('Capturing Stop 4: Kitchen Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.55);
        window.closeRoomCard();
    `);
    await new Promise(r => setTimeout(r, 800));
    await capture('photoreal_stop4_kitchen_hold.png');

    console.log('Capturing Stop 6: Bedroom Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.79);
        window.closeRoomCard();
    `);
    await new Promise(r => setTimeout(r, 800));
    await capture('photoreal_stop6_bedroom_hold.png');

    console.log('Capturing Stop 7: Balcony Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.98);
        window.closeRoomCard();
    `);
    await new Promise(r => setTimeout(r, 800));
    await capture('photoreal_stop7_balcony_hold.png');

    // Reset to start
    await evalCode(`window.applyProgressToScene(0);`);

    ws.close();
    console.log('Photorealism test and capture complete!');
}

main().catch(console.error);
