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
        return new Promise((resolve, reject) => {
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

    // Set high quality 1280x720 capture mode
    await evaluate(`
        window.isCapturing = true;
        renderer.setSize(1280, 720);
        composer.setSize(1280, 720);
        camera.aspect = 1280 / 720;
        camera.updateProjectionMatrix();
    `);

    // -------------------------------------------------------------
    // BEDROOM TESTS at 76% scroll
    // -------------------------------------------------------------
    const bedroomCandidates = [
        {
            name: 'test_bed_opt1_bisector',
            posX: -1.82, posY: 1.50, posZ: -0.20,
            targetX: -3.20, targetY: 1.15, targetZ: -0.75,
            fov: 52.0
        },
        {
            name: 'test_bed_opt2_wide',
            posX: -1.80, posY: 1.50, posZ: -0.18,
            targetX: -3.15, targetY: 1.12, targetZ: -0.90,
            fov: 52.0
        },
        {
            name: 'test_bed_opt3_doorway',
            posX: -1.85, posY: 1.50, posZ: -0.22,
            targetX: -3.25, targetY: 1.15, targetZ: -0.80,
            fov: 54.0
        }
    ];

    for (const c of bedroomCandidates) {
        await evaluate(`
            window.applyProgressToScene(0.76);
            camState.posX = ${c.posX};
            camState.posY = ${c.posY};
            camState.posZ = ${c.posZ};
            camState.targetX = ${c.targetX};
            camState.targetY = ${c.targetY};
            camState.targetZ = ${c.targetZ};
            camState.fov = ${c.fov};
            camera.position.set(${c.posX}, ${c.posY}, ${c.posZ});
            camera.lookAt(${c.targetX}, ${c.targetY}, ${c.targetZ});
            camera.fov = ${c.fov};
            camera.updateProjectionMatrix();
            composer.render();
        `);
        await new Promise(r => setTimeout(r, 600));
        await capture(`${c.name}.png`);
    }

    // -------------------------------------------------------------
    // BALCONY TESTS at 90% scroll
    // -------------------------------------------------------------
    const balconyCandidates = [
        {
            name: 'test_balc_opt1_center',
            posX: 1.45, posY: 1.48, posZ: -1.28,
            targetX: 1.65, targetY: 1.35, targetZ: -6.50,
            fov: 50.0
        },
        {
            name: 'test_balc_opt2_interior_left',
            posX: 1.15, posY: 1.48, posZ: -1.35,
            targetX: 1.65, targetY: 1.35, targetZ: -6.50,
            fov: 50.0
        },
        {
            name: 'test_balc_opt3_wide_foreground',
            posX: 1.35, posY: 1.48, posZ: -1.30,
            targetX: 1.70, targetY: 1.32, targetZ: -6.00,
            fov: 52.0
        }
    ];

    for (const c of balconyCandidates) {
        await evaluate(`
            window.applyProgressToScene(0.90);
            camState.posX = ${c.posX};
            camState.posY = ${c.posY};
            camState.posZ = ${c.posZ};
            camState.targetX = ${c.targetX};
            camState.targetY = ${c.targetY};
            camState.targetZ = ${c.targetZ};
            camState.fov = ${c.fov};
            camera.position.set(${c.posX}, ${c.posY}, ${c.posZ});
            camera.lookAt(${c.targetX}, ${c.targetY}, ${c.targetZ});
            camera.fov = ${c.fov};
            camera.updateProjectionMatrix();
            composer.render();
        `);
        await new Promise(r => setTimeout(r, 600));
        await capture(`${c.name}.png`);
    }

    ws.close();
}

main().catch(console.error);
