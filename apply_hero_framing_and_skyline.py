import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update bedroom north wall: replace solid box with architectural window opening & daylight backing
old_wall_code = "addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, -2.50);"
new_wall_code = """// Master Bedroom North Window Reveal & Envelopes (Architectural Window Opening)
addWall(0.40, WALL_H, 0.20, -4.10, WALL_H / 2, -2.50); // West reveal
addWall(0.45, WALL_H, 0.20, -1.975, WALL_H / 2, -2.50); // East reveal
addWall(1.70, 0.675, 0.20, -3.05, 0.3375, -2.50); // Window sill base
addWall(1.70, 0.625, 0.20, -3.05, WALL_H - 0.3125, -2.50); // Window lintel

// Soft morning daylight background plane behind bedroom window
const cBedSky = document.createElement('canvas');
cBedSky.width = 512;
cBedSky.height = 512;
const ctxBedSky = cBedSky.getContext('2d');
const bedSkyGrad = ctxBedSky.createLinearGradient(0, 0, 0, 512);
bedSkyGrad.addColorStop(0.0, '#E0EEF8');
bedSkyGrad.addColorStop(0.45, '#FFF2E2');
bedSkyGrad.addColorStop(1.0, '#FFDFC0');
ctxBedSky.fillStyle = bedSkyGrad;
ctxBedSky.fillRect(0, 0, 512, 512);
const bedSkyTex = new THREE.CanvasTexture(cBedSky);
bedSkyTex.colorSpace = THREE.SRGBColorSpace;
const bedDaylightMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(2.6, 2.2),
    new THREE.MeshBasicMaterial({ map: bedSkyTex, depthWrite: true })
);
bedDaylightMesh.position.set(-3.05, 1.45, -2.75);
materialGroup.add(bedDaylightMesh);"""

assert old_wall_code in content, "Could not find old bedroom wall code"
content = content.replace(old_wall_code, new_wall_code, 1)

# 2. Update bistro table height in buildBalcony
old_table_code = """    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.65, 0.65, -1.75);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.64, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.65, 0.32, -1.75);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.65 + Math.cos(cAngle) * 0.12, 0.68, -1.75 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }"""

new_table_code = """    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups (Elevated to 0.72m standard architectural height)
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.65, 0.72, -1.80);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.71, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.65, 0.355, -1.80);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.65 + Math.cos(cAngle) * 0.12, 0.75, -1.80 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }"""

assert old_table_code in content, "Could not find old table code"
content = content.replace(old_table_code, new_table_code, 1)

# 3. Replace buildSunsetBackdrop with photorealistic architectural Mumbai skyline
old_sky_start = "function buildSunsetBackdrop() {"
old_sky_end = "const skyBillboard = buildSunsetBackdrop();"

new_sky_code = """function buildSunsetBackdrop() {
    const group = new THREE.Group();

    // 1. High-Resolution 2048x1024 Master Mumbai Golden Sunset & Skyline Canvas
    const cSky = document.createElement('canvas');
    cSky.width = 2048;
    cSky.height = 1024;
    const ctxSky = cSky.getContext('2d');

    // Soft atmospheric sunset gradient tuned for ACESFilmicToneMapping
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

    // Broad horizontal atmospheric glow along the horizon (no harsh white sun dot)
    const sunGlow = ctxSky.createRadialGradient(1320, 740, 40, 1320, 740, 720);
    sunGlow.addColorStop(0.00, 'rgba(255, 218, 150, 0.38)');
    sunGlow.addColorStop(0.28, 'rgba(255, 175, 95, 0.22)');
    sunGlow.addColorStop(0.60, 'rgba(235, 125, 60, 0.10)');
    sunGlow.addColorStop(1.00, 'rgba(0, 0, 0, 0)');
    ctxSky.fillStyle = sunGlow;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // LAYER 1: Distant Mumbai High-Rise Silhouette & Bandra-Worli Sea Link Pylon
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

    // LAYER 2: Midground Modernist Urban Towers with Organic Lit Windows
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
            // Aviation warning beacon
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

    // LAYER 3: Soft Golden Atmospheric Horizon Mist
    const mistGrad = ctxSky.createLinearGradient(0, 800, 0, 1024);
    mistGrad.addColorStop(0.0, 'rgba(226, 149, 78, 0.0)');
    mistGrad.addColorStop(0.45, 'rgba(215, 135, 70, 0.32)');
    mistGrad.addColorStop(1.0, 'rgba(180, 100, 50, 0.58)');
    ctxSky.fillStyle = mistGrad;
    ctxSky.fillRect(0, 800, 2048, 224);

    const skyTex = new THREE.CanvasTexture(cSky);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyTex.anisotropy = maxAniso;

    // Master Opaque Sky Plane (depthWrite: true so Transmission Glass renders it crisp!)
    const skyPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(54, 27),
        new THREE.MeshBasicMaterial({ map: skyTex, depthWrite: true })
    );
    skyPlane.position.set(1.5, 4.2, -15.0);
    group.add(skyPlane);

    // Warm Volumetric Sun Shafts Streaming into the Balcony
    const sunBeamGroup = new THREE.Group();
    const cBeam = document.createElement('canvas');
    cBeam.width = 64;
    cBeam.height = 256;
    const ctxBeam = cBeam.getContext('2d');
    const bGrad = ctxBeam.createLinearGradient(0, 0, 0, 256);
    bGrad.addColorStop(0.0, 'rgba(255, 235, 175, 0.0)');
    bGrad.addColorStop(0.2, 'rgba(255, 220, 150, 0.45)');
    bGrad.addColorStop(0.65, 'rgba(255, 200, 120, 0.28)');
    bGrad.addColorStop(1.0, 'rgba(255, 180, 90, 0.0)');
    ctxBeam.fillStyle = bGrad;
    ctxBeam.fillRect(0, 0, 64, 256);

    const beamTex = new THREE.CanvasTexture(cBeam);
    beamTex.colorSpace = THREE.SRGBColorSpace;
    const beamMat = new THREE.MeshBasicMaterial({
        map: beamTex,
        transparent: true,
        opacity: 0.14,
        blending: THREE.AdditiveBlending,
        side: THREE.DoubleSide,
        depthWrite: false
    });

    const beam1 = new THREE.Mesh(new THREE.PlaneGeometry(0.85, 4.2), beamMat);
    beam1.position.set(1.05, 1.70, -1.90);
    beam1.rotation.set(0.38, -0.42, 0.55);
    sunBeamGroup.add(beam1);

    const beam2 = new THREE.Mesh(new THREE.PlaneGeometry(1.10, 4.6), beamMat);
    beam2.position.set(1.75, 1.85, -1.85);
    beam2.rotation.set(0.36, -0.40, 0.52);
    sunBeamGroup.add(beam2);

    const beam3 = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 4.4), beamMat);
    beam3.position.set(2.45, 1.75, -1.80);
    beam3.rotation.set(0.35, -0.38, 0.50);
    sunBeamGroup.add(beam3);

    group.add(sunBeamGroup);
    return group;
}"""

