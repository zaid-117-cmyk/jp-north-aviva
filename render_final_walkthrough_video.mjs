import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';
const FRAMES_DIR = path.join(LOCAL_DIR, 'frames_final_walkthrough');
const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_VIDEO_PATH = path.join(LOCAL_DIR, 'jp_north_aviva_final_walkthrough.mp4');
const BRAIN_VIDEO_PATH = path.join(BRAIN_DIR, 'jp_north_aviva_final_walkthrough.mp4');

if (!fs.existsSync(FRAMES_DIR)) {
    fs.mkdirSync(FRAMES_DIR, { recursive: true });
} else {
    // Clear old frames
    const oldFiles = fs.readdirSync(FRAMES_DIR);
    for (const f of oldFiles) {
        if (f.endsWith('.jpg')) fs.unlinkSync(path.join(FRAMES_DIR, f));
    }
}

// Cinematic 56.25-second film progression schedule (24 fps native discrete rendering, ZERO blending)
function buildProgressSchedule() {
    const schedule = [];

    const segments = [
        { count: 72,  from: 0.05,  to: 0.05,  name: "Stop 0: 2D Blueprint Plan Sheet (Scale 1:50)" },
        { count: 96,  from: 0.05,  to: 0.22,  name: "Stop 1: Walls Rise to 2.85m & Front Oak Door Swings Open" },
        { count: 72,  from: 0.22,  to: 0.30,  name: "Transition 1->2: Step Through Front Door into Living Sanctuary" },
        { count: 96,  from: 0.34,  to: 0.34,  name: "Stop 2: Living Sanctuary Hold (L-Shaped Linen Sofa, Jute Rug, Marble Table, Gallery Prints & Fluted TV Wall)" },
        { count: 96,  from: 0.34,  to: 0.48,  name: "Transition 2->3: Glide West Through Passage into Gourmet Kitchen Alcove" },
        { count: 96,  from: 0.49,  to: 0.49,  name: "Stop 3: Kitchen Hold (Schott Ceran Hob, Gooseneck Faucet, Task Lights)" },
        { count: 84,  from: 0.49,  to: 0.60,  name: "Transition 3->4: Glide South into 05 - BATH & W.C. (1.15M x 1.30M)" },
        { count: 96,  from: 0.625, to: 0.625, name: "Stop 4: BATH & W.C. Hold (Vanity, Commode & Rain Shower Composition)" },
        { count: 96,  from: 0.625, to: 0.73,  name: "Transition 4->5: Glide North out of Bath, Turn West into Master Bedroom" },
        { count: 96,  from: 0.755, to: 0.755, name: "Stop 5: Master Bedroom Hold (Doorway Diagonal Framing: Tufted Bed, Linen Pillows, Window Curtains & Wardrobe)" },
        { count: 120, from: 0.78,  to: 0.88,  name: "Transition 5->6: Smooth Glide along Living-to-Balcony Glass Corridor" },
        { count: 96,  from: 0.89,  to: 0.89,  name: "Stop 6: Enclosed Balcony Hold (Teak Deck, Bistro Set, Monstera Planter & Glass Mullions)" },
        { count: 96,  from: 0.89,  to: 0.96,  name: "Stop 7: Glide toward Outer Glass framing Sunset Skyline" },
        { count: 146, from: 0.96,  to: 0.96,  name: "Finale Hold: Mumbai Sunset Horizon & Closing Interactive CTA Card" }
    ];

    for (const seg of segments) {
        for (let i = 0; i < seg.count; i++) {
            const t = (seg.count > 1) ? (i / (seg.count - 1)) : 1.0;
            // Smooth sinusoidal easing for transitions
            const eased = (seg.from === seg.to) ? seg.from : seg.from + (seg.to - seg.from) * (0.5 - 0.5 * Math.cos(Math.PI * t));
            schedule.push({ progress: eased, desc: seg.name });
        }
    }

    return schedule;
}

async function main() {
    console.log('Connecting to Chrome DevTools on port 9222...');
    const res = await fetch('http://127.0.0.1:9222/json');
    const targets = await res.json();
    let pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

    if (!pageTarget) {
        console.error('No page target found on port 9222');
        process.exit(1);
    }

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
    await send('Page.enable');
    await send('Network.enable');
    await send('Network.setCacheDisabled', { cacheDisabled: true });
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1280,
        height: 720,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4500));

    // Configure HUD for cinematic presentation
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            if (window.dismissPreloader) window.dismissPreloader('recording');
            if (window.closeRoomCard) window.closeRoomCard();
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            const btn = document.getElementById('room-plus-btn');
            if (btn) btn.style.display = 'none';
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        `
    });

    console.log('Warming up shaders...');
    for (let p = 0.0; p <= 1.0; p += 0.25) {
        await send('Runtime.evaluate', { expression: `if (window.applyProgressToScene) window.applyProgressToScene(${p});` });
        await new Promise(r => setTimeout(r, 150));
    }
    await send('Runtime.evaluate', { expression: `if (window.applyProgressToScene) window.applyProgressToScene(0.05);` });
    await new Promise(r => setTimeout(r, 800));

    const schedule = buildProgressSchedule();
    const total = schedule.length;
    console.log(`Starting capture of ${total} discrete frames for 56.25-second film (native 24 fps, zero blending)...`);

    const startTime = Date.now();

    for (let i = 0; i < total; i++) {
        const item = schedule[i];
        const p = Math.max(0.0, Math.min(1.0, item.progress));

        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p.toFixed(4)});` });
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });

        const numStr = String(i).padStart(4, '0');
        const framePath = path.join(FRAMES_DIR, `frame_${numStr}.jpg`);
        fs.writeFileSync(framePath, Buffer.from(shot.data, 'base64'));

        if (i % 50 === 0 || i === total - 1) {
            const elapsedSec = ((Date.now() - startTime) / 1000).toFixed(1);
            const fpsCapture = (i > 0) ? (i / (elapsedSec)).toFixed(2) : '0';
            const remainingSec = (i > 0 && i < total - 1) ? (((total - i) / (i / elapsedSec))).toFixed(0) : '0';
            console.log(`[Frame ${i + 1}/${total}] (${((i + 1) / total * 100).toFixed(1)}%) p=${p.toFixed(3)} | ${item.desc} | ${elapsedSec}s elapsed (~${remainingSec}s remain, ${fpsCapture} fps)`);
        }
    }

    console.log(`All ${total} frames successfully captured in ${((Date.now() - startTime) / 1000).toFixed(1)}s!`);
    ws.close();

    console.log('Encoding frames to 1080p MP4 via FFmpeg (native 24fps discrete frames, ZERO blending/ghosting)...');
    const ffmpegCmd = `ffmpeg -y -framerate 24 -i "${path.join(FRAMES_DIR, 'frame_%04d.jpg')}" -vf "scale=1920:1080:flags=lanczos" -c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast "${LOCAL_VIDEO_PATH}"`;
    console.log(`Running FFmpeg...`);
    execSync(ffmpegCmd, { stdio: 'inherit' });

    console.log('Copying deliverable video to brain artifacts folder...');
    fs.copyFileSync(LOCAL_VIDEO_PATH, BRAIN_VIDEO_PATH);

    const stats = fs.statSync(LOCAL_VIDEO_PATH);
    console.log(`SUCCESS! Final Master Video created: ${LOCAL_VIDEO_PATH} (${(stats.size / (1024 * 1024)).toFixed(2)} MB, duration: ${(total / 24).toFixed(1)}s)`);
}

main().catch(err => {
    console.error('Fatal recording error:', err);
    process.exit(1);
});
