import fs from 'fs';

async function testAngles() {
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

    const angles = [
        // Angle A: Diagonal from East doorway corner looking West-South into shower & vanity
        { name: "angle_A_diagonal", posX: -0.85, posY: 1.48, posZ: 0.25, targetX: -1.32, targetY: 1.12, targetZ: 1.42, fov: 54.0 },
        // Angle B: Centered at doorway looking straight ahead
        { name: "angle_B_center", posX: -1.05, posY: 1.48, posZ: 0.25, targetX: -1.15, targetY: 1.10, targetZ: 1.45, fov: 54.0 },
        // Angle C: Slightly raised doorway looking down at full floorplan composition
        { name: "angle_C_elevated", posX: -0.92, posY: 1.52, posZ: 0.22, targetX: -1.25, targetY: 1.05, targetZ: 1.40, fov: 56.0 }
    ];

    for (const a of angles) {
        await send('Runtime.evaluate', {
            expression: `
                (() => {
                    window.applyProgressToScene(0.62);
                    camera.position.set(${a.posX}, ${a.posY}, ${a.posZ});
                    currentCamTarget.set(${a.targetX}, ${a.targetY}, ${a.targetZ});
                    camera.lookAt(currentCamTarget);
                    camera.fov = ${a.fov};
                    camera.updateProjectionMatrix();
                    composer.render();
                })()
            `
        });
        await new Promise(r => setTimeout(r, 600));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(`C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/test_bath_${a.name}.png`, Buffer.from(shot.data, 'base64'));
        console.log(`Saved test_bath_${a.name}.png`);
    }

    ws.close();
}

testAngles().catch(console.error);
