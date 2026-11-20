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

    async function capture(filename) {
        const result = await send('Page.captureScreenshot', { format: 'png' });
        const brainPath = path.join(CURRENT_BRAIN_DIR, filename);
        const localPath = path.join(LOCAL_DIR, filename);
        fs.writeFileSync(brainPath, Buffer.from(result.data, 'base64'));
        fs.writeFileSync(localPath, Buffer.from(result.data, 'base64'));
        console.log(`Saved screenshot: ${filename}`);
    }

    const stops = [
        { name: 'prod_stop0_plan_sheet.png', progress: 0.04, desc: 'Stop 0: 2D Flat Architectural Plan Sheet (3D Section Cut at 1.2m)' },
        { name: 'prod_stop1_walls_rising.png', progress: 0.12, desc: 'Stop 1: Walls Rising to 2.85m, Ceiling Locks in, Front Door Descent' },
        { name: 'prod_stop2_living_room.png', progress: 0.25, desc: 'Stop 2: Living & Dining Sanctuary (Habitable Room)' },
        { name: 'prod_stop3_kitchen_alcove.png', progress: 0.39, desc: 'Stop 3: Kitchen Alcove (Jet Black Quartz & Scandinavian Oak)' },
        { name: 'prod_stop4_bathroom_suite.png', progress: 0.53, desc: 'Stop 4: Designer Bathroom & W.C. Suite' },
        { name: 'prod_stop5_master_bedroom.png', progress: 0.67, desc: 'Stop 5: Master Bedroom Suite ("Wild Mushroom" Headboard)' },
        { name: 'prod_stop6_balcony_deck.png', progress: 0.85, desc: 'Stop 6: Enclosed Balcony Deck' },
        { name: 'prod_stop7_sunset_finale.png', progress: 0.98, desc: 'Stop 7: Golden Mumbai Sunset Grand Finale' }
    ];

    for (const s of stops) {
        console.log(`--- Jump to ${s.desc} (progress: ${s.progress}) ---`);
        await evalCode(`window.applyProgressToScene(${s.progress});`);
        await new Promise(r => setTimeout(r, 1500));
        await capture(s.name);
    }

    console.log('All production walkthrough captures completed successfully!');
    ws.close();
}

main().catch(err => {
    console.error('Fatal error in capture_production_walkthrough:', err);
    process.exit(1);
});
