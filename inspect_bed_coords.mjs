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
    await send('Runtime.evaluate', { expression: 'window.isCapturing = true; window.applyProgressToScene(0.74);' });
    await new Promise(r => setTimeout(r, 1000));

    const coords = [[960, 850], [960, 950], [1200, 900]];
    for (const [px, py] of coords) {
        const expr = `
            (() => {
                const T = window.THREE;
                const mouse = new T.Vector2(
                    (${px} / 1920) * 2 - 1,
                    -(${py} / 1080) * 2 + 1
                );
                const raycaster = new T.Raycaster();
                raycaster.setFromCamera(mouse, window.camera);
                const hits = raycaster.intersectObjects(window.scene.children, true);
                if (!hits.length) return null;
                const h = hits[0];
                return {
                    worldPoint: h.point,
                    bedGroupLocal: h.point.clone().sub(new T.Vector3(-3.12, 0, -0.95)),
                    matColor: h.object.material && h.object.material.color ? '#' + h.object.material.color.getHexString() : null
                };
            })()
        `;
        const result = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
        console.log('RAYCAST at (' + px + ', ' + py + '):', JSON.stringify(result.result.value));
    }
    ws.close();
}
main().catch(console.error);
