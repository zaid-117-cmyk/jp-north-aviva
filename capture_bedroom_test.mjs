import fs from 'fs';

async function testBedroom() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    const t = targets.find(x => x.type === 'page' && x.url.includes('8080')) || targets.find(x => x.type === 'page');
    if (!t) throw new Error('No page found');
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    let id = 1;
    const send = (m, p = {}) => new Promise((resolve, reject) => {
        const reqId = id++;
        const onm = (evt) => {
            const d = JSON.parse(evt.data);
            if (d.id === reqId) {
                ws.removeEventListener('message', onm);
                if (d.error) reject(d.error);
                else resolve(d.result);
            }
        };
        ws.addEventListener('message', onm);
        ws.send(JSON.stringify({ id: reqId, method: m, params: p }));
    });
    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 3500));

    const tests = [
        { name: "bed_target_125", posX: -1.80, posY: 1.50, posZ: -0.22, targetX: -3.10, targetY: 1.15, targetZ: -1.25, fov: 52.0 },
        { name: "bed_target_140", posX: -1.78, posY: 1.50, posZ: -0.20, targetX: -3.05, targetY: 1.15, targetZ: -1.40, fov: 52.0 },
        { name: "bed_target_155", posX: -1.75, posY: 1.50, posZ: -0.18, targetX: -3.00, targetY: 1.12, targetZ: -1.55, fov: 52.0 }
    ];

    for (const test of tests) {
        await send('Runtime.evaluate', {
            expression: `
                (() => {
                    window.applyProgressToScene(0.76);
                    camState.posX = ${test.posX};
                    camState.posY = ${test.posY};
                    camState.posZ = ${test.posZ};
                    camState.targetX = ${test.targetX};
                    camState.targetY = ${test.targetY};
                    camState.targetZ = ${test.targetZ};
                    camState.fov = ${test.fov};
                    currentCamPos.set(camState.posX, camState.posY, camState.posZ);
                    currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
                    camera.position.copy(currentCamPos);
                    camera.lookAt(currentCamTarget);
                    camera.fov = ${test.fov};
                    camera.updateProjectionMatrix();
                    composer.render();
                })()
            `
        });
        await new Promise(r => setTimeout(r, 600));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(`C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/${test.name}.png`, Buffer.from(shot.data, 'base64'));
        console.log(`Saved ${test.name}.png`);
    }

    ws.close();
}

testBedroom().catch(console.error);
