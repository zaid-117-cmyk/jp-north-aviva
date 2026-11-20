// Node 22 built-in WebSocket

async function check() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let target = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
    if (!target) {
        console.error('No page target found');
        return;
    }
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
        return new Promise(resolve => {
            const reqId = id++;
            const handler = (evt) => {
                const d = JSON.parse(evt.data);
                if (d.id === reqId) {
                    ws.removeEventListener('message', handler);
                    resolve(d.result);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id: reqId, method, params }));
        });
    }

    const testPs = [0.38, 0.39, 0.41, 0.42, 0.44, 0.46, 0.52, 0.54, 0.56, 0.58, 0.60, 0.65, 0.67, 0.70, 0.72, 0.75, 0.80, 0.81, 0.84, 0.85, 0.87, 0.89];
    for (const p of testPs) {
        const ret = await send('Runtime.evaluate', {
            expression: `
                window.applyProgressToScene(${p});
                JSON.stringify({
                    p: ${p},
                    pos: [camState.posX.toFixed(2), camState.posY.toFixed(2), camState.posZ.toFixed(2)],
                    target: [camState.targetX.toFixed(2), camState.targetY.toFixed(2), camState.targetZ.toFixed(2)]
                });
            `,
            returnByValue: true
        });
        console.log(ret.result.value);
    }
    ws.close();
}
check().catch(console.error);
