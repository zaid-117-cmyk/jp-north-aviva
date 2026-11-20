async function checkSpots() {
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

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    const result = await send('Runtime.evaluate', {
        expression: `
            window.applyProgressToScene(0.90);
            const raycaster = new THREE.Raycaster();
            // Test normalized device coordinates around top-center
            const coords = [
                { x: 0.0, y: 0.6 },
                { x: -0.2, y: 0.7 },
                { x: 0.2, y: 0.65 }
            ];
            const hits = [];
            coords.forEach(pt => {
                raycaster.setFromCamera(new THREE.Vector2(pt.x, pt.y), camera);
                const intersects = raycaster.intersectObjects(scene.children, true);
                hits.push({
                    pt,
                    objects: intersects.map(i => ({
                        name: i.object.name || i.object.type,
                        pos: i.object.position,
                        mat: i.object.material ? (i.object.material.name || i.object.material.type) : 'no-mat',
                        color: i.object.material && i.object.material.color ? i.object.material.color.getHexString() : null,
                        dist: i.distance
                    }))
                });
            });
            // Also inspect scene for any Points or Sprites or Lights in balcony view
            const specialObjects = [];
            scene.traverse(obj => {
                if (obj.isPoints || obj.isSprite) {
                    specialObjects.push({ type: obj.type, pos: obj.position, count: obj.geometry ? obj.geometry.attributes.position.count : 0 });
                }
            });
            JSON.stringify({ hits, specialObjects }, null, 2);
        `
    });

    console.log(result.result.value);
    ws.close();
}

checkSpots().catch(console.error);
