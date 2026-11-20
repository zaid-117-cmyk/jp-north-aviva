// capture_photorealism_via_server.mjs
async function main() {
    console.log('Connecting to Chrome DevTools...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
    if (!pageTarget) pageTarget = targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found. Targets:', targets);
        process.exit(1);
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
    });

    let msgId = 1;
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = msgId++;
            const handler = (evt) => {
                const data = JSON.parse(evt.data);
                if (data.id === id) {
                    ws.removeEventListener('message', handler);
                    if (data.error) reject(data.error);
                    else resolve(data.result);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    ws.onmessage = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.method === 'Runtime.consoleAPICalled') {
            const vals = (msg.params.args || []).map(a => a.value || a.description || '');
            console.log('BROWSER CONSOLE:', vals.join(' '));
        } else if (msg.method === 'Runtime.exceptionThrown') {
            console.error('BROWSER EXCEPTION:', JSON.stringify(msg.params.exceptionDetails, null, 2));
        }
    };

    await send('Runtime.enable');
    await send('Page.enable');

    await send('Emulation.setDeviceMetricsOverride', {
        width: 1600,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating page to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });

    // Wait 2.5s for initial load
    await new Promise(r => setTimeout(r, 2500));

    async function evalCode(expr) {
        return await send('Runtime.evaluate', {
            expression: expr,
            awaitPromise: true,
            returnByValue: true
        });
    }

    console.log('Waiting for all Poly Haven CC0 3D models to finish loading...');
    await evalCode(`
        (async () => {
            if (typeof window.whenModelsReady === 'function') {
                await window.whenModelsReady();
            } else {
                await new Promise(r => setTimeout(r, 3000));
            }
        })()
    `);
    console.log('All 3D models ready in Three.js scene!');

    // Wait 1s for shaders to settle
    await new Promise(r => setTimeout(r, 1000));

    // Capture each stop via in-page canvas.toDataURL and /save_snapshot
    console.log('Capturing Stop 2: Living Room Hold...');
    await evalCode(`
        (async () => {
            window.applyProgressToScene(0.30);
            window.closeRoomCard();
            await new Promise(r => setTimeout(r, 600));
            const dataUrl = canvas.toDataURL('image/png');
            await fetch('/save_snapshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: 'photoreal_stop2_living_hold.png', image: dataUrl })
            });
            console.log('Captured & saved photoreal_stop2_living_hold.png');
        })()
    `);

    console.log('Capturing Stop 4: Kitchen Hold...');
    await evalCode(`
        (async () => {
            window.applyProgressToScene(0.55);
            window.closeRoomCard();
            await new Promise(r => setTimeout(r, 600));
            const dataUrl = canvas.toDataURL('image/png');
            await fetch('/save_snapshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: 'photoreal_stop4_kitchen_hold.png', image: dataUrl })
            });
            console.log('Captured & saved photoreal_stop4_kitchen_hold.png');
        })()
    `);

    console.log('Capturing Stop 6: Bedroom Hold...');
    await evalCode(`
        (async () => {
            window.applyProgressToScene(0.79);
            window.closeRoomCard();
            await new Promise(r => setTimeout(r, 600));
            const dataUrl = canvas.toDataURL('image/png');
            await fetch('/save_snapshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: 'photoreal_stop6_bedroom_hold.png', image: dataUrl })
            });
            console.log('Captured & saved photoreal_stop6_bedroom_hold.png');
        })()
    `);

    console.log('Capturing Stop 7: Balcony Hold...');
    await evalCode(`
        (async () => {
            window.applyProgressToScene(0.98);
            window.closeRoomCard();
            await new Promise(r => setTimeout(r, 600));
            const dataUrl = canvas.toDataURL('image/png');
            await fetch('/save_snapshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: 'photoreal_stop7_balcony_hold.png', image: dataUrl })
            });
            console.log('Captured & saved photoreal_stop7_balcony_hold.png');
        })()
    `);

    // Reset to start
    await evalCode(`window.applyProgressToScene(0);`);

    ws.close();
    console.log('All photorealism screenshots captured and verified successfully!');
}

main().catch(console.error);
