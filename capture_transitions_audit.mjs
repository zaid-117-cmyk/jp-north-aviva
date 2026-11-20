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

    // Set capturing mode to prevent requestAnimationFrame race conditions
    await evaluate(`window.isCapturing = true; if (window.closeRoomCard) window.closeRoomCard();`);

    // Audit Transition 1: 62% to 76% (Bathroom -> Master Bedroom)
    console.log('\n--- AUDITING TRANSITION 1: BATHROOM -> MASTER BEDROOM (62% to 76%) ---');
    const t1Steps = [0.62, 0.65, 0.67, 0.69, 0.71, 0.73, 0.76];
    for (const p of t1Steps) {
        await evaluate(`window.applyProgressToScene(${p})`);
        await new Promise(r => setTimeout(r, 300));
        const camData = await evaluate(`(() => {
            const s = window.camState || {};
            return {
                p: ${p},
                pos: { x: +(s.posX || 0).toFixed(2), y: +(s.posY || 0).toFixed(2), z: +(s.posZ || 0).toFixed(2) },
                target: { x: +(s.targetX || 0).toFixed(2), y: +(s.targetY || 0).toFixed(2), z: +(s.targetZ || 0).toFixed(2) }
            };
        })()`);
        console.log(`Progress ${Math.round(p*100)}%: Cam Pos=(${camData.pos.x}, ${camData.pos.y}, ${camData.pos.z}), Target=(${camData.target.x}, ${camData.target.y}, ${camData.target.z})`);
    }

    // Capture snapshot at 67% (Rise & glide out of bath)
    await evaluate(`window.applyProgressToScene(0.67)`);
    await new Promise(r => setTimeout(r, 500));
    await takeScreenshot('transition_67_bath_exit_glide.png');

    // Capture snapshot at 71% (Glide through bedroom doorway)
    await evaluate(`window.applyProgressToScene(0.71)`);
    await new Promise(r => setTimeout(r, 500));
    await takeScreenshot('transition_71_bedroom_door_entry.png');

    // Audit Transition 2: 78% to 92% (Master Bedroom -> Balcony Deck)
    console.log('\n--- AUDITING TRANSITION 2: MASTER BEDROOM -> BALCONY DECK (78% to 92%) ---');
    const t2Steps = [0.78, 0.81, 0.83, 0.85, 0.87, 0.89, 0.91];
    for (const p of t2Steps) {
        await evaluate(`window.applyProgressToScene(${p})`);
        await new Promise(r => setTimeout(r, 300));
        const camData = await evaluate(`(() => {
            const s = window.camState || {};
            return {
                p: ${p},
                pos: { x: +(s.posX || 0).toFixed(2), y: +(s.posY || 0).toFixed(2), z: +(s.posZ || 0).toFixed(2) },
                target: { x: +(s.targetX || 0).toFixed(2), y: +(s.targetY || 0).toFixed(2), z: +(s.targetZ || 0).toFixed(2) },
                doorX: +(s.balconyDoorX || 0).toFixed(2)
            };
        })()`);
        console.log(`Progress ${Math.round(p*100)}%: Cam Pos=(${camData.pos.x}, ${camData.pos.y}, ${camData.pos.z}), Target=(${camData.target.x}, ${camData.target.y}, ${camData.target.z}), BalconyDoorX=${camData.doorX}`);
    }

    // Capture snapshot at 82% (Rise & glide out of bedroom)
    await evaluate(`window.applyProgressToScene(0.82)`);
    await new Promise(r => setTimeout(r, 500));
    await takeScreenshot('transition_82_bedroom_exit_glide.png');

    // Capture snapshot at 85% (Glide across living toward open sliders)
    await evaluate(`window.applyProgressToScene(0.85)`);
    await new Promise(r => setTimeout(r, 500));
    await takeScreenshot('transition_85_living_to_balcony_glide.png');

    // Audit Mumbai Sunset Finale & Closing CTA Card at 98%
    console.log('\n--- AUDITING MUMBAI SUNSET FINALE & CLOSING CTA CARD (98%) ---');
    await evaluate(`window.applyProgressToScene(0.98)`);
    await new Promise(r => setTimeout(r, 800));
    const ctaStatus = await evaluate(`(() => {
        const cta = document.getElementById('closing-cta-card');
        return {
            exists: !!cta,
            visible: cta ? cta.classList.contains('visible') : false,
            opacity: cta ? window.getComputedStyle(cta).opacity : null
        };
    })()`);
    console.log('CTA Card Status at 98%:', ctaStatus);
    await takeScreenshot('sunset_finale_with_cta.png');

    // Capture all 8 full stops for delivery artifact
    console.log('\n--- CAPTURING FULL 8-STOP WALKTHROUGH FOR FINAL REPORT ---');
    const stops = [
        { p: 0.05, name: 'smooth_stop0_plan_sheet.png' },
        { p: 0.16, name: 'smooth_stop1_walls_rising.png' },
        { p: 0.32, name: 'smooth_stop2_living_room.png' },
        { p: 0.48, name: 'smooth_stop3_kitchen_alcove.png' },
        { p: 0.62, name: 'smooth_stop4_bathroom_suite.png' },
        { p: 0.76, name: 'smooth_stop5_master_bedroom.png' },
        { p: 0.90, name: 'smooth_stop6_balcony_deck.png' },
        { p: 0.98, name: 'smooth_stop7_sunset_finale.png' }
    ];

    for (const s of stops) {
        await evaluate(`window.applyProgressToScene(${s.p})`);
        await new Promise(r => setTimeout(r, 500));
        await takeScreenshot(s.name);
    }

    console.log('\nAll transitions, sunset finale, and full stops captured successfully!');
    ws.close();
}

main().catch(err => {
    console.error('Audit failed:', err);
    process.exit(1);
});
