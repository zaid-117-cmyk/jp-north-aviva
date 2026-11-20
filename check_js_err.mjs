async function test() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let target = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
    if (!target) { console.log('No page target found on 9222'); return; }
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

    const ret = await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.67);
            JSON.stringify({
                pos: [camState.posX.toFixed(2), camState.posY.toFixed(2), camState.posZ.toFixed(2)],
                target: [camState.targetX.toFixed(2), camState.targetY.toFixed(2), camState.targetZ.toFixed(2)]
            });
        `,
        returnByValue: true
    });
    console.log('Evaluation result:', ret);
    ws.close();
}
test().catch(console.error);
