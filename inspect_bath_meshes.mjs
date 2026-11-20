import fs from 'fs';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((r, e) => { ws.onopen = r; ws.onerror = e; });

    let id = 1;
    const pending = new Map();
    ws.onmessage = (evt) => {
        const d = JSON.parse(evt.data);
        if (d.id && pending.has(d.id)) {
            const { resolve, reject } = pending.get(d.id);
            pending.delete(d.id);
            if (d.error) reject(d.error);
            else resolve(d.result);
        }
    };
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const reqId = id++;
            pending.set(reqId, { resolve, reject });
            ws.send(JSON.stringify({ id: reqId, method, params }));
        });
    }

    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 3500));

    const evalRes = await send('Runtime.evaluate', {
        expression: `(() => {
            try {
                window.applyProgressToScene(0.62);
                const meshes = [];
                scene.traverse(obj => {
                    if (obj.isMesh && obj.visible) {
                        const wp = new THREE.Vector3();
                        obj.getWorldPosition(wp);
                        if (wp.x >= -2.2 && wp.x <= -0.4 && wp.z >= 0.0 && wp.z <= 2.0) {
                            meshes.push({
                                type: obj.geometry ? obj.geometry.type : 'unknown',
                                pos: { x: +wp.x.toFixed(3), y: +wp.y.toFixed(3), z: +wp.z.toFixed(3) },
                                color: obj.material ? (obj.material.color ? obj.material.color.getHexString() : null) : null
                            });
                        }
                    }
                });
                return JSON.stringify(meshes);
            } catch(e) {
                return 'ERROR: ' + e.message;
            }
        })()`,
        returnByValue: true
    });

    console.log(evalRes.result.value);
    ws.close();
}

main().catch(console.error);
