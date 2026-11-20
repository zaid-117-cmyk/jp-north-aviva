import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    const pending = new Map();
    let msgId = 1;
    ws.onmessage = evt => {
        const d = JSON.parse(evt.data);
        if (d.id && pending.has(d.id)) pending.get(d.id)(d.result);
    };
    function send(method, params = {}) {
        return new Promise((resolve) => {
            const id = msgId++;
            pending.set(id, (res) => resolve(res));
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    async function evaluate(expr) {
        return (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).value;
    }

    async function capture(filename) {
        const r = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(r.data, 'base64');
        fs.writeFileSync(path.join(BRAIN_DIR, filename), buf);
        console.log(`Saved ${filename}`);
    }

    await evaluate(`
        window.isCapturing = true;
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    // =========================================================
    // 1. BEDROOM ANGLES: Entrance looking diagonally across room
    // =========================================================
    // We want to see: headboard & nightstand (south), bed (center), wardrobe (west), window (north)
    const bedTests = [
        {
            name: 'v2_bed_angleA_wide',
            posX: -1.75, posY: 1.50, posZ: -0.15,
            targetX: -3.20, targetY: 1.05, targetZ: -1.05,
            fov: 52.0
        },
        {
            name: 'v2_bed_angleB_entrance',
            posX: -1.70, posY: 1.50, posZ: -0.10,
            targetX: -3.10, targetY: 1.00, targetZ: -1.15,
            fov: 54.0
        },
        {
            name: 'v2_bed_angleC_corridor_stepback',
            posX: -1.55, posY: 1.50, posZ: -0.10,
            targetX: -3.15, targetY: 1.05, targetZ: -1.10,
            fov: 54.0
        }
    ];

    for (const b of bedTests) {
        await evaluate(`
            window.applyProgressToScene(0.76);
            camState.posX = ${b.posX}; camState.posY = ${b.posY}; camState.posZ = ${b.posZ};
            camState.targetX = ${b.targetX}; camState.targetY = ${b.targetY}; camState.targetZ = ${b.targetZ};
            camState.fov = ${b.fov};
            camera.fov = ${b.fov};
            camera.updateProjectionMatrix();
            camera.position.set(${b.posX}, ${b.posY}, ${b.posZ});
            camera.lookAt(${b.targetX}, ${b.targetY}, ${b.targetZ});
            composer.render();
        `);
        await new Promise(r => setTimeout(r, 600));
        await capture(`${b.name}.png`);
    }

    // =========================================================
    // 2. BALCONY ANGLES: Inside enclosed balcony with foreground
    // =========================================================
    const balcTests = [
        {
            name: 'v2_balc_angleA_slider_doorway',
            posX: 1.25, posY: 1.48, posZ: -0.95,
            targetX: 1.70, targetY: 1.15, targetZ: -5.50,
            fov: 52.0
        },
        {
            name: 'v2_balc_angleB_slider_threshold',
            posX: 1.35, posY: 1.48, posZ: -1.10,
            targetX: 1.75, targetY: 1.12, targetZ: -5.50,
            fov: 54.0
        },
        {
            name: 'v2_balc_angleC_inside_deck',
            posX: 1.20, posY: 1.48, posZ: -1.25,
            targetX: 1.75, targetY: 1.10, targetZ: -5.50,
            fov: 54.0
        }
    ];

    for (const bl of balcTests) {
        await evaluate(`
            window.applyProgressToScene(0.90);
            camState.posX = ${bl.posX}; camState.posY = ${bl.posY}; camState.posZ = ${bl.posZ};
            camState.targetX = ${bl.targetX}; camState.targetY = ${bl.targetY}; camState.targetZ = ${bl.targetZ};
            camState.fov = ${bl.fov};
            camera.fov = ${bl.fov};
            camera.updateProjectionMatrix();
            camera.position.set(${bl.posX}, ${bl.posY}, ${bl.posZ});
            camera.lookAt(${bl.targetX}, ${bl.targetY}, ${bl.targetZ});
            composer.render();
        `);
        await new Promise(r => setTimeout(r, 600));
        await capture(`${bl.name}.png`);
    }

    ws.close();
}

main().catch(console.error);
