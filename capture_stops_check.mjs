import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

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

    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            renderer.setSize(1920, 1080);
            composer.setSize(1920, 1080);
            camera.aspect = 1920 / 1080;
            camera.updateProjectionMatrix();
        `
    });

    async function capture(p, name) {
        await send('Runtime.evaluate', {
            expression: `
                window.applyProgressToScene(${p});
                composer.render();
            `,
            returnByValue: true
        });
        await new Promise(r => setTimeout(r, 200));
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(shot.data, 'base64');
        fs.writeFileSync(path.join(BRAIN_DIR, name), buf);
        fs.writeFileSync(path.join('D:\\floor plans\\jp-aviva-3d', name), buf);
        console.log(`Saved ${name}`);
    }

    await capture(0.76, 'test_bedroom_stop5.png');
    await capture(0.88, 'test_balcony_stop6.png');
    await capture(0.96, 'test_sunset_stop7.png');

    ws.close();
}

main().catch(console.error);
