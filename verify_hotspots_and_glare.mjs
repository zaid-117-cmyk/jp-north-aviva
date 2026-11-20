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
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    // 1. Living Sanctuary at p = 0.32 (Check furniture opacity & plus button)
    console.log('\nTesting Living Sanctuary (p = 0.32)...');
    await evaluate(`
        if (window.closeRoomCard) window.closeRoomCard();
        window.applyProgressToScene(0.32);
    `);
    await new Promise(r => setTimeout(r, 600));
    await takeScreenshot('test_living_furniture_opacity.png');

    // 2. Open Room Card at Living Sanctuary (Check interactive spec card)
    console.log('\nTesting Interactive Room Spec Card (Living Sanctuary)...');
    await evaluate(`
        window.openRoomCard(2);
    `);
    await new Promise(r => setTimeout(r, 600));
    await takeScreenshot('test_living_spec_card_open_metric.png');

    // 3. Toggle to Imperial units
    console.log('\nTesting Unit Toggle to Imperial...');
    await evaluate(`
        window.setGlobalUnit('imperial');
    `);
    await new Promise(r => setTimeout(r, 400));
    await takeScreenshot('test_living_spec_card_open_imperial.png');

    // 4. Balcony Deck at p = 0.90 (Check bloom, glare reduction, circular bokeh particles)
    console.log('\nTesting Balcony Deck & Sunset Glare (p = 0.90)...');
    await evaluate(`
        if (window.closeRoomCard) window.closeRoomCard();
        window.applyProgressToScene(0.90);
    `);
    await new Promise(r => setTimeout(r, 600));
    await takeScreenshot('test_balcony_sunset_glare_fixed.png');

    // 5. Open Balcony Spec Card
    console.log('\nTesting Balcony Room Spec Card...');
    await evaluate(`
        window.openRoomCard(6);
    `);
    await new Promise(r => setTimeout(r, 600));
    await takeScreenshot('test_balcony_spec_card_open.png');

    ws.close();
    console.log('\n[COMPLETE] All hotspot and glare verification screenshots captured!');
}

main().catch(err => {
    console.error('Verification error:', err);
    process.exit(1);
});
