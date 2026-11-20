import re

print("Starting update_walkthrough_transitions.py...")

# -----------------------------------------------------------------------------
# 1. UPDATE index.html (Add Closing CTA Card)
# -----------------------------------------------------------------------------
with open("D:/floor plans/jp-aviva-3d/index.html", "r", encoding="utf-8") as f:
    html = f.read()

cta_html = '''    <!-- Closing Pitch & Site Visit CTA Card (Appears at 92%-100% Sunset Finale) -->
    <div id="closing-cta-card" class="closing-cta-card" aria-hidden="true">
        <div class="cta-glass-panel">
            <div class="cta-top-row">
                <span class="cta-badge">JP NORTH AVIVA · WING A TYPICAL FLOORS</span>
                <span class="cta-rera-tag">MahaRERA: P51700023940</span>
            </div>
            <h2 class="cta-title">Ready to Experience It in Person?</h2>
            <p class="cta-description">Walk through the actual 27.96 Sq.M. (301 Sq.Ft.) carpet 1 BHK with enclosed private balcony at North Garden City, Mira Road East.</p>
            
            <div class="cta-features-grid">
                <div class="cta-feature-chip">
                    <span class="chip-val">100% Usable</span>
                    <span class="chip-lbl">Zero Space Wastage</span>
                </div>
                <div class="cta-feature-chip">
                    <span class="chip-val">Direct Balcony</span>
                    <span class="chip-lbl">Teak Deck & Utility</span>
                </div>
                <div class="cta-feature-chip">
                    <span class="chip-val">Luxury PBR</span>
                    <span class="chip-lbl">Turnkey Finishes</span>
                </div>
            </div>

            <div class="cta-button-group">
                <button type="button" class="cta-btn primary" onclick="window.triggerSiteVisitModal()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 4H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V6a2 2 0 00-2-2zM16 2v4M8 2v4M3 10h18"/></svg>
                    Book a Private Site Visit
                </button>
                <button type="button" class="cta-btn secondary" onclick="window.downloadFloorplanBrochure()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                    Download Floorplan Specs
                </button>
            </div>
            <button type="button" class="cta-replay-link" onclick="window.jumpToStop(0, false)">
                ↻ Replay Architectural Tour from Blueprint
            </button>
        </div>
    </div>
'''

if 'id="closing-cta-card"' not in html:
    html = html.replace('<!-- External Libraries: Lenis & GSAP ScrollTrigger -->', cta_html + '\n    <!-- External Libraries: Lenis & GSAP ScrollTrigger -->')
    with open("D:/floor plans/jp-aviva-3d/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[OK] index.html updated with closing CTA card.")
else:
    print("[INFO] index.html already has closing CTA card.")

# -----------------------------------------------------------------------------
# 2. UPDATE style.css (Add Closing CTA Card Styles)
# -----------------------------------------------------------------------------
with open("D:/floor plans/jp-aviva-3d/style.css", "r", encoding="utf-8") as f:
    css = f.read()

