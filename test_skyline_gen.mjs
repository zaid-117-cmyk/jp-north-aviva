import { createCanvas } from 'canvas';
import fs from 'fs';

function generateSkyline() {
    const cSky = createCanvas(2048, 1024);
    const ctxSky = cSky.getContext('2d');

    // 1. Soft atmospheric sunset gradient tuned for ACESFilmicToneMapping
    const skyGrad = ctxSky.createLinearGradient(0, 0, 0, 1024);
    skyGrad.addColorStop(0.00, '#101726'); // Deep twilight navy
    skyGrad.addColorStop(0.22, '#2B2438'); // Evening mauve
    skyGrad.addColorStop(0.45, '#633B44'); // Warm terracotta dusk
    skyGrad.addColorStop(0.66, '#B8623A'); // Golden hour amber
    skyGrad.addColorStop(0.80, '#E2954E'); // Soft golden horizon glow
    skyGrad.addColorStop(0.90, '#C87E42'); // Atmospheric horizon mist
    skyGrad.addColorStop(1.00, '#884D2C'); // Ground dusk haze
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // 2. Broad horizontal atmospheric glow along the horizon (no harsh white sun dot)
    const sunGlow = ctxSky.createRadialGradient(1320, 740, 40, 1320, 740, 720);
    sunGlow.addColorStop(0.00, 'rgba(255, 218, 150, 0.38)');
    sunGlow.addColorStop(0.28, 'rgba(255, 175, 95, 0.22)');
    sunGlow.addColorStop(0.60, 'rgba(235, 125, 60, 0.10)');
    sunGlow.addColorStop(1.00, 'rgba(0, 0, 0, 0)');
    ctxSky.fillStyle = sunGlow;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // 3. LAYER 1: Distant Mumbai High-Rise Silhouette & Bandra-Worli Sea Link Pylon
    ctxSky.fillStyle = 'rgba(72, 50, 62, 0.70)';
    ctxSky.beginPath();
    ctxSky.moveTo(0, 1024);
    for (let x = 0; x < 2048; x += 32) {
        const baseH = 170 + Math.sin(x * 0.015) * 75 + Math.cos(x * 0.035) * 55;
        const towerBoost = (x > 320 && x < 650) ? 120 : ((x > 1320 && x < 1680) ? 140 : 0);
        const h = Math.min(440, baseH + towerBoost);
        ctxSky.lineTo(x, 1024 - h);
        ctxSky.lineTo(x + 24, 1024 - h);
    }
    // Bandra-Worli Sea Link iconic cable-stayed pylon
    ctxSky.lineTo(1520, 1024 - 380);
    ctxSky.lineTo(1530, 1024 - 380);
    ctxSky.lineTo(1548, 1024 - 170);
    ctxSky.lineTo(2048, 1024 - 150);
    ctxSky.lineTo(2048, 1024);
    ctxSky.lineTo(0, 1024);
    ctxSky.closePath();
    ctxSky.fill();

    // 4. LAYER 2: Midground Modernist Urban Towers with Organic Lit Windows
    const towers = [
        { x: 20,   w: 75,  h: 260, type: 'res', spire: false },
        { x: 110,  w: 95,  h: 350, type: 'com', spire: true },
        { x: 220,  w: 68,  h: 220, type: 'res', spire: false },
        { x: 305,  w: 115, h: 420, type: 'res', spire: false },
        { x: 435,  w: 88,  h: 310, type: 'com', spire: false },
        { x: 538,  w: 130, h: 465, type: 'com', spire: true },
        { x: 685,  w: 78,  h: 280, type: 'res', spire: false },
        { x: 780,  w: 108, h: 375, type: 'res', spire: false },
        { x: 905,  w: 82,  h: 250, type: 'res', spire: false },
        { x: 1005, w: 135, h: 445, type: 'com', spire: true },
        { x: 1155, w: 98,  h: 330, type: 'res', spire: false },
        { x: 1270, w: 120, h: 405, type: 'com', spire: false },
        { x: 1408, w: 88,  h: 290, type: 'res', spire: false },
        { x: 1515, w: 145, h: 475, type: 'com', spire: true },
        { x: 1675, w: 92,  h: 320, type: 'res', spire: false },
        { x: 1785, w: 115, h: 395, type: 'com', spire: false },
        { x: 1915, w: 98,  h: 270, type: 'res', spire: false }
    ];

    // Simple deterministic pseudo-random generator
    function pseudoRand(seed) {
        const x = Math.sin(seed) * 10000;
        return x - Math.floor(x);
    }

    towers.forEach((tw, tIdx) => {
        const topY = 1024 - tw.h;
        // Tower Body
        ctxSky.fillStyle = 'rgba(38, 28, 38, 0.96)';
        ctxSky.fillRect(tw.x, topY, tw.w, tw.h);

        // Rooftop Architecture (crown / mechanical penthouse / spire)
        if (tw.spire) {
            ctxSky.fillStyle = 'rgba(32, 24, 32, 0.98)';
            ctxSky.fillRect(tw.x + tw.w * 0.25, topY - 24, tw.w * 0.5, 24);
            ctxSky.fillRect(tw.x + tw.w * 0.45, topY - 55, tw.w * 0.1, 31);
            // Aviation warning light
            ctxSky.fillStyle = 'rgba(255, 60, 60, 0.85)';
            ctxSky.fillRect(tw.x + tw.w * 0.48, topY - 58, 4, 4);
        } else {
            ctxSky.fillStyle = 'rgba(32, 24, 32, 0.98)';
            ctxSky.fillRect(tw.x + tw.w * 0.15, topY - 12, tw.w * 0.7, 12);
        }

        // Windows strictly within tower bounds
        if (tw.type === 'res') {
            const winW = 4;
            const winH = 7;
            const stepX = 10;
            const stepY = 14;
            const padX = 7;
            const padY = 16;
            for (let wx = tw.x + padX; wx <= tw.x + tw.w - padX - winW; wx += stepX) {
                for (let wy = topY + padY; wy <= 1024 - 30; wy += stepY) {
                    const r = pseudoRand(wx * 17.1 + wy * 31.7 + tIdx * 99.3);
                    if (r < 0.40) {
                        const colR = pseudoRand(wx * 7.3 + wy * 13.9);
                        if (colR < 0.45) {
                            ctxSky.fillStyle = 'rgba(255, 218, 140, 0.88)'; // Warm incandescent 2700K
                        } else if (colR < 0.80) {
                            ctxSky.fillStyle = 'rgba(255, 185, 115, 0.82)'; // Cozy peach amber
                        } else {
                            ctxSky.fillStyle = 'rgba(255, 245, 220, 0.90)'; // Soft warm white
                        }
                        ctxSky.fillRect(wx, wy, winW, winH);
                    } else if (r < 0.65) {
                        ctxSky.fillStyle = 'rgba(48, 36, 46, 0.55)'; // Unlit dark glass
                        ctxSky.fillRect(wx, wy, winW, winH);
                    }
                }
            }
        } else {
            // Commercial Tower: Horizontal ribbon bands
            const winW = 10;
            const winH = 4;
            const stepX = 15;
            const stepY = 11;
            const padX = 8;
            const padY = 20;
            for (let wx = tw.x + padX; wx <= tw.x + tw.w - padX - winW; wx += stepX) {
                for (let wy = topY + padY; wy <= 1024 - 30; wy += stepY) {
                    const r = pseudoRand(wx * 19.3 + wy * 27.1 + tIdx * 77.1);
                    if (r < 0.46) {
                        const colR = pseudoRand(wx * 11.1 + wy * 19.7);
                        if (colR < 0.50) {
                            ctxSky.fillStyle = 'rgba(255, 240, 210, 0.90)'; // Crisp office warm white
                        } else if (colR < 0.82) {
                            ctxSky.fillStyle = 'rgba(255, 198, 130, 0.85)'; // Amber interior
                        } else {
                            ctxSky.fillStyle = 'rgba(200, 225, 245, 0.72)'; // Twilight reflection
                        }
                        ctxSky.fillRect(wx, wy, winW, winH);
                    } else if (r < 0.70) {
                        ctxSky.fillStyle = 'rgba(44, 32, 42, 0.50)'; // Dark unlit office
                        ctxSky.fillRect(wx, wy, winW, winH);
                    }
                }
            }
        }
    });

    // 5. LAYER 3: Soft Golden Atmospheric Horizon Mist
    const mistGrad = ctxSky.createLinearGradient(0, 800, 0, 1024);
    mistGrad.addColorStop(0.0, 'rgba(226, 149, 78, 0.0)');
    mistGrad.addColorStop(0.45, 'rgba(215, 135, 70, 0.32)');
    mistGrad.addColorStop(1.0, 'rgba(180, 100, 50, 0.58)');
    ctxSky.fillStyle = mistGrad;
    ctxSky.fillRect(0, 800, 2048, 224);

    const outPath = 'C:/Users/ADMIN/.gemini/antigravity/brain/a89496f6-6f7c-4a3f-b45b-cae80fa0337c/test_skyline_preview.png';
    fs.writeFileSync(outPath, cSky.toBuffer('image/png'));
    console.log(`Saved ${outPath}`);
}

generateSkyline();
