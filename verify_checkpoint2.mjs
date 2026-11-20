import fs from 'fs';
import path from 'path';

const CURRENT_BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
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

    await new Promise(r => setTimeout(r, 3000));

    async function evalCode(expr, awaitPromise = false) {
        return await send('Runtime.evaluate', {
            expression: expr,
            awaitPromise: awaitPromise,
            returnByValue: true
        });
    }

    console.log('Waiting for scene models to mount...');
    await evalCode(`
        (async () => {
            if (typeof window.whenModelsReady === 'function') {
                await window.whenModelsReady();
            } else {
                await new Promise(r => setTimeout(r, 2000));
            }
        })()
    `, true);

    await new Promise(r => setTimeout(r, 1000));

    async function capture(filename) {
        const result = await send('Page.captureScreenshot', { format: 'png' });
        const brainPath = path.join(CURRENT_BRAIN_DIR, filename);
        const localPath = path.join(LOCAL_DIR, filename);
        fs.writeFileSync(brainPath, Buffer.from(result.data, 'base64'));
        fs.writeFileSync(localPath, Buffer.from(result.data, 'base64'));
        console.log(`Saved screenshot: ${filename}`);
    }

    const stops = [
        { name: 'cp2_step3a_kitchen_entry.png', progress: 0.32, desc: 'Step 3A: Gliding through central passage into Kitchen Alcove at eye height 1.6m' },
        { name: 'cp2_step3b_kitchen_hold.png', progress: 0.38, desc: 'Step 3B: Kitchen Alcove Hold (Jet Black Quartz, Oak cabinets, Subway tiles, Sink)' },
        { name: 'cp2_step4a_bathroom_entry.png', progress: 0.46, desc: 'Step 4A: Stepping into Bathroom doorway at eye height 1.6m' },
        { name: 'cp2_step4b_bathroom_hold.png', progress: 0.52, desc: 'Step 4B: Designer Bathroom & W.C. Suite Hold (Slate tiles, Backlit vanity mirror, Shower)' }
    ];

    for (const s of stops) {
        console.log(`--- Jump to ${s.desc} ---`);
        await evalCode(`window.applyProgressToScene(${s.progress});`);
        await new Promise(r => setTimeout(r, 1500));
        await capture(s.name);
    }

    console.log('All Checkpoint 2 captures completed successfully!');
    ws.close();
}

main().catch(err => {
    console.error('Fatal error in verify_checkpoint2:', err);
    process.exit(1);
});
