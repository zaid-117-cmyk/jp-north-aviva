async function diag() {
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
    await new Promise(r => setTimeout(r, 4000));

    const r1 = await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.76);
            JSON.stringify({
                camPos: [camera.position.x, camera.position.y, camera.position.z],
                camState: [camState.posX, camState.posY, camState.posZ, camState.targetX, camState.targetY, camState.targetZ],
                renderRunning: !window.isCapturing
            })
        `,
        returnByValue: true
    });
    console.log('After applyProgressToScene(0.76):', r1.value);

    // Now set camera.position
    const r2 = await send('Runtime.evaluate', {
        expression: `
            camera.position.set(-1.85, 1.48, -1.25);
            camera.lookAt(-3.15, 1.00, -0.20);
            JSON.stringify({
                camPos: [camera.position.x, camera.position.y, camera.position.z]
            })
        `,
        returnByValue: true
    });
    console.log('Immediately after set:', r2.value);

    await new Promise(r => setTimeout(r, 500));
    const r3 = await send('Runtime.evaluate', {
        expression: `
            JSON.stringify({
                camPos: [camera.position.x, camera.position.y, camera.position.z]
            })
        `,
        returnByValue: true
    });
    console.log('500ms later:', r3.value);

    ws.close();
}

diag().catch(console.error);