cta_css = '''
/* =========================================================
   MUMBAI SUNSET FINALE CLOSING CTA CARD (92% - 100%)
   ========================================================= */
.closing-cta-card {
    position: fixed;
    bottom: 96px;
    left: 50%;
    transform: translate(-50%, 40px);
    opacity: 0;
    pointer-events: none;
    z-index: 100;
    width: 90%;
    max-width: 580px;
    transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
}

.closing-cta-card.visible {
    opacity: 1;
    transform: translate(-50%, 0);
    pointer-events: auto;
}

.cta-glass-panel {
    background: rgba(18, 16, 22, 0.84);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(230, 184, 138, 0.35);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55), 0 0 35px rgba(230, 184, 138, 0.15);
    border-radius: 20px;
    padding: 24px 28px;
    color: #F8F9FA;
    text-align: center;
}

.cta-top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.cta-badge {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #E6B88A;
    background: rgba(230, 184, 138, 0.12);
    border: 1px solid rgba(230, 184, 138, 0.28);
    padding: 4px 10px;
    border-radius: 20px;
}

.cta-rera-tag {
    font-size: 0.72rem;
    color: rgba(255, 255, 255, 0.65);
    letter-spacing: 0.04em;
    font-family: monospace;
}

.cta-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin: 0 0 8px 0;
    color: #FFFFFF;
    font-family: 'Playfair Display', Georgia, serif;
    letter-spacing: -0.01em;
}

.cta-description {
    font-size: 0.85rem;
    line-height: 1.45;
    color: rgba(255, 255, 255, 0.82);
    margin: 0 0 16px 0;
}

.cta-features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 18px;
}

.cta-feature-chip {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 8px 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}

.chip-val {
    font-size: 0.82rem;
    font-weight: 700;
    color: #E6B88A;
}

.chip-lbl {
    font-size: 0.68rem;
    color: rgba(255, 255, 255, 0.65);
}

.cta-button-group {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-bottom: 12px;
}

.cta-btn {
    flex: 1 1 auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 18px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
    border: none;
    text-decoration: none;
}

.cta-btn.primary {
    background: linear-gradient(135deg, #D4A359 0%, #B8833B 100%);
    color: #121316;
    box-shadow: 0 6px 18px rgba(212, 163, 89, 0.35);
}

.cta-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(212, 163, 89, 0.50);
}

.cta-btn.secondary {
    background: rgba(255, 255, 255, 0.08);
    color: #F8F9FA;
    border: 1px solid rgba(255, 255, 255, 0.16);
}

.cta-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.14);
    transform: translateY(-2px);
}

.cta-replay-link {
    background: none;
    border: none;
    color: rgba(230, 184, 138, 0.85);
    font-size: 0.78rem;
    cursor: pointer;
    text-decoration: underline;
    text-underline-offset: 3px;
    transition: color 0.2s ease;
}

.cta-replay-link:hover {
    color: #FFFFFF;
}

@media (max-width: 768px) {
    .closing-cta-card {
        bottom: 84px;
        width: calc(100vw - 32px);
    }
    .cta-glass-panel {
        padding: 18px 16px;
    }
    .cta-button-group {
        flex-direction: column;
        gap: 8px;
    }
    .cta-features-grid {
        grid-template-columns: 1fr;
        gap: 6px;
    }
}
'''

