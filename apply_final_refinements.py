import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("\r\n", "\n")

# 1. Replace buildSunsetBackdrop with integrated high-fidelity Mumbai skyline on cSky
old_backdrop_start = "// E. MUMBAI SUNSET PARALLAX SKYLINE & VOLUMETRIC SUN SHAFTS\n// ============================================================================\nfunction buildSunsetBackdrop() {"
old_backdrop_end = "const skyBillboard = buildSunsetBackdrop();"

new_backdrop = """// E. MUMBAI SUNSET PARALLAX SKYLINE & VOLUMETRIC SUN SHAFTS
// ============================================================================
function buildSunsetBackdrop() {
    const group = new THREE.Group();

    // 1. High-Resolution 2048x1024 Master Mumbai Golden Sunset & Skyline Canvas
    const cSky = document.createElement('canvas');
    cSky.width = 2048;
    cSky.height = 1024;
    const ctxSky = cSky.getContext('2d');

    // Rich Twilight to Golden Horizon Sunset Gradient
    const skyGrad = ctxSky.createLinearGradient(0, 0, 0, 1024);
    skyGrad.addColorStop(0.00, '#1E2B3E'); // Deep dusk twilight navy
    skyGrad.addColorStop(0.28, '#4D3B4C'); // Twilight mauve
    skyGrad.addColorStop(0.50, '#9E5B4B'); // Warm terracotta peach
    skyGrad.addColorStop(0.68, '#DC8B52'); // Golden hour amber
    skyGrad.addColorStop(0.82, '#FBC882'); // Radiant golden horizon glow
    skyGrad.addColorStop(0.92, '#E2A875'); // Atmospheric horizon mist
    skyGrad.addColorStop(1.00, '#C88856'); // Ground haze
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // Radiant Sun Core & Vast Atmospheric Corona Glow
    const sunGlow = ctxSky.createRadialGradient(1280, 720, 25, 1280, 720, 520);
    sunGlow.addColorStop(0.00, 'rgba(255, 255, 245, 1.00)');
    sunGlow.addColorStop(0.20, 'rgba(255, 230, 165, 0.75)');
    sunGlow.addColorStop(0.55, 'rgba(245, 170, 95, 0.35)');
    sunGlow.addColorStop(1.00, 'rgba(0, 0, 0, 0)');
    ctxSky.fillStyle = sunGlow;
    ctxSky.fillRect(0, 0, 2048, 1024);

    // ------------------------------------------------------------------------
    // LAYER 1: Distant Mumbai High-Rise Skyline & Bandra-Worli Sea Link Pylon
    // ------------------------------------------------------------------------
    ctxSky.fillStyle = 'rgba(75, 52, 65, 0.72)'; // Soft dusky mauve silhouette
    ctxSky.beginPath();
    ctxSky.moveTo(0, 1024);
    for (let x = 0; x < 2048; x += 36) {
        const baseH = 180 + Math.sin(x * 0.015) * 80 + Math.cos(x * 0.035) * 60;
        const towerBoost = (x > 350 && x < 680) ? 130 : ((x > 1350 && x < 1700) ? 150 : 0);
        const h = Math.min(460, baseH + towerBoost);
        ctxSky.lineTo(x, 1024 - h);
        ctxSky.lineTo(x + 28, 1024 - h);
    }
    // Bandra-Worli Sea Link iconic cable-stayed pylon
    ctxSky.lineTo(1520, 1024 - 390);
    ctxSky.lineTo(1532, 1024 - 390);
    ctxSky.lineTo(1550, 1024 - 170);
    ctxSky.lineTo(2048, 1024 - 160);
    ctxSky.lineTo(2048, 1024);
    ctxSky.lineTo(0, 1024);
    ctxSky.closePath();
    ctxSky.fill();

    // ------------------------------------------------------------------------
    // LAYER 2: Midground Modernist Urban Towers & Illuminated Golden Windows
    // ------------------------------------------------------------------------
    ctxSky.fillStyle = 'rgba(42, 30, 40, 0.95)'; // Deep architectural charcoal-plum
    ctxSky.beginPath();
    ctxSky.moveTo(0, 1024);
    for (let x = 0; x < 2048; x += 48) {
        const baseH = 150 + Math.sin(x * 0.02) * 75 + Math.cos(x * 0.05) * 55;
        const pinnacle = (x % 192 === 0) ? 110 : ((x % 96 === 0) ? 65 : 0);
        const bh = Math.min(430, baseH + pinnacle);
        ctxSky.lineTo(x, 1024 - bh);
        ctxSky.lineTo(x + 40, 1024 - bh);
    }
    ctxSky.lineTo(2048, 1024);
    ctxSky.lineTo(0, 1024);
    ctxSky.closePath();
    ctxSky.fill();

    // Thousands of Warm Illuminated Evening Windows across Mumbai Towers
    ctxSky.fillStyle = 'rgba(255, 230, 160, 0.88)';
    for (let x = 20; x < 2020; x += 28) {
        for (let y = 620; y < 980; y += 18) {
            if (Math.sin(x * 12.3 + y * 7.1) > 0.15) {
                ctxSky.fillRect(x + Math.sin(y * 0.05) * 4, y, 5, 7);
            }
        }
    }

    // ------------------------------------------------------------------------
    // LAYER 3: Soft Golden Atmospheric Horizon Mist
    // ------------------------------------------------------------------------
    const mistGrad = ctxSky.createLinearGradient(0, 780, 0, 1024);
    mistGrad.addColorStop(0.0, 'rgba(251, 200, 130, 0.0)');
    mistGrad.addColorStop(0.4, 'rgba(251, 200, 130, 0.38)');
    mistGrad.addColorStop(1.0, 'rgba(215, 145, 90, 0.65)');
    ctxSky.fillStyle = mistGrad;
    ctxSky.fillRect(0, 780, 2048, 244);

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
    bGrad.addColorStop(0.2, 'rgba(255, 220, 150, 0.55)');
    bGrad.addColorStop(0.65, 'rgba(255, 200, 120, 0.35)');
    bGrad.addColorStop(1.0, 'rgba(255, 180, 90, 0.0)');
    ctxBeam.fillStyle = bGrad;
    ctxBeam.fillRect(0, 0, 64, 256);

    const beamTex = new THREE.CanvasTexture(cBeam);
    beamTex.colorSpace = THREE.SRGBColorSpace;
    const beamMat = new THREE.MeshBasicMaterial({
        map: beamTex,
        transparent: true,
        opacity: 0.32,
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

    // Floating Golden Light Motes
    const moteGeo = new THREE.BufferGeometry();
    const motePos = new Float32Array(50 * 3);
    for (let i = 0; i < 50; i++) {
        motePos[i * 3 + 0] = 0.5 + Math.random() * 2.2;
        motePos[i * 3 + 1] = 0.4 + Math.random() * 1.8;
        motePos[i * 3 + 2] = -2.3 + Math.random() * 1.4;
    }
    moteGeo.setAttribute('position', new THREE.BufferAttribute(motePos, 3));
    const moteMat = new THREE.PointsMaterial({
        color: 0xFFEAB5,
        size: 0.035,
        transparent: true,
        opacity: 0.65,
        blending: THREE.AdditiveBlending
    });
    group.add(new THREE.Points(moteGeo, moteMat));

    return group;
}

"""

