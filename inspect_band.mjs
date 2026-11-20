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

    const expr = `
        (() => {
            const T = window.THREE;
            const mouse = new T.Vector2(
                (1100 / 1920) * 2 - 1,
                -(733 / 1080) * 2 + 1
            );
            const raycaster = new T.Raycaster();
            raycaster.setFromCamera(mouse, window.camera);
            const hits = raycaster.intersectObjects(window.scene.children, true);
            const visibleHits = hits.filter(h => {
                let obj = h.object;
                while (obj) {
                    if (!obj.visible) return false;
                    obj = obj.parent;
                }
                return true;
            });
            return visibleHits.slice(0, 5).map(h => ({
                name: h.object.name || 'unnamed',
                type: h.object.type,
                geo: h.object.geometry ? h.object.geometry.type : null,
                geoParams: h.object.geometry && h.object.geometry.parameters ? h.object.geometry.parameters : null,
                pos: h.object.position,
                worldPos: h.object.getWorldPosition(new T.Vector3()),
                matColor: h.object.material ? (h.object.material.color ? '#' + h.object.material.color.getHexString() : null) : null,
                matType: h.object.material ? h.object.material.type : null,
                parentName: h.object.parent ? (h.object.parent.name || h.object.parent.type) : null,
                point: h.point
            }));
        })()
    `;

    const result = await send('Runtime.evaluate', {
        expression: expr,
        returnByValue: true
    });

    console.log('ACTUALLY VISIBLE RAYCAST HITS AT (1100, 733):', JSON.stringify(result.result.value, null, 2));
    ws.close();
}

main().catch(console.error);