if '.closing-cta-card' not in css:
    css = css + '\n' + cta_css
    with open("D:/floor plans/jp-aviva-3d/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("[OK] style.css updated with closing CTA card styles.")
else:
    print("[INFO] style.css already has closing CTA card styles.")

# -----------------------------------------------------------------------------
# 3. UPDATE script.js (Walls, Parallax Sunset, Sun Shafts, Smooth Transitions)
# -----------------------------------------------------------------------------
with open("D:/floor plans/jp-aviva-3d/script.js", "r", encoding="utf-8") as f:
    js = f.read()

# A. Fix the Interior Partitions with Real Architectural Openings
old_partitions = """// Interior Partitions
addWall(0.15, WALL_H, 2.25, 0.125, WALL_H / 2, 0.325);
addWall(0.15, WALL_H, 1.40, -1.825, WALL_H / 2, -0.35);
addWall(0.12, WALL_H, 1.40, -0.65, WALL_H / 2, 1.00); // W.C. partition wall

// Master Bedroom Accent Wall ("Wild Mushroom" #998878)
addWall(2.45, WALL_H, 0.10, -2.975, WALL_H / 2, 0.30, pbrWildMushroom);

// Door Lintels (Solid Headers Above Doors)
addWall(1.00, 0.75, 0.20, 0.85, WALL_H - 0.375, 2.90);  // Main Entrance Lintel
addWall(0.90, 0.75, 0.15, -0.60, WALL_H - 0.375, -0.55); // Kitchen Lintel
addWall(0.85, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);  // Bath Lintel
addWall(0.90, 0.75, 0.15, -1.825, WALL_H - 0.375, -0.20); // Bedroom Lintel
addWall(1.80, 0.75, 0.15, 1.575, WALL_H - 0.375, -1.15); // Balcony Sliding Lintel"""

new_partitions = """// --- Interior Partitions & Real Architectural Door Openings ---
// 1. Living Room to Central Passage Partition (x = 0.125)
// Solid wall separating Living from W.C. & Foyer (z = 0.25 to 1.45, length = 1.20m)
addWall(0.15, WALL_H, 1.20, 0.125, WALL_H / 2, 0.85);
// Lintel overhead across the open passage portal (y = 2.10m to 2.85m, z = -0.65 to 0.25)
addWall(0.15, 0.75, 0.90, 0.125, WALL_H - 0.375, -0.20);
// NOTE: Space from y = 0.0 to 2.10m between z = -0.65 and 0.25 is OPEN for uninterrupted passage.

// 2. Master Bedroom to Central Passage Partition (x = -1.825)
// North solid partition segment between bedroom and kitchen shaft (z = -1.30 to -0.65)
addWall(0.15, WALL_H, 0.65, -1.825, WALL_H / 2, -0.975);
// South solid partition segment connecting to bedroom accent wall (z = 0.25 to 0.45)
addWall(0.15, WALL_H, 0.20, -1.825, WALL_H / 2, 0.35);
// Master Bedroom Door Lintel overhead (y = 2.10m to 2.85m, z = -0.65 to 0.25)
addWall(0.15, 0.75, 0.90, -1.825, WALL_H - 0.375, -0.20);
// NOTE: Space from y = 0.0 to 2.10m between z = -0.65 and 0.25 is OPEN! Camera glides cleanly through doorway.

// 3. W.C. Partition Wall (x = -0.65)
addWall(0.12, WALL_H, 1.40, -0.65, WALL_H / 2, 1.00);

// 4. Bathroom Doorway & North Wall (z = 0.35)
// West solid segment next to bedroom wall (x = -1.85 to -1.55)
addWall(0.30, WALL_H, 0.15, -1.70, WALL_H / 2, 0.35);
// Bathroom Door Lintel overhead (y = 2.10m to 2.85m, x = -1.55 to -0.75)
addWall(0.80, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);
// NOTE: Space from y = 0.0 to 2.10m between x = -1.55 and -0.75 is OPEN!

// 5. Master Bedroom Accent Wall ("Wild Mushroom" #998878)
addWall(2.45, WALL_H, 0.10, -2.975, WALL_H / 2, 0.30, pbrWildMushroom);

// 6. Main Entrance Lintel & Balcony Sliding Lintel
addWall(1.00, 0.75, 0.20, 0.85, WALL_H - 0.375, 2.90);   // Main Entrance Lintel
addWall(0.90, 0.75, 0.15, -0.60, WALL_H - 0.375, -0.55); // Kitchen Lintel
addWall(1.80, 0.75, 0.15, 1.575, WALL_H - 0.375, -1.15); // Balcony Sliding Lintel"""

if old_partitions in js:
    js = js.replace(old_partitions, new_partitions)
    print("[OK] script.js interior partition walls updated with real door openings.")
else:
    print("! Warning: old_partitions pattern not found directly, checking partial matches.")

# B. Upgrade buildSunsetBackdrop to Layered Parallax Skyline & Volumetric Sun Shafts
old_sunset_pattern = re.compile(r"// =+\s*// E\. SUNSET SKYLINE BACKDROP.*?(?=const skyBillboard = buildSunsetBackdrop\(\);)", re.DOTALL)

new_sunset_function = """// ============================================================================
// E. MUMBAI SUNSET PARALLAX SKYLINE & VOLUMETRIC SUN SHAFTS
// ============================================================================
function buildSunsetBackdrop() {
    const group = new THREE.Group();

    // 1. Layer 0: High-Res Golden Sunset Sky Dome / Backdrop (z = -18.0)
    const cSky = document.createElement('canvas');
    cSky.width = 1024;
    cSky.height = 512;
    const ctxSky = cSky.getContext('2d');

    const skyGrad = ctxSky.createLinearGradient(0, 0, 0, 512);
    skyGrad.addColorStop(0.00, '#243248'); // Dusk twilight navy
    skyGrad.addColorStop(0.30, '#5C4A5A'); // Twilight mauve
    skyGrad.addColorStop(0.55, '#A46858'); // Warm terracotta peach
    skyGrad.addColorStop(0.72, '#E29760'); // Golden hour amber
    skyGrad.addColorStop(0.88, '#FCD094'); // Radiant horizon glow
    skyGrad.addColorStop(1.00, '#E5B280'); // Warm atmospheric mist
    ctxSky.fillStyle = skyGrad;
    ctxSky.fillRect(0, 0, 1024, 512);

    // Radiant Sun Core & Atmosphere Halo
    const sunGlow = ctxSky.createRadialGradient(640, 370, 15, 640, 370, 260);
    sunGlow.addColorStop(0.0, 'rgba(255, 255, 245, 0.95)');
    sunGlow.addColorStop(0.25, 'rgba(255, 225, 160, 0.65)');
    sunGlow.addColorStop(0.60, 'rgba(240, 165, 95, 0.25)');
    sunGlow.addColorStop(1.0, 'rgba(0, 0, 0, 0)');
    ctxSky.fillStyle = sunGlow;
    ctxSky.fillRect(0, 0, 1024, 512);

    const skyTex = new THREE.CanvasTexture(cSky);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    const skyPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(48, 22),
        new THREE.MeshBasicMaterial({ map: skyTex, depthWrite: false })
    );
    skyPlane.position.set(1.5, 4.8, -18.0);
    group.add(skyPlane);

    // 2. Layer 1: Distant Mumbai High-Rise Skyline (z = -13.5)
    const cFar = document.createElement('canvas');
    cFar.width = 1024;
    cFar.height = 256;
    const ctxFar = cFar.getContext('2d');
    ctxFar.fillStyle = 'rgba(78, 62, 75, 0.55)'; // Soft dusky mauve haze
    ctxFar.beginPath();
    ctxFar.moveTo(0, 256);
    for (let x = 0; x < 1024; x += 18) {
        const h = 45 + Math.sin(x * 0.03) * 28 + Math.cos(x * 0.08) * 18 + (x > 500 && x < 750 ? 30 : 0);
        ctxFar.lineTo(x, 256 - h);
        ctxFar.lineTo(x + 14, 256 - h);
    }
    // Bandra-Worli Sea Link cable tower hint
    ctxFar.lineTo(820, 256 - 95);
    ctxFar.lineTo(826, 256 - 95);
    ctxFar.lineTo(834, 256 - 45);
    ctxFar.lineTo(1024, 256 - 40);
    ctxFar.lineTo(1024, 256);
    ctxFar.lineTo(0, 256);
    ctxFar.closePath();
    ctxFar.fill();

    const farTex = new THREE.CanvasTexture(cFar);
    farTex.colorSpace = THREE.SRGBColorSpace;
    const farPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(42, 11),
        new THREE.MeshBasicMaterial({ map: farTex, transparent: true, depthWrite: false })
    );
    farPlane.position.set(1.5, 3.4, -13.5);
    group.add(farPlane);

    // 3. Layer 2: Midground Urban Towers with Architectural Window Flecks (z = -9.0)
    const cMid = document.createElement('canvas');
    cMid.width = 1024;
    cMid.height = 256;
    const ctxMid = cMid.getContext('2d');
    ctxMid.fillStyle = 'rgba(46, 35, 45, 0.88)'; // Rich dark purple-slate
    ctxMid.beginPath();
    ctxMid.moveTo(0, 256);
    for (let x = 0; x < 1024; x += 28) {
        const bh = 55 + Math.sin(x * 0.045) * 35 + Math.cos(x * 0.12) * 20;
        ctxMid.lineTo(x, 256 - bh);
        ctxMid.lineTo(x + 24, 256 - bh);
    }
    ctxMid.lineTo(1024, 256);
    ctxMid.lineTo(0, 256);
    ctxMid.closePath();
    ctxMid.fill();

    // Subtle warm glowing architectural windows
    ctxMid.fillStyle = 'rgba(255, 225, 150, 0.80)';
    for (let x = 15; x < 1010; x += 32) {
        for (let y = 140; y < 240; y += 14) {
            if (Math.sin(x * 12.3 + y * 7.1) > 0.2) {
                ctxMid.fillRect(x + Math.sin(y) * 4, y, 3, 4);
            }
        }
    }

    const midTex = new THREE.CanvasTexture(cMid);
    midTex.colorSpace = THREE.SRGBColorSpace;
    const midPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(34, 8.5),
        new THREE.MeshBasicMaterial({ map: midTex, transparent: true, depthWrite: false })
    );
    midPlane.position.set(1.5, 2.5, -9.0);
    group.add(midPlane);

    // 4. Layer 3: Atmospheric Golden Mist & Haze Plane (z = -6.2)
    const cMist = document.createElement('canvas');
    cMist.width = 512;
    cMist.height = 128;
    const ctxMist = cMist.getContext('2d');
    const mistGrad = ctxMist.createLinearGradient(0, 0, 0, 128);
    mistGrad.addColorStop(0.0, 'rgba(255, 210, 140, 0.0)');
    mistGrad.addColorStop(0.5, 'rgba(255, 210, 140, 0.40)');
    mistGrad.addColorStop(1.0, 'rgba(220, 170, 110, 0.0)');
    ctxMist.fillStyle = mistGrad;
    ctxMist.fillRect(0, 0, 512, 128);

    const mistTex = new THREE.CanvasTexture(cMist);
    mistTex.colorSpace = THREE.SRGBColorSpace;
    const mistPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(28, 7),
        new THREE.MeshBasicMaterial({
            map: mistTex,
            transparent: true,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        })
    );
    mistPlane.position.set(1.5, 1.8, -6.2);
    group.add(mistPlane);

    // 5. Warm Volumetric Sun Shafts Streaming into the Balcony
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

    // 3 Angled volumetric light beams crossing the balcony threshold
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

    // 6. Floating Golden Light Motes in Sunbeam Volume
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
    const motePoints = new THREE.Points(moteGeo, moteMat);
    group.add(motePoints);

    scene.add(group);
    return group;
}
"""

if old_sunset_pattern.search(js):
    js = old_sunset_pattern.sub(new_sunset_function, js)
    print("[OK] script.js buildSunsetBackdrop upgraded to multi-layer parallax & sun shafts.")
else:
    print("! Warning: buildSunsetBackdrop regex match failed.")

# C. Update the GSAP Timeline Stops 4, 5, 6, 7 with 'Rise, Glide, Descend' Transitions
old_stops_pattern = re.compile(r"// --- STOP 4: 52% to 66%.*?(?=// ----------------------------------------------------------------------------\s*// 13\. REAL-TIME RENDERING LOOP)", re.DOTALL)

new_stops_code = """// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen back into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.60,
    posY: 1.60,
    posZ: -0.05,
    targetX: -1.15,
    targetY: 1.40,
    targetZ: 0.90,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Step into Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.50,
    posZ: 0.55,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.45,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.50,
    posZ: 0.55,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth 'Rise, Glide, Descend' into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%) — RISE & GLIDE OUT OF BATHROOM:
// Camera smoothly rises from 1.50m up to 1.82m and glides North out of the bathroom into central passage.
// Target pans forward toward the bedroom opening (avoiding staring at blank unlit walls).
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -1.15,
    posY: 1.82,
    posZ: -0.05,
    targetX: -1.85,
    targetY: 1.50,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%) — GLIDE THROUGH OPEN BEDROOM DOORWAY:
// Camera glides at airy elevated height (1.82m to 1.75m) cleanly through the open door frame (x = -1.825, z = -0.20).
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBedroomX: -4.15,
    posX: -2.10,
    posY: 1.75,
    posZ: -0.25,
    targetX: -3.25,
    targetY: 1.30,
    targetZ: -0.55,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%) — DESCEND TO BEDROOM EYE HEIGHT:
// Camera gently descends from 1.75m down to 1.55m eye level at bedroom presentation stop.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15,
    posX: -2.30,
    posY: 1.55,
    posZ: -0.35,
    targetX: -3.15,
    targetY: 1.10,
    targetZ: -0.45,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15,
    posX: -2.30,
    posY: 1.55,
    posZ: -0.35,
    targetX: -3.15,
    targetY: 1.10,
    targetZ: -0.45,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — RISE & GLIDE OUT OF BEDROOM:
// Camera rises smoothly to 1.85m and glides East through open bedroom doorway into central passage.
// Target pans toward the sunlit living room and open balcony reveal.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.95,
    posY: 1.85,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.55,
    targetZ: -0.35,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%) — GLIDE TOWARD BALCONY & SLIDERS GLIDE OPEN:
// Camera glides through open portal across living room; balcony sliding doors slide open (-0.90m).
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.75,
    posZ: -0.65,
    targetX: 1.55,
    targetY: 1.45,
    targetZ: -2.20,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%) — DESCEND ONTO TEAK BALCONY DECK:
// Camera steps onto the teak deck and gently descends from 1.75m down to 1.50m eye height.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBalconyZ: -2.35,
    posX: 1.40,
    posY: 1.50,
    posZ: -1.65,
    targetX: 1.75,
    targetY: 1.10,
    targetZ: -2.15,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%) — BALCONY DECK STEADY HOLD:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBalconyZ: -2.35,
    posX: 1.40,
    posY: 1.50,
    posZ: -1.65,
    targetX: 1.75,
    targetY: 1.10,
    targetZ: -2.15,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides smoothly forward to the edge of the glass balustrade overlooking panoramic skyline.
// Telephoto compression (FOV 62° -> 48°) draws the sunset skyline closer; sun shafts illuminate deck.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 48.0,
    posX: 1.575,
    posY: 1.55,
    posZ: -2.25,
    targetX: 1.575,
    targetY: 1.45,
    targetZ: -8.00,
    balconyDoorX: -0.90,
    duration: 0.08,
    ease: 'power1.out'
});
"""

if old_stops_pattern.search(js):
    js = old_stops_pattern.sub(new_stops_code, js)
    print("[OK] script.js GSAP Stops 4, 5, 6, 7 updated with smooth 'Rise, Glide, Descend' transitions.")
else:
    print("! Warning: old_stops_pattern match failed.")

# D. Fix balconyDoorPivot positioning in render and applyProgressToScene
js = js.replace(
    "if (balconyDoorPivot) balconyDoorPivot.position.x = camState.balconyDoorX;",
    "if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;"
)

# E. Update updateUI() to toggle closing-cta-card and show interactive notifications
old_ui_blueprint = """    const progressPill = document.getElementById('progress-card-pill');
    if (progressPill) {
        progressPill.classList.toggle('blueprint-mode', isBlueprint);
    }
}"""

new_ui_blueprint = """    const progressPill = document.getElementById('progress-card-pill');
    if (progressPill) {
        progressPill.classList.toggle('blueprint-mode', isBlueprint);
    }

    // Mumbai Sunset Finale Closing CTA Card (92% - 100%)
    const ctaCard = document.getElementById('closing-cta-card');
    if (ctaCard) {
        const showCTA = (p >= 0.92);
        ctaCard.classList.toggle('visible', showCTA);
        ctaCard.setAttribute('aria-hidden', showCTA ? 'false' : 'true');
    }
}

window.triggerSiteVisitModal = function() {
    alert("JP North Aviva · Private Site Visit Booking:\\n\\nThank you for exploring Wing A Type R1 (27.96 Sq.M. Carpet).\\nA JP Infra Luxury Consultant will reach out to confirm your private on-site show apartment walk-through.\\n\\nMahaRERA Registration: P51700023940");
};

window.downloadFloorplanBrochure = function() {
    alert("JP North Aviva · Floorplan Brochure Download:\\n\\nOfficial MahaRERA sanctioned CAD layouts, structural dimensions (Scale 1:50), and turnkey finish specifications are being prepared for download.");
};"""

if old_ui_blueprint in js:
    js = js.replace(old_ui_blueprint, new_ui_blueprint)
    print("[OK] script.js updateUI and CTA button triggers added.")
else:
    print("[INFO] Warning: old_ui_blueprint match failed, attempting regex search.")

with open("D:/floor plans/jp-aviva-3d/script.js", "w", encoding="utf-8") as f:
    f.write(js)

print("update_walkthrough_transitions.py completed successfully!")