s_idx = content.find(old_backdrop_start)
e_idx = content.find(old_backdrop_end)

if s_idx != -1 and e_idx != -1:
    content = content[:s_idx] + new_backdrop + content[e_idx:]
    print("[OK] Replaced buildSunsetBackdrop with integrated high-res Mumbai skyline")
else:
    print(f"[ERROR] Could not find buildSunsetBackdrop boundaries: {s_idx}, {e_idx}")

# 2. Update Stop 5, Stop 6, Stop 7 Waypoints
old_stop5_start = "// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM ENTRANCE:"
old_stop7_end = "// ----------------------------------------------------------------------------\n// 13. REAL-TIME RENDERING LOOP"

new_stops_567 = """// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM ENTRANCE:
// Eye level (Y = 1.45m) looking diagonally across the full bed, headboard, warm pendant light, and window!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — GLIDE OUT OF BEDROOM INTO PASSAGE:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.55,
    posZ: -0.10,
    targetX: 0.85,
    targetY: 1.50,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%) — GLIDE ACROSS LIVING & BALCONY SLIDERS OPEN:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.55,
    posZ: -0.55,
    targetX: 1.50,
    targetY: 1.40,
    targetZ: -2.20,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%) — STEP ONTO TEAK BALCONY DECK & LEVEL CAMERA HORIZON:
// Eye level Y = 1.45m looking horizontally out through glass toward Mumbai golden-hour skyline!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.35,
    posY: 1.45,
    posZ: -1.45,
    targetX: 1.50,
    targetY: 1.30,
    targetZ: -6.00,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%) — BALCONY DECK STEADY HOLD (Horizontal Horizon Framing):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBalconyZ: -2.35,
    posX: 1.35,
    posY: 1.45,
    posZ: -1.45,
    targetX: 1.50,
    targetY: 1.30,
    targetZ: -6.00,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides smoothly forward to the edge of the glass balustrade overlooking panoramic skyline.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 50.0,
    posX: 1.50,
    posY: 1.45,
    posZ: -2.15,
    targetX: 1.50,
    targetY: 1.35,
    targetZ: -8.00,
    balconyDoorX: -0.90,
    duration: 0.08,
    ease: 'power1.out'
});
"""

s5_idx = content.find(old_stop5_start)
e7_idx = content.find(old_stop7_end)

if s5_idx != -1 and e7_idx != -1:
    content = content[:s5_idx] + new_stops_567 + content[e7_idx:]
    print("[OK] Replaced Stops 5, 6, 7 waypoints with perfect reframing")
else:
    print(f"[ERROR] Could not find stops 5-7 boundaries: {s5_idx}, {e7_idx}")

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] script.js updated successfully with final refinements!")
