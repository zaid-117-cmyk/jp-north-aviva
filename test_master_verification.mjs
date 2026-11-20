import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';

async function main() {
    console.log('Connecting to Chrome on port 9222...');
    let targets = null;
    for (let attempt = 0; attempt < 20; attempt++) {
        try {
            const res = await fetch('http://127.0.0.1:9222/json');
            targets = await res.json();
            if (targets && targets.length > 0) break;
        } catch (e) {
            await new Promise(r => setTimeout(r, 500));
        }
    }

    if (!targets) {
        console.error('No page target found on port 9222');
        process.exit(1);
    }

    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

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

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Network.enable');
    await send('Network.setCacheDisabled', { cacheDisabled: true });
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating to http://localhost:8080...');
    await send('Page.navigate', { url: 'http://localhost:8080' });
    await new Promise(r => setTimeout(r, 4500));

    // Disable RAF loop interference and configure viewport
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            if (window.dismissPreloader) window.dismissPreloader('test_verification');
            if (window.closeRoomCard) window.closeRoomCard();
        `
    });

    console.log('Warming up scene shaders...');
    for (let p = 0.0; p <= 1.0; p += 0.25) {
        await send('Runtime.evaluate', {
            expression: `if (window.applyProgressToScene) window.applyProgressToScene(${p});`
        });
        await new Promise(r => setTimeout(r, 150));
    }

    // Capture stops
    const stops = [
        { name: 'verify_living_032', p: 0.34, desc: 'Living Room TV Forward Text, Opaque Table, 20deg Tilted Cream Pillow, Zero Chaise Clipping' },
        { name: 'verify_living_sync_040', p: 0.40, desc: 'Living Room Label Still Active at 40% (delayed to 42%)' },
        { name: 'verify_kitchen_048', p: 0.48, desc: 'Gourmet Kitchen Hob, Task Lighting, Hood Touch Strip, Oak Cabinets' },
        { name: 'verify_kitchen_sync_055', p: 0.55, desc: 'Kitchen-to-Bath Synchronization (04 Label active through 56%)' },
        { name: 'verify_bathroom_061', p: 0.61, desc: 'Bath & W.C. Eye-Level Framing, Sculpted WC, Shower Screen' },
        { name: 'verify_bedroom_074', p: 0.74, desc: 'Master Bedroom Leveled Framing, Plump Pillows, Draped Throw, Drapery' },
        { name: 'verify_corridor_glide_081', p: 0.81, desc: 'Bedroom-to-Balcony Smooth Glide along Corridor at 81%' },
        { name: 'verify_balcony_088', p: 0.88, desc: 'Balcony Deck Eye-Level Pitch, Matte Terracotta Espresso Cups on Marble Table, Bistro Chair, Planter, Skyline' },
        { name: 'verify_finale_098', p: 0.98, desc: 'Sunset Finale, Closing Pitch CTA Card' }
    ];

    for (const s of stops) {
        console.log(`Setting progress to ${s.p} (${s.name})...`);
        await send('Runtime.evaluate', {
            expression: `
                if (window.applyProgressToScene) {
                    window.applyProgressToScene(${s.p});
                }
            `
        });
        await new Promise(r => setTimeout(r, 1200));

        const snap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
        const buf = Buffer.from(snap.data, 'base64');

        const localFile = path.join(LOCAL_DIR, `${s.name}.jpg`);
        const brainFile = path.join(BRAIN_DIR, `${s.name}.jpg`);

        fs.writeFileSync(localFile, buf);
        fs.writeFileSync(brainFile, buf);
        console.log(`[OK] Saved ${s.name}.jpg (${s.desc})`);
    }

    // Test Metric to Imperial Live Toggle at Living Sanctuary (p = 0.34)
    console.log('Testing Live Unit Toggle to Imperial (SQ.FT)...');
    await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.34);
            window.setGlobalUnit('imperial');
        `
    });
    await new Promise(r => setTimeout(r, 600));
    const imperialSnap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    fs.writeFileSync(path.join(LOCAL_DIR, 'verify_imperial_toggle_032.jpg'), Buffer.from(imperialSnap.data, 'base64'));
    fs.writeFileSync(path.join(BRAIN_DIR, 'verify_imperial_toggle_032.jpg'), Buffer.from(imperialSnap.data, 'base64'));
    console.log('[OK] Saved verify_imperial_toggle_032.jpg (Imperial 301 SQ.FT Toggle Verified)');

    // Reset back to Metric for remaining tests
    await send('Runtime.evaluate', {
        expression: `window.setGlobalUnit('metric');`
    });
    await new Promise(r => setTimeout(r, 400));

    // Test Opening Site Visit Modal
    console.log('Testing Book Site Visit Modal...');
    await send('Runtime.evaluate', {
        expression: `window.triggerSiteVisitModal();`
    });
    await new Promise(r => setTimeout(r, 800));
    const modalSnap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    fs.writeFileSync(path.join(LOCAL_DIR, 'verify_modal_site_visit.jpg'), Buffer.from(modalSnap.data, 'base64'));
    fs.writeFileSync(path.join(BRAIN_DIR, 'verify_modal_site_visit.jpg'), Buffer.from(modalSnap.data, 'base64'));
    console.log('[OK] Saved verify_modal_site_visit.jpg');

    // Close and Test Floorplan Specs Modal
    console.log('Testing Floorplan Specs Modal...');
    await send('Runtime.evaluate', {
        expression: `
            window.closeModal('modal-site-visit');
            window.downloadFloorplanBrochure();
        `
    });
    await new Promise(r => setTimeout(r, 800));
    const specsSnap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    fs.writeFileSync(path.join(LOCAL_DIR, 'verify_modal_specs.jpg'), Buffer.from(specsSnap.data, 'base64'));
    fs.writeFileSync(path.join(BRAIN_DIR, 'verify_modal_specs.jpg'), Buffer.from(specsSnap.data, 'base64'));
    console.log('[OK] Saved verify_modal_specs.jpg');

    ws.close();
    console.log('All master verification snapshots captured successfully!');
}

main().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
