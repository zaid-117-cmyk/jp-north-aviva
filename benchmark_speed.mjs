import fs from 'fs';
import path from 'path';

async function testBenchmark() {
    console.log('Connecting to Chrome...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
    if (!pageTarget) pageTarget = targets.find(t => t.type === 'page');

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

    await send('Emulation.setDeviceMetricsOverride', {
        width: 1280,
        height: 720,
        deviceScaleFactor: 1,
        mobile: false
    });

    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 3000));

    // Turn on isCapturing to kill the 60fps render loop
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        `
    });

    console.log('Testing 5 frames at 1280x720 with isCapturing = true...');
    for (let i = 0; i < 5; i++) {
        const t0 = Date.now();
        const p = 0.2 + i * 0.1;
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p});` });
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 85 });
        const dt = Date.now() - t0;
        console.log(`Frame ${i}: ${dt}ms`);
    }

    ws.close();
}

testBenchmark().catch(console.error);
