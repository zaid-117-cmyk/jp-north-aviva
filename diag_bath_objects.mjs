import fs from 'fs';

async function diag() {
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

    const evalResult = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const results = [];
                scene.traverse(obj => {
                    if (obj.isMesh && obj.position) {
                        const wp = new THREE.Vector3();
                        obj.getWorldPosition(wp);
                        if (wp.x < -0.5 && wp.x > -2.0 && wp.z > 0.2 && wp.z < 1.8) {
                            results.push({
                                name: obj.name || 'unnamed',
                                geo: obj.geometry ? obj.geometry.type : 'none',
                                pos: { x: wp.x.toFixed(2), y: wp.y.toFixed(2), z: wp.z.toFixed(2) },
                                mat: obj.material ? (obj.material.name || obj.material.type) : 'none',
                                color: (obj.material && obj.material.color) ? obj.material.color.getHexString() : 'none'
                            });
                        }
                    }
                });
                return JSON.stringify(results, null, 2);
            })()
        `,
        returnByValue: true
    });

    console.log("Bathroom objects in bounding box:");
    console.log(evalResult.result.value);
    ws.close();
}

diag().catch(console.error);
