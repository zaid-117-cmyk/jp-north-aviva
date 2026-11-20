import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const LOCAL_DIR = 'D:\\floor plans\\jp-aviva-3d';
const FRAMES_DIR = path.join(LOCAL_DIR, 'frames_10_out_of_10');
const BRAIN_DIR = 'C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\a89496f6-6f7c-4a3f-b45b-cae80fa0337c';
const LOCAL_VIDEO_PATH = path.join(LOCAL_DIR, 'jp_north_aviva_walkthrough_10_out_of_10.mp4');
const BRAIN_VIDEO_PATH = path.join(BRAIN_DIR, 'jp_north_aviva_walkthrough_10_out_of_10.mp4');

if (!fs.existsSync(FRAMES_DIR)) fs.mkdirSync(FRAMES_DIR, { recursive: true });

// Pacing schedule: 660 frames (55.0s at 12fps -> interpolated to 24fps Full HD 1080p)
function buildProgressSchedule() {
    const schedule = [];
    
    // Timeline key progress points in script.js:
    // Stop 0: Blueprint Sheet (p = 0.05)
    // Stop 1: Walls Rise & Door Open (p = 0.16)
    // Stop 2: Living Sanctuary (p = 0.32)
    // Stop 3: Gourmet Kitchen Alcove (p = 0.48)
    // Stop 4: Designer Bathroom Suite (p = 0.62)
    // Stop 5: Master Bedroom Suite (p = 0.76)
    // Stop 6: Balcony Deck & Utility (p = 0.90)
    // Stop 7: Golden Mumbai Sunset Finale (p = 0.98)

    const segments = [
        { count: 65, from: 0.05, to: 0.05, name: "Stop 0: Blueprint Sheet (Scale 1:50)" },
        { count: 75, from: 0.05, to: 0.16, name: "Stop 1: Walls Rise to 2.85m & Front Door Swings Open" },
        { count: 65, from: 0.16, to: 0.32, name: "Stop 2: Entry into Living & Dining Sanctuary" },
        { count: 65, from: 0.32, to: 0.32, name: "Stop 2: Living Sanctuary Hold (OLED TV, AC, Dining Table)" },
        { count: 50, from: 0.32, to: 0.48, name: "Stop 3: Corridor Glide into Gourmet Kitchen Alcove" },
        { count: 60, from: 0.48, to: 0.48, name: "Stop 3: Kitchen Hold (Fridge, Microwave, Glowing Hob, Chimney)" },
        { count: 48, from: 0.48, to: 0.62, name: "Stop 4: Corridor Transition into Bathroom Suite" },
        { count: 55, from: 0.62, to: 0.62, name: "Stop 4: Bathroom Hold (Backlit Halo Mirror, Toilet, Rain Shower)" },
        { count: 48, from: 0.62, to: 0.76, name: "Stop 5: Passage into Master Bedroom Suite" },
        { count: 60, from: 0.76, to: 0.76, name: "Stop 5: Bedroom Hold (Wild Mushroom Wall, Floating Bed, Pendants)" },
        { count: 45, from: 0.76, to: 0.90, name: "Stop 6: Balcony Glass Slider Opens & Step onto Teak Deck" },
        { count: 50, from: 0.90, to: 0.90, name: "Stop 6: Balcony Hold (Washing Machine, Armchair, Bistro, Plants)" },
        { count: 24, from: 0.90, to: 0.98, name: "Stop 7: Golden Mumbai Sunset Grand Finale" }
    ];

    for (const seg of segments) {
        for (let i = 0; i < seg.count; i++) {
            const t = (seg.count > 1) ? (i / (seg.count - 1)) : 1.0;
            // Smooth ease for transitions
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
    await send('Emulation.setDeviceMetricsOverride', {
        width: 1280,
        height: 720,
        deviceScaleFactor: 1,
        mobile: false
    });

    console.log('Navigating to http://localhost:8080/ ...');
    await send('Page.navigate', { url: 'http://localhost:8080/' });
    await new Promise(r => setTimeout(r, 4000));

    // Prepare presentation HUD: hide buttons, hide hints, configure 1280x720 canvas
    await send('Runtime.evaluate', {
        expression: `
            window.isCapturing = true;
            const nav = document.querySelector('.nav-controls-group');
            if (nav) nav.style.display = 'none';
            const hint = document.querySelector('.scroll-hint');
            if (hint) hint.style.display = 'none';
            const btn = document.getElementById('room-plus-btn');
            if (btn) btn.style.display = 'none';
            const card = document.getElementById('room-card');
            if (card) card.style.display = 'none';
            renderer.setSize(1280, 720);
            composer.setSize(1280, 720);
            camera.aspect = 1280 / 720;
            camera.updateProjectionMatrix();
        `
    });

    console.log('Warming up shaders with initial render...');
    await send('Runtime.evaluate', { expression: `window.applyProgressToScene(0.32);` });
    await new Promise(r => setTimeout(r, 1000));

    const schedule = buildProgressSchedule();
    const total = schedule.length;
    console.log(`Starting deterministic capture of ${total} frames for 55-second film...`);

    const startTime = Date.now();

    for (let i = 0; i < total; i++) {
        const item = schedule[i];
        const p = Math.max(0.0, Math.min(1.0, item.progress));
        
        await send('Runtime.evaluate', { expression: `window.applyProgressToScene(${p.toFixed(4)});` });
        const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });

        const numStr = String(i).padStart(4, '0');
        const framePath = path.join(FRAMES_DIR, `frame_${numStr}.jpg`);
        fs.writeFileSync(framePath, Buffer.from(shot.data, 'base64'));

        if (i % 35 === 0 || i === total - 1) {
            const elapsedSec = ((Date.now() - startTime) / 1000).toFixed(1);
            const fpsCapture = (i > 0) ? (i / (elapsedSec)).toFixed(2) : '0';
            const remainingSec = (i > 0 && i < total - 1) ? (((total - i) / (i / elapsedSec))).toFixed(0) : '0';
            console.log(`[Frame ${i + 1}/${total}] (${((i + 1) / total * 100).toFixed(1)}%) p=${p.toFixed(3)} | ${item.desc} | ${elapsedSec}s elapsed (~${remainingSec}s remain, ${fpsCapture} fps)`);
        }
    }

    console.log(`All ${total} frames successfully captured in ${((Date.now() - startTime) / 1000).toFixed(1)}s!`);
    ws.close();

    console.log('Encoding frames to pristine 1080p MP4 via FFmpeg (55s @ 24fps motion blend)...');
    const ffmpegCmd = `ffmpeg -y -framerate 12 -i "${path.join(FRAMES_DIR, 'frame_%04d.jpg')}" -vf "scale=1920:1080:flags=lanczos,minterpolate='fps=24:mi_mode=blend'" -c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast "${LOCAL_VIDEO_PATH}"`;
    console.log(`Running FFmpeg: ${ffmpegCmd}`);
    execSync(ffmpegCmd, { stdio: 'inherit' });

    console.log('Copying 10/10 video deliverable to brain artifacts folder...');
    fs.copyFileSync(LOCAL_VIDEO_PATH, BRAIN_VIDEO_PATH);

    const stats = fs.statSync(LOCAL_VIDEO_PATH);
    console.log(`SUCCESS! 10/10 Video created: ${LOCAL_VIDEO_PATH} (${(stats.size / (1024 * 1024)).toFixed(2)} MB)`);
}

main().catch(err => {
    console.error('Fatal recording error:', err);
    process.exit(1);
});
