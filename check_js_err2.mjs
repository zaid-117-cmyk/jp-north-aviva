async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
        ws.onopen = resolve;
        ws.onerror = reject;
    });

    const pending = new Map();
    let msgId = 1;

    ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        if (data.method === 'Runtime.exceptionThrown') {
            console.error('EXCEPTION THROWN:', JSON.stringify(data.params.exceptionDetails));
        } else if (data.method === 'Runtime.consoleAPICalled') {
            console.log('CONSOLE:', data.params.type, data.params.args.map(a => a.value || a.description).join(' '));
        }
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

    console.log('Reloading page...');
    await send('Page.reload');
    await new Promise(r => setTimeout(r, 4000));

    const evalRes = await send('Runtime.evaluate', { expression: 'typeof window.applyProgressToScene' });
    console.log('typeof window.applyProgressToScene:', evalRes.result.value);

    ws.close();
}

main().catch(console.error);
