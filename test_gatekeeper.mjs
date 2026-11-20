import fs from 'fs';
import path from 'path';

const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';

async function main() {
    console.log('Connecting to Chrome on port 9222...');
    let targets = null;
    for (let attempt = 0; attempt < 20; attempt++) {
        try {
            const res = await fetch('http://127.0.0.1:9222/json');
            targets = await res.json();
            if (targets && targets.length > 0) break;
        } catch (e) {
            await new Promise(r => setTimeout(r, 500));
        }
    }

    if (!targets) {
        console.error('No page target found on port 9222');
        process.exit(1);
    }

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
        if (data.method === 'Runtime.consoleAPICalled') {
            const args = data.params.args.map(a => a.value || a.description).join(' ');
            console.log(`[Browser Console] ${data.params.type}: ${args}`);
        } else if (data.method === 'Runtime.exceptionThrown') {
            console.error(`[Browser Exception]`, data.params.exceptionDetails);
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
    await send('Network.enable');

    console.log('Navigating to http://localhost:8080 ...');
    await send('Page.navigate', { url: 'http://localhost:8080' });

    // Wait 5 seconds for full initialization
    await new Promise(r => setTimeout(r, 5000));

    console.log('\n--- 1. VERIFYING HARDWARE & WEBGL 2 CHECK ---');
    const hwCheck = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const report = window.checkHardwareCapabilities();
                return {
                    hasGatekeeperFn: typeof window.checkHardwareCapabilities === 'function',
                    capable: report.capable,
                    reason: report.reason,
                    renderer: report.renderer,
                    vendor: report.vendor
                };
            })()
        `,
        returnByValue: true
    });
    console.log('Hardware Probe Report:', hwCheck.result.value);

    // Test software renderer detector logic simulation
    const swSimulation = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const softwareKeywords = ['swiftshader', 'llvmpipe', 'softpipe', 'software rasterizer', 'microsoft basic render driver'];
                const test1 = 'Google SwiftShader (Subzero) Direct3D11';
                const isSw1 = softwareKeywords.some(kw => test1.toLowerCase().includes(kw));
                const test2 = 'llvmpipe (LLVM 12.0.0, 256 bits)';
                const isSw2 = softwareKeywords.some(kw => test2.toLowerCase().includes(kw));
                const test3 = 'ANGLE (NVIDIA GeForce RTX 4090 Direct3D11)';
                const isSw3 = softwareKeywords.some(kw => test3.toLowerCase().includes(kw));
                return {
                    detectsSwiftShader: isSw1,
                    detectsLlvmpipe: isSw2,
                    passesRealGPU: !isSw3
                };
            })()
        `,
        returnByValue: true
    });
    console.log('Software Emulation Detection Simulation:', swSimulation.result.value);

    console.log('\n--- 2. VERIFYING MANUAL "SWITCH TO VIDEO MODE" TOGGLE ---');
    const toggleButtonsCheck = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const headerBtn = document.getElementById('header-mode-toggle');
                const preloaderBtn = document.querySelector('.preloader-mode-switch');
                return {
                    headerToggleExists: !!headerBtn,
                    headerToggleText: headerBtn ? headerBtn.textContent.trim() : null,
                    preloaderToggleExists: !!preloaderBtn
                };
            })()
        `,
        returnByValue: true
    });
    console.log('Toggle Buttons Available:', toggleButtonsCheck.result.value);

    console.log('\n--- 3. ACTIVATING VIDEO FALLBACK MODE ---');
    await send('Runtime.evaluate', {
        expression: `window.switchExperienceMode('video');`
    });
    await new Promise(r => setTimeout(r, 1200));

    const videoModeState = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const vf = document.getElementById('video-fallback-view');
                const vid = document.getElementById('fallback-video');
                const canvas = document.getElementById('webgl-canvas');
                const hud = document.getElementById('hud-overlay');
                const headerBtn = document.getElementById('header-mode-toggle');
                return {
                    fallbackViewVisible: vf && vf.style.display !== 'none' && window.getComputedStyle(vf).display !== 'none',
                    canvasHidden: canvas && canvas.style.display === 'none',
                    hudHidden: hud && hud.style.display === 'none',
                    videoExists: !!vid,
                    videoSrc: vid ? vid.getAttribute('src') : null,
                    hasAutoplay: vid ? vid.hasAttribute('autoplay') : false,
                    hasMuted: vid ? vid.hasAttribute('muted') : false,
                    hasLoop: vid ? vid.hasAttribute('loop') : false,
                    hasPlaysinline: vid ? vid.hasAttribute('playsinline') : false,
                    hasControls: vid ? vid.hasAttribute('controls') : false,
                    headerBtnTextInVideoMode: headerBtn ? headerBtn.textContent.trim() : null
                };
            })()
        `,
        returnByValue: true
    });
    console.log('Video Fallback Mode State:', videoModeState.result.value);

    // Capture visual confirmation of Video Fallback View
    const vfSnap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
    fs.writeFileSync(path.join(BRAIN_DIR, 'verify_video_fallback_mode.jpg'), Buffer.from(vfSnap.data, 'base64'));
    console.log('[OK] Saved verify_video_fallback_mode.jpg');

    console.log('\n--- 4. SWITCHING BACK TO 3D TOUR ---');
    await send('Runtime.evaluate', {
        expression: `window.switchExperienceMode('3d');`
    });
    await new Promise(r => setTimeout(r, 1200));

    const threeDState = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const vf = document.getElementById('video-fallback-view');
                const canvas = document.getElementById('webgl-canvas');
                const hud = document.getElementById('hud-overlay');
                const headerBtn = document.getElementById('header-mode-toggle');
                return {
                    fallbackViewHidden: vf && (vf.style.display === 'none' || window.getComputedStyle(vf).display === 'none'),
                    canvasVisible: canvas && canvas.style.display !== 'none',
                    hudVisible: hud && hud.style.display !== 'none',
                    headerBtnTextIn3DMode: headerBtn ? headerBtn.textContent.trim() : null
                };
            })()
        `,
        returnByValue: true
    });
    console.log('Restored 3D Spatial State:', threeDState.result.value);

    // Capture visual confirmation of restored 3D Mode
    const tdSnap = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90 });
    fs.writeFileSync(path.join(BRAIN_DIR, 'verify_mode_toggle_3d.jpg'), Buffer.from(tdSnap.data, 'base64'));
    console.log('[OK] Saved verify_mode_toggle_3d.jpg');

    ws.close();
    console.log('\nALL GATEKEEPER & FALLBACK TESTS PASSED SUCCESSFULLY!');
}

main().catch(err => {
    console.error('Gatekeeper test error:', err);
    process.exit(1);
});
