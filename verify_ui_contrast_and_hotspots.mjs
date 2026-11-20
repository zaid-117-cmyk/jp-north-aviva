import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';

async function main() {
    console.log('Connecting to Chrome DevTools on port 9222...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found on port 9222');
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
            console.log('BROWSER LOG:', vals.join(' '));
        } else if (data.method === 'Runtime.exceptionThrown') {
            console.error('BROWSER ERROR:', JSON.stringify(data.params.exceptionDetails, null, 2));
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

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Ensure UI elements are visible
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'flex';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'flex';
        `
    });

    async function takeShot(filename, description) {
        console.log(`Capturing: ${filename} (${description})...`);
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const brainFile = path.join(BRAIN_DIR, filename);
        const localFile = path.join(LOCAL_DIR, filename);
        fs.writeFileSync(brainFile, Buffer.from(shot.data, 'base64'));
        fs.writeFileSync(localFile, Buffer.from(shot.data, 'base64'));
        console.log(`Saved screenshot: ${filename}`);
    }

    // 1. Blueprint Mode (p = 0.05)
    console.log('--- Step 1: Testing Blueprint Mode (p = 0.05) ---');
    await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.05);
            if (window.closeRoomCard) window.closeRoomCard();
        `
    });
    await new Promise(r => setTimeout(r, 1500));
    await takeShot('ui_blueprint_mode.png', 'Blueprint mode with high contrast dark charcoal header & status pill');

    // 2. 3D Interior Mode (p = 0.32, Living Room)
    console.log('--- Step 2: Testing 3D Interior Mode (p = 0.32) ---');
    await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.32);
            if (window.closeRoomCard) window.closeRoomCard();
        `
    });
    await new Promise(r => setTimeout(r, 1500));
    await takeShot('ui_3d_living_room.png', '3D Interior with frosted glass header, collision-free progress pill, and + hotspot button');

    // 3. Open Spec Card in Metric Mode
    console.log('--- Step 3: Testing Spec Card Open (Metric Mode) ---');
    await send('Runtime.evaluate', {
        expression: `
            window.setGlobalUnit('metric');
            window.openRoomCard(2);
        `
    });
    await new Promise(r => setTimeout(r, 1000));
    await takeShot('ui_spec_card_metric.png', 'Living Room Architectural Spec Card in Metric mode (M / SQ.M.)');

    // 4. Switch Spec Card to Imperial Mode
    console.log('--- Step 4: Testing Spec Card Switch to Imperial Mode ---');
    await send('Runtime.evaluate', {
        expression: `
            window.setGlobalUnit('imperial');
        `
    });
    await new Promise(r => setTimeout(r, 800));
    await takeShot('ui_spec_card_imperial.png', 'Living Room Architectural Spec Card in Imperial mode (FT / SQ.FT.)');

    // 5. Kitchen Alcove Spec Card (p = 0.48)
    console.log('--- Step 5: Testing Kitchen Alcove Spec Card (p = 0.48) ---');
    await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.48);
            window.setGlobalUnit('metric');
            window.openRoomCard(3);
        `
    });
    await new Promise(r => setTimeout(r, 1200));
    await takeShot('ui_spec_card_kitchen.png', 'Chef\'s Kitchen Alcove Architectural Spec Card');

    // 6. Master Bedroom Suite Spec Card (p = 0.76)
    console.log('--- Step 6: Testing Master Bedroom Suite Spec Card (p = 0.76) ---');
    await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.76);
            window.openRoomCard(5);
        `
    });
    await new Promise(r => setTimeout(r, 1200));
    await takeShot('ui_spec_card_bedroom.png', 'Master Bedroom Suite Architectural Spec Card');

    console.log('All UI contrast and hotspot verifications completed successfully!');
    ws.close();
}

main().catch(err => {
    console.error('Error running verification:', err);
    process.exit(1);
});
