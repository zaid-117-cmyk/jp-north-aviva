import fs from 'fs';

async function main() {
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found');
        return;
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

    let id = 1;
    function send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const reqId = id++;
            const handler = (evt) => {
                const data = JSON.parse(evt.data);
                if (data.id === reqId) {
                    ws.removeEventListener('message', handler);
                    if (data.error) reject(data.error);
                    else resolve(data.result);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    await send('Runtime.enable');
    const info = await send('Runtime.evaluate', {
        expression: `(() => {
            try {
                window.applyProgressToScene(0.82);
                const res = {};
                res.camPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
                res.clipHeight = clipHeightPlane.constant;
                
                // Find walls in materialGroup
                const walls = [];
                materialGroup.traverse(child => {
                    if (child.isMesh && child.geometry) {
                        const p = child.position;
                        const params = child.geometry.parameters || {};
                        if (params.height >= 2.0) {
                            walls.push({
                                pos: { x: +p.x.toFixed(3), y: +p.y.toFixed(3), z: +p.z.toFixed(3) },
                                dims: { w: +params.width.toFixed(3), h: +params.height.toFixed(3), d: +params.depth.toFixed(3) },
                                visible: child.visible,
                                matName: child.material ? child.material.type : null,
                                transparent: child.material ? child.material.transparent : null,
                                opacity: child.material ? child.material.opacity : null,
                                depthWrite: child.material ? child.material.depthWrite : null,
                                side: child.material ? child.material.side : null
                            });
                        }
                    }
                });
                res.walls = walls;
                return res;
            } catch (err) {
                return { error: err.stack };
            }
        })()`,
        returnByValue: true,
        awaitPromise: true
    });

    console.log(JSON.stringify(info.result ? info.result.value : info, null, 2));
    ws.close();
}

main().catch(console.error);
