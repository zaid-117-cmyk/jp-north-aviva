async function test() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    const page = targets.find(t => t.type === 'page');
    if (!page) { console.log('No page'); return; }
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    let id = 1;
    function send(method, params = {}) {
        return new Promise((resolve) => {
            const curId = id++;
            const handler = (evt) => {
                const d = JSON.parse(evt.data);
                if (d.id === curId) {
                    ws.removeEventListener('message', handler);
                    resolve(d);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id: curId, method, params }));
        });
    }
    await send('Runtime.enable');
    const logs = await send('Runtime.evaluate', { expression: 'window.__logs || []' });
    console.log('Logs:', JSON.stringify(logs));
    const evalRes = await send('Runtime.evaluate', { expression: 'typeof window.applyProgressToScene' });
    console.log('applyProgressToScene:', JSON.stringify(evalRes));
    ws.close();
}
test().catch(e => console.error(e));
