import fs from 'fs';

async function inspect() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    const t = targets.find(x => x.type === 'page' && x.url.includes('8080')) || targets.find(x => x.type === 'page');
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);
    let id = 1;
    const send = (m, p = {}) => new Promise((resolve) => {
        const reqId = id++;
        const onm = (evt) => {
            const d = JSON.parse(evt.data);
            if (d.id === reqId) { ws.removeEventListener('message', onm); resolve(d.result); }
        };
        ws.addEventListener('message', onm);
        ws.send(JSON.stringify({ id: reqId, method: m, params: p }));
    });
    await send('Runtime.enable');
    await send('Page.enable');

    // Raycast from the center-right of the screen (NDC: x = 0.5, y = 0.0)
    const evalResult = await send('Runtime.evaluate', {
        expression: `
            (() => {
                window.applyProgressToScene(0.62);
                const raycaster = new THREE.Raycaster();
                // Test multiple screen coordinates on the right side: (0.3, 0), (0.5, 0), (0.7, 0)
                const hits = [];
                [0.3, 0.5, 0.7, 0.85].forEach(screenX => {
                    raycaster.setFromCamera(new THREE.Vector2(screenX, 0.0), camera);
                    const intersects = raycaster.intersectObjects(scene.children, true);
                    if (intersects.length > 0) {
                        const first = intersects[0];
                        const obj = first.object;
                        hits.push({
                            screenX,
                            distance: first.distance.toFixed(2),
                            point: { x: first.point.x.toFixed(2), y: first.point.y.toFixed(2), z: first.point.z.toFixed(2) },
                            geo: obj.geometry.type,
                            mat: obj.material.name || obj.material.type,
                            color: obj.material.color ? obj.material.color.getHexString() : 'none',
                            parentName: obj.parent ? obj.parent.name : 'root'
                        });
                    }
                });
                return JSON.stringify(hits, null, 2);
            })()
        `,
        returnByValue: true
    });

    console.log("Raycast hits on the right of screen:");
    console.log(evalResult.result.value);
    ws.close();
}

inspect().catch(console.error);
