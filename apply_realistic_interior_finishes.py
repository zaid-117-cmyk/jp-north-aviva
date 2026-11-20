import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# -----------------------------------------------------------------------------
# 1. Update Textures & Materials (createInductionCooktopTexture, boucleTex, travertineTileTex, pbrArchitecturalGlass)
# -----------------------------------------------------------------------------
old_induction_start = "// G. Procedural Schott Ceran Induction Cooktop Texture"
old_blob_shadow = "// H. Contact Blob Shadow Generator"

idx_ind_start = code.find(old_induction_start)
idx_blob_start = code.find(old_blob_shadow)

if idx_ind_start == -1 or idx_blob_start == -1:
    raise ValueError(f"Could not find induction texture section: start={idx_ind_start}, end={idx_blob_start}")

new_texture_helpers = r'''// G. Procedural Schott Ceran Obsidian Induction Cooktop Texture (Subtle Faint Burner Rings)
function createInductionCooktopTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');

    // Deep obsidian ceramic glass
    ctx.fillStyle = '#121316';
    ctx.fillRect(0, 0, 512, 512);

    // Subtle brushed bevel perimeter border
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 2;
    ctx.strokeRect(4, 4, 504, 504);

    // Draw 4 circular burner rings with subtle warm amber / champagne rings
    function drawBurner(cx, cy, r) {
        // Outer thin ring
        ctx.strokeStyle = 'rgba(255, 230, 200, 0.42)';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();

        // Inner dashed guide ring
        ctx.strokeStyle = 'rgba(255, 215, 175, 0.22)';
        ctx.setLineDash([4, 6]);
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.arc(cx, cy, r * 0.55, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);

        // Minimalist center crosshair
        ctx.strokeStyle = 'rgba(255, 230, 200, 0.35)';
        ctx.lineWidth = 1.0;
        ctx.beginPath();
        ctx.moveTo(cx - 8, cy); ctx.lineTo(cx + 8, cy);
        ctx.moveTo(cx, cy - 8); ctx.lineTo(cx, cy + 8);
        ctx.stroke();
    }

    drawBurner(140, 140, 90);
    drawBurner(370, 140, 72);
    drawBurner(140, 360, 72);
    drawBurner(370, 360, 105);

    // Minimalist Miele-style touch slider & power controls
    ctx.fillStyle = 'rgba(235, 230, 220, 0.55)';
    ctx.font = '500 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('⏻   [ - - - - - + ]   BOOST   TIMER   [ 🔒 ]', 115, 485);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const inductionTex = createInductionCooktopTexture();

// G2. Woven Linen / Bouclé Fabric Bump & Roughness Texture
function createBoucleLinenTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#EBE5DC';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const pattern = ((x + y) % 8 === 0) ? 22 : -18;
            const noise = (Math.random() - 0.5) * 28;
            const val = Math.min(255, Math.max(0, 190 + pattern + noise));
            ctx.fillStyle = `rgb(${val},${val - 4},${val - 8})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    return tex;
}
const boucleTex = createBoucleLinenTexture();

// G3. Italian Porcelain / Travertine 600x1200mm Bathroom Tile Texture
function createTravertineTileTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 1024;
    const ctx = c.getContext('2d');

    // Warm porcelain / travertine cream background
    ctx.fillStyle = '#EDE7DE';
    ctx.fillRect(0, 0, 1024, 1024);

    // Subtle stone veining and mineral striations
    for (let i = 0; i < 40; i++) {
        ctx.strokeStyle = `rgba(185, 175, 160, ${0.08 + Math.random() * 0.10})`;
        ctx.lineWidth = 1 + Math.random() * 3.5;
        ctx.beginPath();
        let vy = Math.random() * 1024;
        ctx.moveTo(0, vy);
        for (let vx = 50; vx <= 1024; vx += 50) {
            vy += (Math.random() - 0.5) * 14;
            ctx.lineTo(vx, vy);
        }
        ctx.stroke();
    }

    // 600x1200mm tile grid with crisp 2mm grout lines
    ctx.strokeStyle = 'rgba(125, 115, 105, 0.45)';
    ctx.lineWidth = 2.5;

    // Horizontal grout lines
    for (let y = 0; y <= 1024; y += 256) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke();
    }
    // Vertical staggered grout lines
    for (let row = 0; row < 4; row++) {
        const yTop = row * 256;
        const offset = (row % 2) * 256;
        for (let x = offset; x <= 1024; x += 512) {
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yTop + 256); ctx.stroke();
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    return tex;
}
const travertineTileTex = createTravertineTileTexture();
'''

code = code[:idx_ind_start] + new_texture_helpers.strip() + "\n\n" + code[idx_blob_start:]

# -----------------------------------------------------------------------------
# 2. Add pbrBoucleLinen, pbrTravertineTile, pbrArchitecturalGlass, pbrCurtainLinen
# -----------------------------------------------------------------------------
pbr_insert_marker = "const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({"
idx_pbr = code.find(pbr_insert_marker)
if idx_pbr == -1:
    raise ValueError("Could not find pbrBrushedSteel")

new_pbr_mats = r'''const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.92,
    opacity: 1.0,
    transparent: true,
    roughness: 0.10, // Exact user specified 0.1
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.03,
    reflectivity: 0.90,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    clippingPlanes: [clipHeightPlane]
});

const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xE8E1D7,
    bumpMap: boucleTex,
    bumpScale: 0.007,
    roughness: 0.85,
    metalness: 0.0,
    sheen: 0.75,
    sheenRoughness: 0.55,
    sheenColor: new THREE.Color(0xF5EFEB),
    clippingPlanes: [clipHeightPlane]
});

const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
    color: 0xF3EFEA,
    map: travertineTileTex,
    roughness: 0.32,
    metalness: 0.02,
    clearcoat: 0.45,
    clearcoatRoughness: 0.18,
    clippingPlanes: [clipHeightPlane]
});

const pbrCurtainLinen = new THREE.MeshPhysicalMaterial({
    color: 0xF2EDE6,
    bumpMap: boucleTex,
    bumpScale: 0.005,
    roughness: 0.90,
    metalness: 0.0,
    sheen: 0.50,
    clippingPlanes: [clipHeightPlane]
});

const pbrSheerCurtain = new THREE.MeshPhysicalMaterial({
    color: 0xFFFAF5,
    transmission: 0.75,
    transparent: true,
    opacity: 0.70,
    roughness: 0.65,
    clippingPlanes: [clipHeightPlane]
});
'''

