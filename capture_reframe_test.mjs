import fs from 'fs';
import path from 'path';

const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';
const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

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
        }
    };

    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = msgId++;
            pending.set(id, { resolve, reject });
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    async function evaluate(expr) {
        const res = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
        return res.result ? res.result.value : null;
    }

    async function takeScreenshot(filename) {
        const res = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(res.data, 'base64');
        const localPath = path.join(LOCAL_DIR, filename);
        const brainPath = path.join(BRAIN_DIR, filename);
        fs.writeFileSync(localPath, buf);
        fs.writeFileSync(brainPath, buf);
        console.log(`Saved screenshot: ${filename} (${(buf.length / 1024).toFixed(1)} KB)`);
    }

    await evaluate(`
        window.isCapturing = true;
        if (window.closeRoomCard) window.closeRoomCard();
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    const testStops = [
        { p: 0.42, name: 'reframe_transition_38_44_living_to_kitchen.png', desc: 'Transition Living to Kitchen Portal' },
        { p: 0.48, name: 'reframe_stop3_gourmet_kitchen.png', desc: 'Stop 3: Kitchen Alcove Presentation' },
        { p: 0.55, name: 'reframe_transition_kitchen_to_bath.png', desc: 'Transition Kitchen to Bathroom Doorway' },
        { p: 0.62, name: 'reframe_stop4_designer_bath.png', desc: 'Stop 4: Designer Bathroom Suite' },
        { p: 0.70, name: 'reframe_transition_bath_to_bedroom.png', desc: 'Transition Bath to Bedroom Doorway' },
        { p: 0.76, name: 'reframe_stop5_master_bedroom_reframed.png', desc: 'Stop 5: Master Bedroom Re-Framed Eye-Level Diagonal' },
        { p: 0.85, name: 'reframe_transition_bedroom_to_balcony.png', desc: 'Transition Bedroom to Balcony Open Sliders' },
        { p: 0.90, name: 'reframe_stop6_balcony_deck_reframed.png', desc: 'Stop 6: Balcony Deck Re-Framed Level Horizon' },
        { p: 0.98, name: 'reframe_stop7_sunset_finale.png', desc: 'Stop 7: Mumbai Sunset Finale' }
    ];

    for (const item of testStops) {
        await evaluate(`window.applyProgressToScene(${item.p})`);
        await new Promise(r => setTimeout(r, 600));
        const camData = await evaluate(`(() => {
            const s = window.camState || {};
            return {
                p: ${item.p},
                pos: { x: +(s.posX || 0).toFixed(2), y: +(s.posY || 0).toFixed(2), z: +(s.posZ || 0).toFixed(2) },
                target: { x: +(s.targetX || 0).toFixed(2), y: +(s.targetY || 0).toFixed(2), z: +(s.targetZ || 0).toFixed(2) },
                fov: +(s.fov || 0).toFixed(1)
            };
        })()`);
        console.log(`[${item.desc}] (p=${item.p}): Pos=(${camData.pos.x}, ${camData.pos.y}, ${camData.pos.z}), Target=(${camData.target.x}, ${camData.target.y}, ${camData.target.z}), FOV=${camData.fov}`);
        await takeScreenshot(item.name);
    }

    ws.close();
    console.log('\n[COMPLETE] All test screenshots captured and saved to disk & brain!');
}

main().catch(err => {
    console.error('Test capture error:', err);
    process.exit(1);
});
