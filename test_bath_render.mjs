import fs from 'fs';

async function testBathNew() {
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

    // Dynamic scene update test
    await send('Runtime.evaluate', {
        expression: `
            (() => {
                window.applyProgressToScene(0.62);
                
                // Camera framing at bathroom doorway
                camState.posX = -1.02;
                camState.posY = 1.48;
                camState.posZ = 0.22;
                camState.targetX = -1.16;
                camState.targetY = 1.18;
                camState.targetZ = 1.45;
                camState.fov = 56.0;
                
                currentCamPos.set(camState.posX, camState.posY, camState.posZ);
                currentCamTarget.set(camState.targetX, camState.targetY, camState.targetZ);
                camera.position.copy(currentCamPos);
                camera.lookAt(currentCamTarget);
                camera.fov = 56.0;
                camera.updateProjectionMatrix();
                
                // Re-build bathroom with visible shower fixtures & glass screen
                const bathGroup = materialGroup.children.find(c => c.children && c.children.length > 5);
                
                composer.render();
            })()
        `
    });

    await new Promise(r => setTimeout(r, 600));
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/test_bath_view_56deg.png', Buffer.from(shot.data, 'base64'));
    ws.close();
    console.log('Saved test_bath_view_56deg.png');
}

testBathNew().catch(console.error);
