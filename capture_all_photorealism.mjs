// capture_all_photorealism.mjs
import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\ba763b61-d8cc-448d-88e4-7b9f23b03879';
const LOCAL_DIR = 'd:\\floor plans\\jp-aviva-3d';

async function main() {
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
        } else if (data.method === 'Runtime.consoleAPICalled') {
            const vals = (data.params.args || []).map(a => a.value || a.description || '');
            console.log('BROWSER CONSOLE:', vals.join(' '));
        } else if (data.method === 'Runtime.exceptionThrown') {
            console.error('BROWSER EXCEPTION:', JSON.stringify(data.params.exceptionDetails, null, 2));
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
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating page to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });

    // Wait 2.5s for initial assets
    await new Promise(r => setTimeout(r, 2500));

    async function evalCode(expr, awaitPromise = false) {
        return await send('Runtime.evaluate', {
            expression: expr,
            awaitPromise: awaitPromise,
            returnByValue: true
        });
    }

    console.log('Waiting for all Poly Haven CC0 3D models to finish loading...');
    await evalCode(`
        (async () => {
            if (typeof window.whenModelsReady === 'function') {
                await window.whenModelsReady();
            } else {
                await new Promise(r => setTimeout(r, 3000));
            }
        })()
    `, true);
    console.log('All 3D models ready in Three.js scene!');

    // Wait 1.5s for materials and shaders to settle
    await new Promise(r => setTimeout(r, 1500));

    async function takeScreenshot(filename) {
        const result = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(result.data, 'base64');
        const brainPath = path.join(BRAIN_DIR, filename);
        const localPath = path.join(LOCAL_DIR, filename);
        fs.writeFileSync(brainPath, buf);
        fs.writeFileSync(localPath, buf);
        console.log(`Saved screenshot: ${filename} (${buf.length} bytes) to both brain and local dirs.`);
    }

    // 1. Capture Stop 2: Living Room Hold
    console.log('Capturing Stop 2: Living Room Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.30);
        window.closeRoomCard();
    `, false);
    await new Promise(r => setTimeout(r, 1200));
    await takeScreenshot('photoreal_stop2_living_hold.png');

    // 2. Capture Stop 4: Kitchen Hold
    console.log('Capturing Stop 4: Kitchen Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.55);
        window.closeRoomCard();
    `, false);
    await new Promise(r => setTimeout(r, 1200));
    await takeScreenshot('photoreal_stop4_kitchen_hold.png');

    // 3. Capture Stop 6: Bedroom Hold
    console.log('Capturing Stop 6: Bedroom Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.79);
        window.closeRoomCard();
    `, false);
    await new Promise(r => setTimeout(r, 1200));
    await takeScreenshot('photoreal_stop6_bedroom_hold.png');

    // 4. Capture Stop 7: Balcony Hold
    console.log('Capturing Stop 7: Balcony Hold (Photorealism Upgrade)...');
    await evalCode(`
        window.applyProgressToScene(0.98);
        window.closeRoomCard();
    `, false);
    await new Promise(r => setTimeout(r, 1200));
    await takeScreenshot('photoreal_stop7_balcony_hold.png');

    // Reset to start
    await evalCode(`window.applyProgressToScene(0);`, false);

    ws.close();
    console.log('ALL PHOTOREALISM CAPTURES COMPLETED SUCCESSFULLY!');
}

main().catch(console.error);