code = code[:idx_pbr] + new_pbr_mats.strip() + "\n\n" + code[idx_pbr:]

# -----------------------------------------------------------------------------
# 3. Replace buildHabitableRoom, buildKitchenAlcove, buildBathroomSuite, buildMasterBedroom, and buildSunsetBackdrop
# -----------------------------------------------------------------------------
sec_rooms_start = "// ============================================================================\n// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)"
sec_lighting_start = "// ----------------------------------------------------------------------------\n// 11. LIGHTING SETUP (GOLDEN HOUR SUNLIGHT & CONTACT SHADOW CONFIGURATION)"

idx_rooms_start = code.find(sec_rooms_start)
idx_lighting_start = code.find(sec_lighting_start)

if idx_rooms_start == -1 or idx_lighting_start == -1:
    raise ValueError(f"Could not find rooms start ({idx_rooms_start}) or lighting start ({idx_lighting_start})")

new_rooms_code = r'''// ============================================================================
// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)
// ============================================================================
function buildHabitableRoom() {
    const group = new THREE.Group();

    // 1. 65" Ultra-Thin 4K OLED Smart TV with Art Canvas & Ambilight Wall Glow
    const tvGroup = new THREE.Group();
    const tvFrame = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.84, 1.45), pbrMatteBlackSteel);
    tvFrame.position.set(0.22, 1.45, 0.60);
    tvFrame.castShadow = true;
    tvGroup.add(tvFrame);

    const tvScreenMat = new THREE.MeshBasicMaterial({
        map: tvArtTex,
        clippingPlanes: [clipHeightPlane]
    });
    const tvScreen = new THREE.Mesh(new THREE.PlaneGeometry(1.42, 0.81), tvScreenMat);
    tvScreen.rotateY(Math.PI / 2);
    tvScreen.position.set(0.23, 1.45, 0.60);
    tvGroup.add(tvScreen);

    const tvAmbiLight = new THREE.PointLight(0xFFB066, 1.2, 2.2, 2.0);
    tvAmbiLight.position.set(0.18, 1.45, 0.60);
    tvGroup.add(tvAmbiLight);

    const soundbar = new THREE.Mesh(new RoundedBoxGeometry(0.08, 0.06, 0.95, 4, 0.01), pbrMatteBlackSteel);
    soundbar.position.set(0.25, 0.98, 0.60);
    soundbar.castShadow = true;
    tvGroup.add(soundbar);

    const sbLed = new THREE.Mesh(new THREE.SphereGeometry(0.004, 8, 8), new THREE.MeshBasicMaterial({ color: 0x3399FF }));
    sbLed.position.set(0.295, 0.98, 0.60);
    tvGroup.add(sbLed);

    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.32, 2.10, 4, 0.02), pbrScandinavianOak);
    consoleBox.position.set(0.40, 0.46, 0.60);
    consoleBox.castShadow = true;
    tvGroup.add(consoleBox);
    createBlobShadow(0.48, 2.20, 0.40, 0.60, tvGroup, 0.42);
    group.add(tvGroup);

    // 2. Wall-Mounted Split Air Conditioner (Living Room)
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.30, 0.92, 4, 0.03), pbrCeilingMat);
    acBody.position.set(2.88, 2.45, 1.80);
    acBody.castShadow = true;
    acGroup.add(acBody);

    const acTrim = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.02, 0.92), pbrPolishedChrome);
    acTrim.position.set(2.75, 2.42, 1.80);
    acGroup.add(acTrim);

    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.01, 0.04, 0.10), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(2.75, 2.47, 2.05);
    acGroup.add(acLed);
    group.add(acGroup);

    // 3. Luxury Beveled Bouclé/Linen 3-Seater Sofa with Woven Bump & Soft Cushions
    const sofaGroup = new THREE.Group();
    // Low Scandinavian Oak plinth base
    const sPlinth = new THREE.Mesh(new RoundedBoxGeometry(0.86, 0.08, 2.26, 4, 0.02), pbrScandinavianOak);
    sPlinth.position.set(2.40, 0.04, 0.60);
    sPlinth.castShadow = true;
    sofaGroup.add(sPlinth);

    // Main sculpted seat platform in woven bouclé/linen
    const sBase = new THREE.Mesh(new RoundedBoxGeometry(0.92, 0.28, 2.30, 8, 0.06), pbrBoucleLinen);
    sBase.position.set(2.40, 0.20, 0.60);
    sBase.castShadow = true;
    sofaGroup.add(sBase);

    // Sculpted curved backrest
    const sBack = new THREE.Mesh(new RoundedBoxGeometry(0.28, 0.48, 2.30, 8, 0.06), pbrBoucleLinen);
    sBack.position.set(2.74, 0.54, 0.60);
    sBack.castShadow = true;
    sofaGroup.add(sBack);

    // Left and right sculpted bouclé armrests
    for (let az of [-1.08, 1.08]) {
        const arm = new THREE.Mesh(new RoundedBoxGeometry(0.88, 0.24, 0.18, 8, 0.05), pbrBoucleLinen);
        arm.position.set(2.38, 0.44, 0.60 + az);
        arm.castShadow = true;
        sofaGroup.add(arm);
    }

    // 3 Individual Deep Seat Cushions with Generous Bevels & Piping
    for (let i = 0; i < 3; i++) {
        const sc = new THREE.Mesh(new RoundedBoxGeometry(0.74, 0.15, 0.68, 8, 0.045), pbrBoucleLinen);
        sc.position.set(2.30, 0.41, 0.60 + (i - 1) * 0.72);
        sc.rotation.z = -0.02; // Subtle natural lean back
        sc.castShadow = true;
        sofaGroup.add(sc);
    }

    // 3 Soft Plush Back Cushions
    for (let i = 0; i < 3; i++) {
        const bc = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.40, 0.66, 8, 0.05), pbrBoucleLinen);
        bc.position.set(2.62, 0.64, 0.60 + (i - 1) * 0.72);
        bc.rotation.z = 0.18; // Leaning back naturally against the sofa back
        bc.castShadow = true;
        sofaGroup.add(bc);
    }

    // Layered Designer Accent Pillows (Woven Terracotta & Mustard Bouclé)
    const p1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.14, 6, 0.04), pbrTerracotta);
    p1.position.set(2.42, 0.60, 0.15);
    p1.rotation.y = 0.28;
    p1.rotation.z = 0.12;
    p1.castShadow = true;
    sofaGroup.add(p1);

    const p2 = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.36, 0.14, 6, 0.04), pbrMustard);
    p2.position.set(2.42, 0.60, 1.05);
    p2.rotation.y = -0.24;
    p2.rotation.z = 0.12;
    p2.castShadow = true;
    sofaGroup.add(p2);

    // Sculpted Knitted Throw Blanket with Folded Seams draped over armrest
    const throwBlanket = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.42, 0.48, 6, 0.04), pbrTerracotta);
    throwBlanket.position.set(2.38, 0.42, -0.42);
    throwBlanket.rotation.y = 0.08;
    throwBlanket.castShadow = true;
    sofaGroup.add(throwBlanket);

    createBlobShadow(1.10, 2.45, 2.45, 0.60, sofaGroup, 0.45);
    group.add(sofaGroup);

    // 4. Italian Calacatta Marble & Brushed Brass Coffee Table
    const tableGroup = new THREE.Group();
    const tTop = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.035, 0.58, 4, 0.015), pbrCalacattaFloor);
    tTop.position.set(1.50, 0.38, 0.60);
    tTop.castShadow = true;
    tableGroup.add(tTop);
    for (let lx of [-0.40, 0.40]) {
        for (let lz of [-0.24, 0.24]) {
            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.012, 0.36, 12), pbrBrushedBrass);
            leg.position.set(1.50 + lx, 0.18, 0.60 + lz);
            leg.castShadow = true;
            tableGroup.add(leg);
        }
    }
    const book = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.025, 0.18, 2, 0.005), pbrMatteBlackSteel);
    book.position.set(1.42, 0.41, 0.55);
    book.rotation.y = 0.15;
    tableGroup.add(book);

    const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.07, 16), pbrBrushedBrass);
    candle.position.set(1.62, 0.435, 0.65);
    tableGroup.add(candle);

    createBlobShadow(1.10, 0.75, 1.50, 0.60, tableGroup, 0.38);
    group.add(tableGroup);

    // 5. Dining Suite (Oak & Marble Table + Place Settings)
    const diningGroup = new THREE.Group();
    const dTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 1.05, 4, 0.015), pbrCalacattaFloor);
    dTop.position.set(1.40, 0.76, 2.05);
    dTop.castShadow = true;
    diningGroup.add(dTop);

    const dPedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 0.74, 24), pbrScandinavianOak);
    dPedestal.position.set(1.40, 0.37, 2.05);
    dPedestal.castShadow = true;
    diningGroup.add(dPedestal);

    for (let cz of [-0.55, 0.55]) {
        const chairGroup = new THREE.Group();
        chairGroup.position.set(1.40, 0, 2.05 + cz);

        for (let clx of [-0.18, 0.18]) {
            for (let clz of [-0.18, 0.18]) {
                const cLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.010, 0.45, 12), pbrScandinavianOak);
                cLeg.position.set(clx, 0.225, clz);
                cLeg.castShadow = true;
                chairGroup.add(cLeg);
            }
        }
        const cSeat = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.05, 0.42, 4, 0.02), pbrBoucleLinen);
        cSeat.position.set(0, 0.46, 0);
        cSeat.castShadow = true;
        chairGroup.add(cSeat);

        const cBack = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.32, 0.04, 4, 0.015), pbrScandinavianOak);
        cBack.position.set(0, 0.68, cz < 0 ? -0.19 : 0.19);
        cBack.castShadow = true;
        chairGroup.add(cBack);

        diningGroup.add(chairGroup);

        const plate = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
        plate.position.set(1.40, 0.785, 2.05 + cz * 0.45);
        diningGroup.add(plate);

        const wineGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.015, 0.12, 16), pbrArchitecturalGlass);
        wineGlass.position.set(1.58, 0.84, 2.05 + cz * 0.45);
        diningGroup.add(wineGlass);
    }

    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 0.18, 16), pbrWhisperingSmoke);
    vase.position.set(1.40, 0.87, 2.05);
    diningGroup.add(vase);

    createBlobShadow(1.20, 1.40, 1.40, 2.05, diningGroup, 0.42);
    group.add(diningGroup);

    // 6. PROPER ARCHITECTURAL FRENCH WINDOW SYSTEM WITH MULLIONS & ARCHITECTURAL GLASS
    const windowGroup = new THREE.Group();
    windowGroup.position.set(1.575, 1.10, -1.15);

    // Outer architectural frame casing (Matte Black / Dark Bronze)
    const outerFrameTop = new THREE.Mesh(new THREE.BoxGeometry(2.44, 0.06, 0.08), pbrMatteBlackSteel);
    outerFrameTop.position.set(0, 1.07, 0);
    windowGroup.add(outerFrameTop);

    const outerFrameBottom = new THREE.Mesh(new THREE.BoxGeometry(2.44, 0.08, 0.12), pbrMatteBlackSteel);
    outerFrameBottom.position.set(0, -1.06, 0);
    windowGroup.add(outerFrameBottom);

    const outerFrameLeft = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.20, 0.08), pbrMatteBlackSteel);
    outerFrameLeft.position.set(-1.19, 0, 0);
    windowGroup.add(outerFrameLeft);

    const outerFrameRight = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.20, 0.08), pbrMatteBlackSteel);
    outerFrameRight.position.set(1.19, 0, 0);
    windowGroup.add(outerFrameRight);

    // Center dividing vertical mullion post
    const centerMullion = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.14, 0.08), pbrMatteBlackSteel);
    centerMullion.position.set(0, 0, 0);
    windowGroup.add(centerMullion);

    // Left and right horizontal intermediate mullion bars
    for (let px of [-0.60, 0.60]) {
        const horizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.05), pbrMatteBlackSteel);
        horizMullion.position.set(px, 0.15, 0);
        windowGroup.add(horizMullion);
    }

    // 4 Reflective Architectural Glass Panes (MeshPhysicalMaterial, transmission: 0.92, roughness: 0.10)
    for (let px of [-0.60, 0.60]) {
        // Upper glass pane
        const upperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
        upperGlass.position.set(px, 0.61, 0);
        windowGroup.add(upperGlass);

        // Lower glass pane
        const lowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
        lowerGlass.position.set(px, -0.45, 0);
        windowGroup.add(lowerGlass);
    }

    // Brushed steel vertical handles on sliding panes
    const handleLeft = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleLeft.position.set(-0.06, 0.0, 0.04);
    windowGroup.add(handleLeft);

    const handleRight = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleRight.position.set(0.06, 0.0, -0.04);
    windowGroup.add(handleRight);

    group.add(windowGroup);

    materialGroup.add(group);
}

// ============================================================================
// B. GOURMET KITCHEN ALCOVE (FULL APPLIANCE SUITE & REALISTIC FINISHES)
// ============================================================================
function buildKitchenAlcove() {
    const group = new THREE.Group();

    // 1. L-Shaped Jet Black Quartz Countertop with Authentic Chamfer/Bullnose Edge Profile
    const nCounter = new THREE.Mesh(new RoundedBoxGeometry(1.85, 0.045, 0.64, 6, 0.012), pbrBlackQuartz);
    nCounter.position.set(-0.80, 0.865, -2.05);
    nCounter.castShadow = true;
    group.add(nCounter);

    // Front edge profile strip catching specular light highlights
    const counterEdge = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.015, 0.015), pbrBlackQuartz);
    counterEdge.position.set(-0.80, 0.84, -1.725);
    group.add(counterEdge);

    // Base Cabinet Box
    const nBaseCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.84, 0.58), pbrScandinavianOak);
    nBaseCab.position.set(-0.80, 0.42, -2.05);
    nBaseCab.castShadow = true;
    group.add(nBaseCab);

    // 4 Cabinet / Drawer Front Panels with Architectural Reveals & Brushed Steel Bar Handles
    const cabWidths = [-1.45, -1.05, -0.55, -0.15];
    for (let cx of cabWidths) {
        // Cabinet door panel
        const doorPanel = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.78, 0.02, 4, 0.008), pbrScandinavianOak);
        doorPanel.position.set(cx, 0.43, -1.745);
        doorPanel.castShadow = true;
        group.add(doorPanel);

        // Modern horizontal brushed steel bar handle (180mm) with standoffs
        const handleBar = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.012, 0.014, 2, 0.003), pbrBrushedSteel);
        handleBar.position.set(cx, 0.74, -1.72);
        group.add(handleBar);
        // Left & right standoffs
        for (let so of [-0.07, 0.07]) {
            const standoff = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.018, 12), pbrBrushedSteel);
            standoff.rotation.x = Math.PI / 2;
            standoff.position.set(cx + so, 0.74, -1.735);
            group.add(standoff);
        }
    }

    // 2. Glazed Subway Tile Backsplash with Realistic Grout Lines
    const splashGeo = new THREE.PlaneGeometry(1.85, 0.70);
    const splashMat = new THREE.MeshPhysicalMaterial({
        map: subwayTileTex,
        roughness: 0.15,
        clearcoat: 0.95,
        clearcoatRoughness: 0.08,
        clippingPlanes: [clipHeightPlane]
    });
    const splashMesh = new THREE.Mesh(splashGeo, splashMat);
    splashMesh.position.set(-0.80, 1.25, -2.34);
    group.add(splashMesh);

    // 3. Overhead Scandinavian Oak Cabinets with Brushed Steel Handles
    const upperCab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.75, 0.35), pbrScandinavianOak);
    upperCab.position.set(-0.80, 2.00, -2.20);
    upperCab.castShadow = true;
    group.add(upperCab);

    // 3 Upper Cabinet Door Panels with Vertical Brushed Steel Handles
    const uWidths = [-1.35, -0.80, -0.25];
    for (let ux of uWidths) {
        const uDoor = new THREE.Mesh(new RoundedBoxGeometry(0.52, 0.72, 0.02, 4, 0.008), pbrScandinavianOak);
        uDoor.position.set(ux, 2.00, -2.015);
        uDoor.castShadow = true;
        group.add(uDoor);

        // Vertical brushed steel handle near bottom edge of cabinet
        const uHandle = new THREE.Mesh(new RoundedBoxGeometry(0.012, 0.18, 0.014, 2, 0.003), pbrBrushedSteel);
        uHandle.position.set(ux + 0.20, 1.76, -1.995);
        group.add(uHandle);
    }

    // Recessed Under-Cabinet LED Aluminum Extrusion & Diffuser Strip
    const ledProfile = new THREE.Mesh(new THREE.BoxGeometry(1.80, 0.015, 0.03), pbrBrushedSteel);
    ledProfile.position.set(-0.80, 1.62, -2.18);
    group.add(ledProfile);

    const ledDiffuser = new THREE.Mesh(new THREE.BoxGeometry(1.78, 0.008, 0.02), new THREE.MeshBasicMaterial({
        color: 0xFFF5E0,
        clippingPlanes: [clipHeightPlane]
    }));
    ledDiffuser.position.set(-0.80, 1.61, -2.18);
    group.add(ledDiffuser);

    // 3 Soft Warm Downward Task Lights washing prep counters without harshness
    for (let lx of [-1.35, -0.80, -0.25]) {
        const taskSpot = new THREE.PointLight(0xFFEED6, 0.75, 2.4, 2.0);
        taskSpot.position.set(lx, 1.58, -2.12);
        group.add(taskSpot);
    }

    // 4. Undermount Double Basin Stainless Steel Sink & REALISTIC GOOSENECK FAUCET (TubeGeometry)
    const sinkGeo = new THREE.BoxGeometry(0.52, 0.20, 0.38);
    const sinkMesh = new THREE.Mesh(sinkGeo, pbrBrushedSteel);
    sinkMesh.position.set(-1.25, 0.78, -2.05);
    group.add(sinkMesh);

    // Realistic Gooseneck Faucet using TubeGeometry
    const faucetGroup = new THREE.Group();
    faucetGroup.position.set(-1.25, 0.89, -2.25);

    // Escutcheon base ring
    const escutcheon = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.030, 0.018, 24), pbrBrushedSteel);
    escutcheon.position.set(0, 0.009, 0);
    faucetGroup.add(escutcheon);

    // Elegant Gooseneck Arch Curve
    const faucetCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0.01, 0),
        new THREE.Vector3(0, 0.22, 0),
        new THREE.Vector3(0, 0.34, 0.03),
        new THREE.Vector3(0, 0.38, 0.10),
        new THREE.Vector3(0, 0.32, 0.16),
        new THREE.Vector3(0, 0.24, 0.16)
    ]);
    const faucetGeo = new THREE.TubeGeometry(faucetCurve, 32, 0.011, 16, false);
    const faucetMesh = new THREE.Mesh(faucetGeo, pbrBrushedSteel);
    faucetMesh.castShadow = true;
    faucetGroup.add(faucetMesh);

    // Precision aerator spray nozzle tip
    const nozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.012, 0.03, 16), pbrBrushedSteel);
    nozzle.position.set(0, 0.225, 0.16);
    faucetGroup.add(nozzle);

    // Single-lever mixer handle on side
    const mixerBody = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.03, 12), pbrBrushedSteel);
    mixerBody.rotation.z = Math.PI / 2;
    mixerBody.position.set(0.025, 0.08, 0);
    faucetGroup.add(mixerBody);
    const mixerLever = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.07, 12), pbrBrushedSteel);
    mixerLever.position.set(0.04, 0.11, 0);
    mixerLever.rotation.z = -0.35;
    faucetGroup.add(mixerLever);

    group.add(faucetGroup);

    // 5. Schott Ceran Obsidian Ceramic Induction Hob with Subtle Warm Burner Rings (No Harsh Red)
    const cooktop = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.012, 0.44), new THREE.MeshPhysicalMaterial({
        map: inductionTex,
        roughness: 0.04,
        clearcoat: 1.0,
        clearcoatRoughness: 0.04,
        clippingPlanes: [clipHeightPlane]
    }));
    cooktop.position.set(-0.45, 0.89, -2.05);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle warm amber status indicator (gentle, not harsh glare)
    const cooktopStatus = new THREE.Mesh(new THREE.SphereGeometry(0.004, 8, 8), new THREE.MeshBasicMaterial({ color: 0xFFE0B2 }));
    cooktopStatus.position.set(-0.45, 0.90, -1.86);
    group.add(cooktopStatus);

    // 6. Stainless Steel Chimney Exhaust Hood
    const hoodGroup = new THREE.Group();
    const hoodCanopy = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.08, 0.48), pbrBrushedSteel);
    hoodCanopy.position.set(-0.45, 1.65, -2.10);
    hoodCanopy.castShadow = true;
    hoodGroup.add(hoodCanopy);

    const hoodDuct = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.65, 0.28), pbrBrushedSteel);
    hoodDuct.position.set(-0.45, 2.02, -2.18);
    hoodDuct.castShadow = true;
    hoodGroup.add(hoodDuct);

    const hoodLight = new THREE.PointLight(0xFFE8D0, 1.1, 1.8, 2.0);
    hoodLight.position.set(-0.45, 1.60, -2.10);
    hoodGroup.add(hoodLight);
    group.add(hoodGroup);

    // 7. Built-in Convection Microwave Oven Stack
    const ovenGroup = new THREE.Group();
    const ovenBox = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.36, 0.38), pbrMatteBlackSteel);
    ovenBox.position.set(-0.80, 1.85, -2.20);
    ovenGroup.add(ovenBox);
    const ovenDoor = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.32), new THREE.MeshPhysicalMaterial({
        color: 0x111111,
        clearcoat: 1.0,
        roughness: 0.05,
        clippingPlanes: [clipHeightPlane]
    }));
    ovenDoor.position.set(-0.80, 1.85, -2.00);
    ovenGroup.add(ovenDoor);
    const clockLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.025, 0.005), new THREE.MeshBasicMaterial({ color: 0x00FF66 }));
    clockLed.position.set(-0.64, 1.95, -1.995);
    ovenGroup.add(clockLed);
    const ovenHandle = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.015, 0.02), pbrBrushedSteel);
    ovenHandle.position.set(-0.80, 1.74, -1.98);
    ovenGroup.add(ovenHandle);
    group.add(ovenGroup);

    // 8. French Door Smart Refrigerator
    const fridgeGroup = new THREE.Group();
    const fridgeBody = new THREE.Mesh(new RoundedBoxGeometry(0.85, 1.90, 0.72, 4, 0.02), pbrBrushedSteel);
    fridgeBody.position.set(0.48, 0.95, -2.05);
    fridgeBody.castShadow = true;
    fridgeGroup.add(fridgeBody);
    const leftDoor = new THREE.Mesh(new RoundedBoxGeometry(0.41, 1.15, 0.03, 4, 0.01), pbrBrushedSteel);
    leftDoor.position.set(0.27, 1.30, -1.68);
    fridgeGroup.add(leftDoor);
    const rightDoor = new THREE.Mesh(new RoundedBoxGeometry(0.41, 1.15, 0.03, 4, 0.01), pbrBrushedSteel);
    rightDoor.position.set(0.69, 1.30, -1.68);
    fridgeGroup.add(rightDoor);
    const freezerDrawer = new THREE.Mesh(new RoundedBoxGeometry(0.83, 0.65, 0.03, 4, 0.01), pbrBrushedSteel);
    freezerDrawer.position.set(0.48, 0.35, -1.68);
    fridgeGroup.add(freezerDrawer);
    const dispenser = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 0.28), new THREE.MeshBasicMaterial({ color: 0x1A1C1E }));
    dispenser.position.set(0.27, 1.35, -1.66);
    fridgeGroup.add(dispenser);
    for (let hx of [0.46, 0.50]) {
        const fHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.95, 12), pbrBrushedSteel);
        fHandle.position.set(hx, 1.30, -1.65);
        fridgeGroup.add(fHandle);
    }
    const bzHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.65, 12), pbrBrushedSteel);
    bzHandle.rotation.z = Math.PI / 2;
    bzHandle.position.set(0.48, 0.58, -1.65);
    fridgeGroup.add(bzHandle);
    createBlobShadow(0.95, 0.85, 0.48, -2.05, fridgeGroup, 0.45);
    group.add(fridgeGroup);

    // 9. Italian Espresso Machine & Toaster
    const espressoBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.28, 0.28, 4, 0.015), pbrBrushedSteel);
    espressoBody.position.set(-1.60, 1.02, -2.05);
    group.add(espressoBody);
    const portafilter = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.14, 12), pbrMatteBlackSteel);
    portafilter.rotation.x = Math.PI / 2;
    portafilter.position.set(-1.60, 0.96, -1.86);
    group.add(portafilter);

    const toaster = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.16, 0.14, 4, 0.02), pbrBrushedSteel);
    toaster.position.set(-0.05, 0.96, -2.05);
    group.add(toaster);

    createBlobShadow(1.95, 0.75, -0.80, -2.05, group, 0.40);
    materialGroup.add(group);
}

// ============================================================================
// C. DESIGNER BATH SUITE (PORCELAIN TILES, SOFT HALO MIRROR & SHOWER GLASS)
// ============================================================================
function buildBathroomSuite() {
    const group = new THREE.Group();

    // 1. Dark Slate Porcelain Flooring
    const bathFloorGeo = new THREE.PlaneGeometry(1.90, 1.28);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrSlateTile);
    bathFloor.position.set(-0.775, 0.002, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // 2. Travertine / Porcelain Tiled Wall Panels (600x1200mm Tile Grid)
    // Full-height wet wall behind vanity & mirror (z = 1.62)
    const wetWallGeo = new THREE.PlaneGeometry(1.80, WALL_H);
    const wetWallMesh = new THREE.Mesh(wetWallGeo, pbrTravertineTile);
    wetWallMesh.position.set(-0.85, WALL_H / 2, 1.615);
    wetWallMesh.receiveShadow = true;
    group.add(wetWallMesh);

    // Shower wet wall panel (x = -1.825)
    const showerWallGeo = new THREE.PlaneGeometry(1.25, WALL_H);
    showerWallGeo.rotateY(Math.PI / 2);
    const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);
    showerWallMesh.position.set(-1.82, WALL_H / 2, 0.98);
    showerWallMesh.receiveShadow = true;
    group.add(showerWallMesh);

    // 3. Floating Scandinavian Oak Vanity Unit (in Bath: X = -1.15)
    const vanity = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.36, 0.44, 4, 0.02), pbrScandinavianOak);
    vanity.position.set(-1.15, 0.55, 1.35);
    vanity.castShadow = true;
    group.add(vanity);

    // Brushed steel handle on vanity drawer
    const vHandle = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.012, 0.014, 2, 0.003), pbrBrushedSteel);
    vHandle.position.set(-1.15, 0.58, 1.12);
    group.add(vHandle);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.12, 24), pbrWhisperingSmoke);
    basin.position.set(-1.15, 0.79, 1.35);
    basin.castShadow = true;
    group.add(basin);

    // Tall Matte Black Basin Faucet
    const bFaucet = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.24, 16), pbrMatteBlackSteel);
    bFaucet.position.set(-1.15, 0.88, 1.50);
    group.add(bFaucet);

    // 4. Circular Backlit Mirror with Soft Wall-Mounted Warm LED Halo (No Harsh Glare)
    const mirrorGroup = new THREE.Group();
    // Ultra-flat mirror glass disc with beveled edge
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.012, 48), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.02,
        metalness: 0.98,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.15, 1.45, 1.57);
    mirrorGroup.add(mirrorGlass);

    // 360° Recessed Wall-Mounted LED Strip Ribbon behind mirror
    const haloRingGeo = new THREE.TorusGeometry(0.405, 0.012, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(-1.15, 1.45, 1.58);
    mirrorGroup.add(haloRingMesh);

    // Diffused soft wall-wash light creating gentle halo wash onto travertine tiles
    const haloWallLight = new THREE.PointLight(0xFFE4B5, 0.65, 2.0, 2.0);
    haloWallLight.position.set(-1.15, 1.45, 1.58);
    mirrorGroup.add(haloWallLight);
    group.add(mirrorGroup);

    // 5. Wall-Hung Ceramic Toilet with Concealed Cistern & Chrome Dual-Flush Plate
    const toiletGroup = new THREE.Group();
    const toiletBowl = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.36, 0.52, 4, 0.04), pbrWhisperingSmoke);
    toiletBowl.position.set(-0.25, 0.40, 1.30);
    toiletBowl.castShadow = true;
    toiletGroup.add(toiletBowl);

    const toiletLid = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.025, 0.50, 4, 0.02), pbrWhisperingSmoke);
    toiletLid.position.set(-0.25, 0.59, 1.30);
    toiletGroup.add(toiletLid);

    const flushPlate = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.14, 0.015, 2, 0.005), pbrPolishedChrome);
    flushPlate.position.set(-0.25, 1.10, 1.61);
    toiletGroup.add(flushPlate);

    createBlobShadow(0.48, 0.65, -0.25, 1.30, toiletGroup, 0.35);
    group.add(toiletGroup);

    // 6. Walk-in Tempered Glass Shower Partition with Black Hardware
    const showerGroup = new THREE.Group();
    // 10mm Architectural Glass Screen (pbrArchitecturalGlass)
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.012, 2.15, 0.95), pbrArchitecturalGlass);
    showerGlass.position.set(-0.75, 1.08, 0.85);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Floor and wall U-channel tracks in matte black steel
    const glassChannel = new THREE.Mesh(new THREE.BoxGeometry(0.025, 2.15, 0.025), pbrMatteBlackSteel);
    glassChannel.position.set(-0.75, 1.08, 1.32);
    showerGroup.add(glassChannel);

    const floorChannel = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.025, 0.95), pbrMatteBlackSteel);
    floorChannel.position.set(-0.75, 0.012, 0.85);
    showerGroup.add(floorChannel);

    // Top horizontal stabilizing support bar anchored to wall
    const supportBar = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 1.05, 12), pbrMatteBlackSteel);
    supportBar.rotation.z = Math.PI / 2;
    supportBar.position.set(-1.25, 2.10, 0.85);
    showerGroup.add(supportBar);

    // 250mm square rain shower head
    const rainShower = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.015, 0.25), pbrMatteBlackSteel);
    rainShower.position.set(-1.40, 2.45, 0.70);
    showerGroup.add(rainShower);
    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.40, 12), pbrMatteBlackSteel);
    showerArm.position.set(-1.40, 2.65, 0.70);
    showerGroup.add(showerArm);

    // Heated towel rail with folded plush white bath towel
    const towelRail = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.55, 12), pbrPolishedChrome);
    towelRail.rotation.z = Math.PI / 2;
    towelRail.position.set(-1.15, 1.10, 0.38);
    showerGroup.add(towelRail);
    const towel = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.35, 0.05, 4, 0.02), pbrWhisperingSmoke);
    towel.position.set(-1.15, 0.95, 0.40);
    showerGroup.add(towel);

    group.add(showerGroup);

    createBlobShadow(0.85, 0.55, -1.15, 1.35, group, 0.40);
    materialGroup.add(group);
}

// ============================================================================
// D. MASTER BEDROOM SUITE (RECESSED WARDROBE, DRAPED CURTAINS & SOFT BEDDING)
// ============================================================================
function buildMasterBedroom() {
    const group = new THREE.Group();

    // 1. Floating Luxury Platform Bed with Softer Layered Bedding Folds
    const bedGroup = new THREE.Group();
    // Recessed plinth base
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.14, 1.90), pbrMatteBlackSteel);
    plinth.position.set(-2.95, 0.07, -0.95);
    bedGroup.add(plinth);

    // Floating Oak Bed Frame with rounded corners
    const bedFrame = new THREE.Mesh(new RoundedBoxGeometry(1.88, 0.18, 2.12, 6, 0.03), pbrScandinavianOak);
    bedFrame.position.set(-2.95, 0.23, -0.95);
    bedFrame.castShadow = true;
    bedGroup.add(bedFrame);

    // Under-bed warm floating LED strip glow
    const underBedLight = new THREE.PointLight(0xFFE0B2, 1.2, 2.5, 2.0);
    underBedLight.position.set(-2.95, 0.12, -0.95);
    bedGroup.add(underBedLight);

    // Deep plush mattress with pillowy top contour
    const mattress = new THREE.Mesh(new RoundedBoxGeometry(1.72, 0.28, 1.96, 6, 0.04), pbrWhisperingSmoke);
    mattress.position.set(-2.95, 0.46, -0.95);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    // Softer Layered Duvet with turned-down top fold
    const duvetMain = new THREE.Mesh(new RoundedBoxGeometry(1.76, 0.14, 1.55, 8, 0.05), pbrBoucleLinen);
    duvetMain.position.set(-2.95, 0.58, -1.15);
    duvetMain.castShadow = true;
    bedGroup.add(duvetMain);

    // Turned-down upper duvet fold showing inner soft white cotton sheet
    const duvetFold = new THREE.Mesh(new RoundedBoxGeometry(1.74, 0.08, 0.32, 6, 0.035), pbrWhisperingSmoke);
    duvetFold.position.set(-2.95, 0.62, -0.32);
    duvetFold.castShadow = true;
    bedGroup.add(duvetFold);

    // Draped Waffle Throw Blanket across foot of bed with soft undulating folds
    const bedThrow = new THREE.Mesh(new RoundedBoxGeometry(1.78, 0.09, 0.48, 6, 0.035), pbrTerracotta);
    bedThrow.position.set(-2.95, 0.63, -1.72);
    bedThrow.rotation.z = 0.02;
    bedThrow.castShadow = true;
    bedGroup.add(bedThrow);

    // Padded "Wild Mushroom" Upholstered Headboard
    const headboard = new THREE.Mesh(new RoundedBoxGeometry(2.35, 1.15, 0.10, 6, 0.03), pbrWildMushroom);
    headboard.position.set(-2.95, 0.85, 0.18);
    headboard.castShadow = true;
    bedGroup.add(headboard);

    // 4 Soft Plush Pillows with indentation creases (2 sleeping pillows + 2 mustard accent cushions)
    for (let px of [-0.48, 0.48]) {
        // Sculpted sleeping pillow with natural backward lean
        const sleepPillow = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.15, 0.38, 6, 0.04), pbrBoucleLinen);
        sleepPillow.position.set(-2.95 + px, 0.65, -0.15);
        sleepPillow.rotation.x = 0.22;
        sleepPillow.castShadow = true;
        bedGroup.add(sleepPillow);

        // Accent bouclé cushion
        const accentCushion = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.13, 0.32, 6, 0.035), pbrMustard);
        accentCushion.position.set(-2.95 + px, 0.69, -0.32);
        accentCushion.rotation.x = 0.36;
        accentCushion.castShadow = true;
        bedGroup.add(accentCushion);
    }

    createBlobShadow(2.15, 2.35, -2.95, -0.95, bedGroup, 0.46);
    group.add(bedGroup);

    // 2. Twin Floating Nightstands & Suspended Brass Pendants
    for (let nx of [-4.00, -1.90]) {
        const nsGroup = new THREE.Group();
        const ns = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.22, 0.34, 4, 0.015), pbrScandinavianOak);
        ns.position.set(nx, 0.45, 0.05);
        ns.castShadow = true;
        nsGroup.add(ns);

        const pendantRod = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 1.60, 8), pbrBrushedBrass);
        pendantRod.position.set(nx, WALL_H - 0.80, 0.05);
        nsGroup.add(pendantRod);

        const pendantCone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.14, 16), pbrBrushedBrass);
        pendantCone.position.set(nx, WALL_H - 1.65, 0.05);
        nsGroup.add(pendantCone);

        const pendantLight = new THREE.PointLight(0xFFD8A8, 1.8, 3.0, 2.0);
        pendantLight.position.set(nx, WALL_H - 1.72, 0.05);
        nsGroup.add(pendantLight);

        if (nx < -3.0) {
            const novel = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.02, 0.14, 2, 0.005), pbrTerracotta);
            novel.position.set(nx, 0.57, 0.05);
            nsGroup.add(novel);
        } else {
            const carafe = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.045, 0.14, 16), pbrGlass);
            carafe.position.set(nx, 0.63, 0.05);
            nsGroup.add(carafe);
        }

        createBlobShadow(0.48, 0.44, nx, 0.05, nsGroup, 0.35);
        group.add(nsGroup);
    }

    // 3. Wall-Mounted Split Air Conditioner (Bedroom)
    const acGroup = new THREE.Group();
    const acBody = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.28, 0.88, 4, 0.03), pbrCeilingMat);
    acBody.position.set(-2.95, 2.50, -2.36);
    acBody.castShadow = true;
    acGroup.add(acBody);

    const acLed = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.035, 0.01), new THREE.MeshBasicMaterial({ color: 0x00E5FF }));
    acLed.position.set(-2.70, 2.50, -2.23);
    acGroup.add(acLed);
    group.add(acGroup);

    // 4. BUILT-IN FLOOR-TO-CEILING WARDROBE WITH RECESSED DOORS & INTEGRATED HANDLES
    const wardrobeGroup = new THREE.Group();
    wardrobeGroup.position.set(-3.95, WALL_H / 2, -1.50);

    // Main wardrobe outer carcass casing
    const wardrobeCarcass = new THREE.Mesh(new THREE.BoxGeometry(0.60, WALL_H - 0.04, 1.68), pbrScandinavianOak);
    wardrobeCarcass.castShadow = true;
    wardrobeGroup.add(wardrobeCarcass);

    // 3 Recessed Wardrobe Doors with Architectural Shadow Gaps
    const doorOffsetsZ = [-0.52, 0.0, 0.52];
    for (let dz of doorOffsetsZ) {
        // Recessed door panel
        const doorLeaf = new THREE.Mesh(new RoundedBoxGeometry(0.025, WALL_H - 0.12, 0.50, 4, 0.008), pbrScandinavianOak);
        doorLeaf.position.set(0.295, 0, dz);
        doorLeaf.castShadow = true;
        wardrobeGroup.add(doorLeaf);

        // Full-height vertical brushed brass / metal J-pull handle
        const handle = new THREE.Mesh(new RoundedBoxGeometry(0.018, 1.80, 0.018, 2, 0.003), pbrBrushedBrass);
        handle.position.set(0.31, 0, dz + 0.22);
        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);

    // 5. DRAPED LINEN & SHEER CURTAINS OVER THE WINDOW
    const curtainGroup = new THREE.Group();
    curtainGroup.position.set(-3.05, 0, -2.36);

    // Ceiling-recessed curtain rod
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 2.30, 16), pbrMatteBlackSteel);
    rod.rotation.z = Math.PI / 2;
    rod.position.set(0, WALL_H - 0.04, 0);
    curtainGroup.add(rod);

    // Center Translucent Sheer Curtain Panel (filtering golden morning sunlight)
    const sheer = new THREE.Mesh(new THREE.PlaneGeometry(1.60, WALL_H - 0.08), pbrSheerCurtain);
    sheer.position.set(0, (WALL_H - 0.08) / 2, 0.02);
    curtainGroup.add(sheer);

    // Left and Right Draped Linen Curtains with Soft Vertical Folds
    for (let side of [-1, 1]) {
        const sideGroup = new THREE.Group();
        sideGroup.position.set(side * 0.95, 0, 0.04);

        // 3 undulating vertical fold ripples on each side
        for (let r = 0; r < 3; r++) {
            const ripple = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.055, WALL_H - 0.08, 16), pbrCurtainLinen);
            ripple.position.set((r - 1) * 0.07, (WALL_H - 0.08) / 2, 0);
            ripple.castShadow = true;
            sideGroup.add(ripple);
        }
        curtainGroup.add(sideGroup);
    }
    group.add(curtainGroup);

    materialGroup.add(group);
}

// ============================================================================
// E. SUNSET SKYLINE BACKDROP (REALISTIC GOLDEN MUMBAI HORIZON)
// ============================================================================
function buildSunsetBackdrop() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Subtle golden hour dusk sky with realistic atmospheric haze (not flat orange)
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0, '#3A4860');    // Upper dusk blue-slate
    grad.addColorStop(0.35, '#8C7A78'); // Muted mauve twilight transition
    grad.addColorStop(0.60, '#C2987E'); // Soft golden peach
    grad.addColorStop(0.78, '#E6B88A'); // Warm golden hour horizon band
    grad.addColorStop(0.92, '#F5D8B0'); // Low horizon atmospheric haze
    grad.addColorStop(1.0, '#D8BC9E');  // Horizon ground mist
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 512);

    // Soft warm sun glow on horizon
    const sun = ctx.createRadialGradient(512, 380, 20, 512, 380, 280);
    sun.addColorStop(0, 'rgba(255, 250, 235, 0.85)');
    sun.addColorStop(0.3, 'rgba(255, 220, 160, 0.40)');
    sun.addColorStop(0.7, 'rgba(230, 170, 110, 0.15)');
    sun.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = sun;
    ctx.fillRect(0, 0, 1024, 512);

    // Distant city skyline silhouette in soft muted purple-slate
    ctx.fillStyle = 'rgba(65, 55, 68, 0.65)';
    ctx.beginPath();
    ctx.moveTo(0, 430);
    for (let x = 0; x < 1024; x += 28) {
        const bh = 30 + Math.sin(x * 0.04) * 20 + Math.cos(x * 0.10) * 15;
        ctx.lineTo(x, 512 - bh);
        ctx.lineTo(x + 24, 512 - bh);
    }
    ctx.lineTo(1024, 512);
    ctx.lineTo(0, 512);
    ctx.closePath();
    ctx.fill();

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    const geo = new THREE.PlaneGeometry(32, 14);
    const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(0.5, 4.0, -11.5);
    scene.add(mesh);
    return mesh;
}
const skyBillboard = buildSunsetBackdrop();

// Build All Realism Rooms
buildHabitableRoom();
buildKitchenAlcove();
buildBathroomSuite();
buildMasterBedroom();
buildBalcony();
'''

code = code[:idx_rooms_start] + new_rooms_code.strip() + "\n\n" + code[idx_lighting_start:]

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied realistic interior finishes across Living, Kitchen, Bath, and Bedroom successfully!")