p1 = content.find(old_sky_start)
p2 = content.find(old_sky_end)
assert p1 != -1 and p2 != -1, "Could not find buildSunsetBackdrop boundaries"
content = content[:p1] + new_sky_code + "\n\n" + content[p2:]

# 4. Hide blueprintMesh when 3D walls rise (progress >= 0.15)
old_render_wall = "wallGroup.visible = (camState.clipHeight <= 1.30);"
new_render_wall = """wallGroup.visible = (camState.clipHeight <= 1.30);
    blueprintMesh.visible = (camState.progress < 0.15);"""

assert old_render_wall in content, "Could not find wallGroup.visible in render"
content = content.replace(old_render_wall, new_render_wall, 1)

old_apply_wall = "wallGroup.visible = (camState.clipHeight <= 1.30);"
new_apply_wall = """wallGroup.visible = (camState.clipHeight <= 1.30);
    blueprintMesh.visible = (p < 0.15);"""

assert old_apply_wall in content, "Could not find wallGroup.visible in applyProgressToScene"
content = content.replace(old_apply_wall, new_apply_wall, 1)

# 5. Update Stop 5, Stop 6, Stop 7 Waypoints in GSAP timeline
old_stops = """// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.16,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.40,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%): Glide West Straight Through Open Bedroom Doorway (x = -1.825, z = -0.20)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.85,
    posY: 1.50,
    posZ: -0.20,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%): Settle at Doorway Framing (Diagonally Across Bed, Headboard, Wardrobe & Window)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.50,
    posZ: -0.28,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%): Master Bedroom Steady Hold (Open & Naturally Lit Doorway Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.50,
    posZ: -0.28,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Slide Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.98,
    posY: 1.52,
    posZ: -0.30,
    targetX: 0.98,
    targetY: 1.45,
    targetZ: -1.95,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Walk Straight Forward Through Open 1.15m Left Sliding Doorway onto Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.45,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Settle on Teak Deck for Expansive Skyline View
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides smoothly forward to the edge of the glass balustrade overlooking panoramic skyline.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.50,
    posY: 1.55,
    posZ: -2.18,
    targetX: 1.50,
    targetY: 1.48,
    targetZ: -8.00,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

new_stops = """// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.16,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.40,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%): Glide West to Open Bedroom Doorway (x = -1.75, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%): Settle at Doorway Framing (Diagonally Across Headboard, Bed, Wardrobe & Window)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%): Master Bedroom Steady Hold (Open & Naturally Lit Doorway Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBedroomX: -4.15,
    posX: -1.75,
    posY: 1.50,
    posZ: -0.15,
    targetX: -3.00,
    targetY: 1.05,
    targetZ: -0.95,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.85,
    posY: 1.50,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Slide Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.98,
    posY: 1.48,
    posZ: -0.65,
    targetX: 1.65,
    targetY: 1.35,
    targetZ: -3.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Step Forward into Enclosed Balcony Deck
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    sweepBalconyZ: -2.35,
    posX: 1.10,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.25,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Enclosed Balcony Steady Hold (Architectural Foreground + Sunset Skyline)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    sweepBalconyZ: -2.35,
    posX: 1.10,
    posY: 1.48,
    posZ: -1.35,
    targetX: 1.95,
    targetY: 1.25,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides gently forward along teak deck, maintaining bistro table & planter foreground
tl.to(camState, {
    clipHeight: 2.85,
    fov: 48.0,
    posX: 1.35,
    posY: 1.50,
    posZ: -1.65,
    targetX: 1.75,
    targetY: 1.35,
    targetZ: -6.50,
    balconyDoorX: 1.18,
    duration: 0.08,
    ease: 'power1.out'
});"""

assert old_stops in content, "Could not find old stops timeline code"
content = content.replace(old_stops, new_stops, 1)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied hero framing, architectural window opening, and Mumbai sunset skyline upgrade to script.js!")
