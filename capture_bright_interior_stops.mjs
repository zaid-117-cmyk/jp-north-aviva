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
    await new Promise(r => setTimeout(r, 4500));

    // Warm up and set UI controls
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            if (window.closeRoomCard) window.closeRoomCard();
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'flex';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'flex';
        `
    });

    const stops = [
        { name: 'bright_stop0_plan_sheet.png', p: 0.05, desc: 'Stop 0: 2D Blueprint Plan Sheet (1:50)' },
        { name: 'bright_stop1_walls_rising.png', p: 0.16, desc: 'Stop 1: Walls Rise to 2.85m & Front Door Open' },
        { name: 'bright_stop2_living_room.png', p: 0.32, desc: 'Stop 2: Living Room (Warm Plaster #EAE6DF, Cove Light #FFE4B5, 10cm Skirting, Downlights)' },
        { name: 'bright_stop3_kitchen_alcove.png', p: 0.48, desc: 'Stop 3: Kitchen Alcove (Cove Light #FFE4B5, Appliances, Task Downlights)' },
        { name: 'bright_stop4_bathroom_suite.png', p: 0.62, desc: 'Stop 4: Bathroom Suite (Halo Mirror, Charcoal Slate Tile, Rain Shower)' },
        { name: 'bright_stop5_master_bedroom.png', p: 0.76, desc: 'Stop 5: Master Bedroom (Cove Light #FFE4B5, Wild Mushroom Accent, Sun Streaming)' },
        { name: 'bright_stop6_balcony_deck.png', p: 0.90, desc: 'Stop 6: Balcony Deck (Golden Sunlight, Washing Machine, Teak Deck)' },
        { name: 'bright_stop7_sunset_finale.png', p: 0.98, desc: 'Stop 7: Mumbai Golden Sunset Grand Finale' }
    ];

    for (const s of stops) {
        console.log(`Rendering ${s.desc} (p=${s.p})...`);
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${s.p});` });
        await new Promise(r => setTimeout(r, 1500));

        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const brainFile = path.join(BRAIN_DIR, s.name);
        const localFile = path.join(LOCAL_DIR, s.name);
        fs.writeFileSync(brainFile, Buffer.from(shot.data, 'base64'));
        fs.writeFileSync(localFile, Buffer.from(shot.data, 'base64'));
        console.log(`Saved screenshot: ${s.name}`);
    }

    console.log('All bright interior stop screenshots captured successfully!');
    ws.close();
}

main().catch(err => {
    console.error('Error running capture:', err);
    process.exit(1);
});
