import os
import re

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. ADD PROCEDURAL TEXTURES (Jute Rug, Fluted Wood, Gallery Art Prints 1 & 2)
# -----------------------------------------------------------------------------
tv_art_marker = "const tvArtTex = createArtTVTexture();\n"
assert tv_art_marker in c, "tv_art_marker not found"

new_textures = """
// F1. Procedural Textured Woven Jute/Wool Area Rug Texture
function createJuteRugTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Natural warm oatmeal/sand jute base
    ctx.fillStyle = '#CFC5B4';
    ctx.fillRect(0, 0, 512, 512);

    // Alternating horizontal and vertical woven yarn loops
    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const isWarp = ((Math.floor(x / 8) + Math.floor(y / 4)) % 2 === 0);
            const fiberNoise = (Math.random() - 0.5) * 22;
            const tone = isWarp ? 218 + fiberNoise : 188 + fiberNoise;
            const r = Math.min(255, Math.max(0, Math.round(tone * 1.02)));
            const g = Math.min(255, Math.max(0, Math.round(tone * 0.96)));
            const b = Math.min(255, Math.max(0, Math.round(tone * 0.88)));
            ctx.fillStyle = `rgb(${r},${g},${b})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }

    // Braided perimeter border lines
    ctx.strokeStyle = 'rgba(140, 125, 105, 0.45)';
    ctx.lineWidth = 6;
    ctx.strokeRect(10, 10, 492, 492);
    ctx.strokeStyle = 'rgba(235, 225, 210, 0.55)';
    ctx.lineWidth = 3;
    ctx.strokeRect(16, 16, 480, 480);

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(3, 4);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const juteRugTex = createJuteRugTexture();

// F2. Procedural Fluted Wood Slat Bump Texture
function createFlutedWoodBumpTexture() {
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 256;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, 256, 256);

    // Slat pitch: 16px wide slat + 4px shadow groove
    const pitch = 20;
    const slatW = 16;
    for (let x = 0; x < 256; x += pitch) {
        // Cylindrical convex bevel gradient across the slat
        const grad = ctx.createLinearGradient(x, 0, x + slatW, 0);
        grad.addColorStop(0.0, 'rgb(110, 110, 110)');
        grad.addColorStop(0.2, 'rgb(175, 175, 175)');
        grad.addColorStop(0.5, 'rgb(240, 240, 240)');
        grad.addColorStop(0.8, 'rgb(175, 175, 175)');
        grad.addColorStop(1.0, 'rgb(110, 110, 110)');
        ctx.fillStyle = grad;
        ctx.fillRect(x, 0, slatW, 256);

        // Deep recessed shadow gap groove
        ctx.fillStyle = 'rgb(40, 40, 40)';
        ctx.fillRect(x + slatW, 0, pitch - slatW, 256);
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(12, 1);
    return tex;
}
const flutedWoodBumpTex = createFlutedWoodBumpTexture();

// F3. Procedural Gallery Art Print 1: Minimalist Modernist Architecture Lithograph
function createArchArtPrint1Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Museum archival off-white textured paper
    ctx.fillStyle = '#F6F3EB';
    ctx.fillRect(0, 0, 512, 768);

    // Paper fiber texture
    for (let i = 0; i < 4000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        const alpha = Math.random() * 0.04;
        ctx.fillStyle = `rgba(120, 100, 80, ${alpha})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Outer passe-partout museum mat border
    ctx.strokeStyle = 'rgba(215, 208, 195, 0.45)';
    ctx.lineWidth = 1;
    ctx.strokeRect(36, 36, 440, 696);

    // Minimalist Art Composition: Warm Terracotta Arch & Charcoal Geometry
    ctx.fillStyle = '#B85D43';
    ctx.beginPath();
    ctx.arc(256, 320, 140, Math.PI, 0, false);
    ctx.lineTo(396, 540);
    ctx.lineTo(116, 540);
    ctx.closePath();
    ctx.fill();

    // Charcoal intersecting column / axis
    ctx.fillStyle = '#262422';
    ctx.fillRect(235, 160, 42, 380);

    // Ochre / sun disc
    ctx.fillStyle = '#D6A65D';
    ctx.beginPath();
    ctx.arc(320, 260, 48, 0, Math.PI * 2);
    ctx.fill();

    // Fine minimalist horizon line
    ctx.strokeStyle = '#262422';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(90, 480);
    ctx.lineTo(422, 480);
    ctx.stroke();

    // Modernist typography below composition
    ctx.fillStyle = '#3A3632';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('FORME & ESPACE · SÉRIE ARCHITECTURE', 88, 620);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787268';
    ctx.fillText('MUMBAI MODERN EXHIBITION · EDITION NO. 14/50', 88, 642);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt1Tex = createArchArtPrint1Texture();

// F4. Procedural Gallery Art Print 2: Bauhaus Geometric Axonometric Pavilion
function createArchArtPrint2Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Warm ivory archival paper
    ctx.fillStyle = '#F5F1E8';
    ctx.fillRect(0, 0, 512, 768);

    // Paper fiber texture
    for (let i = 0; i < 4000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        const alpha = Math.random() * 0.04;
        ctx.fillStyle = `rgba(120, 100, 80, ${alpha})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Passe-partout border
    ctx.strokeStyle = 'rgba(215, 208, 195, 0.45)';
    ctx.lineWidth = 1;
    ctx.strokeRect(36, 36, 440, 696);

    // Muted sage/olive color block
    ctx.fillStyle = '#5C6B50';
    ctx.fillRect(116, 220, 160, 260);

    // Warm taupe cantilever block
    ctx.fillStyle = '#9E8F83';
    ctx.fillRect(210, 310, 180, 180);

    // Crisp black axonometric structural lines
    ctx.strokeStyle = '#1E1D1B';
    ctx.lineWidth = 2.0;

    // Pavilion roof plane
    ctx.beginPath();
    ctx.moveTo(140, 200);
    ctx.lineTo(340, 150);
    ctx.lineTo(410, 230);
    ctx.lineTo(210, 280);
    ctx.closePath();
    ctx.stroke();

    // Vertical structural columns
    ctx.beginPath();
    ctx.moveTo(140, 200); ctx.lineTo(140, 480);
    ctx.moveTo(340, 150); ctx.lineTo(340, 430);
    ctx.moveTo(410, 230); ctx.lineTo(410, 510);
    ctx.moveTo(210, 280); ctx.lineTo(210, 540);
    ctx.stroke();

    // Modernist typography
    ctx.fillStyle = '#3A3632';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('STRUCTURE & MATIÈRE · ÉTUDE NO. 07', 88, 620);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787268';
    ctx.fillText('ATELIER MINIMALISTE · COLLECTION PRIVÉE', 88, 642);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt2Tex = createArchArtPrint2Texture();
"""

c = c.replace(tv_art_marker, tv_art_marker + new_textures)

# -----------------------------------------------------------------------------
# 2. ADD CURATED PBR MATERIALS
# -----------------------------------------------------------------------------
materials_marker = "const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({\n"
assert materials_marker in c, "materials_marker not found"

new_materials = """// Woven Jute/Wool Area Rug Material
const pbrJuteRug = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: juteRugTex,
    bumpMap: juteRugTex,
    bumpScale: 0.007,
    roughness: 0.94,
    metalness: 0.0,
    sheen: 0.35,
    sheenColor: new THREE.Color(0xF0E8DC),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Fluted Wood Slat Materials (Oak & Walnut)
const pbrFlutedOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    bumpMap: flutedWoodBumpTex,
    bumpScale: 0.012,
    roughness: 0.50,
    metalness: 0.0,
    clearcoat: 0.15,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrFlutedWalnut = new THREE.MeshPhysicalMaterial({
    color: 0x48382C,
    bumpMap: flutedWoodBumpTex,
    bumpScale: 0.010,
    roughness: 0.46,
    metalness: 0.0,
    clearcoat: 0.20,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Natural Muted Linen Pillow Materials (Terracotta, Warm Taupe, Olive)
const pbrMutedTerracotta = new THREE.MeshPhysicalMaterial({
    color: 0xB85D43,
    bumpMap: boucleTex,
    bumpScale: 0.005,
    roughness: 0.85,
    metalness: 0.0,
    sheen: 0.65,
    sheenColor: new THREE.Color(0xD47D64),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrWarmTaupe = new THREE.MeshPhysicalMaterial({
    color: 0x96877B,
    bumpMap: boucleTex,
    bumpScale: 0.005,
    roughness: 0.86,
    metalness: 0.0,
    sheen: 0.60,
    sheenColor: new THREE.Color(0xB5A89E),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrOliveLinen = new THREE.MeshPhysicalMaterial({
    color: 0x58664D,
    bumpMap: boucleTex,
    bumpScale: 0.005,
    roughness: 0.85,
    metalness: 0.0,
    sheen: 0.60,
    sheenColor: new THREE.Color(0x76876A),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Reflective Ultra-Thin OLED Glass Screen
const pbrOLEDGlass = new THREE.MeshPhysicalMaterial({
    map: tvArtTex,
    color: 0xFFFFFF,
    roughness: 0.05,
    metalness: 0.12,
    clearcoat: 0.95,
    clearcoatRoughness: 0.03,
    reflectivity: 0.80,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

"""

c = c.replace(materials_marker, new_materials + materials_marker)

# -----------------------------------------------------------------------------
# 3. REBUILD buildHabitableRoom()
# -----------------------------------------------------------------------------
living_start = "// ============================================================================\n// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)\n// ============================================================================"
living_end = "// ============================================================================\n// B. GOURMET KITCHEN ALCOVE"

start_idx = c.find(living_start)
end_idx = c.find(living_end)
assert start_idx != -1, "living_start not found"
assert end_idx != -1, "living_end not found"

new_living_code = """// ============================================================================
// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)
// ============================================================================
function buildHabitableRoom() {
    const group = new THREE.Group();

    // ------------------------------------------------------------------------
    // 1. UPGRADED TV FEATURE WALL
    // - Vertical fluted oak wood slats (3D physical geometry + bump map)
    // - Slim matte-black floating media console with 3 shadow-gap drawers
    // - Realistic 55-inch ultra-thin bezel OLED TV with specular glass reflection
    // ------------------------------------------------------------------------
    const tvGroup = new THREE.Group();

    // A. Architectural Fluted Oak Feature Slat Backdrop
    // Centered along the solid TV partition wall (z = -0.05 to 1.55, length = 1.60m)
    const slatBackdropX = 0.208;
    const slatBackdropZ = 0.75;
    const slatPanelW = 1.52;
    const slatPanelH = 2.18;

    // Base Oak Acoustic Backing Board
    const tvBackingPanel = new THREE.Mesh(
        new THREE.BoxGeometry(0.015, slatPanelH, slatPanelW),
        pbrScandinavianOak
    );
    tvBackingPanel.position.set(slatBackdropX, 1.42, slatBackdropZ);
    tvBackingPanel.castShadow = true;
    tvGroup.add(tvBackingPanel);

    // 38 Vertical Fluted Oak Slats (20mm wide x 16mm deep, spaced 40mm on center)
    const numSlats = 38;
    const slatSpacing = slatPanelW / numSlats;
    for (let i = 0; i < numSlats; i++) {
        const sz = (slatBackdropZ - slatPanelW / 2 + slatSpacing / 2) + i * slatSpacing;
        const slat = new THREE.Mesh(
            new RoundedBoxGeometry(0.016, slatPanelH - 0.02, 0.018, 4, 0.003),
            pbrFlutedOak
        );
        slat.position.set(slatBackdropX + 0.015, 1.42, sz);
        slat.castShadow = true;
        slat.receiveShadow = true;
        tvGroup.add(slat);
    }

    // Warm Ambient Bias Light (Ambilight glow washing behind TV onto fluted slats)
    const tvAmbiLight = new THREE.PointLight(0xFFB066, 1.35, 2.2, 2.0);
    tvAmbiLight.position.set(slatBackdropX + 0.04, 1.38, slatBackdropZ);
    tvGroup.add(tvAmbiLight);

    // B. Realistic 55-Inch Ultra-Thin Bezel OLED TV with Glass Reflection
    // Dimensions: 1.22m wide x 0.69m high x 0.012m deep
    const tvY = 1.38;
    const tvX = slatBackdropX + 0.038;

    // Razor-thin gunmetal/matte-black aluminum bezel frame
    const tvBezel = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.704, 1.234, 4, 0.003),
        pbrMatteBlackSteel
    );
    tvBezel.position.set(tvX, tvY, slatBackdropZ);
    tvBezel.castShadow = true;
    tvGroup.add(tvBezel);

    // Ultra-thin OLED display screen with specular glass reflections & ambient light response
    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);
    tvScreen.position.set(tvX + 0.007, tvY, slatBackdropZ);
    tvGroup.add(tvScreen);

    // C. Slim Matte-Black Floating Media Console with Shadow-Gap Drawers
    // Dimensions: Length: 1.46m, Depth: 0.32m, Height: 0.22m, floating at y = 0.40m
    const consoleX = 0.37;
    const consoleY = 0.40;
    const consoleCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.22, 1.46, 4, 0.008),
        pbrMatteBlackSteel
    );
    consoleCarcass.position.set(consoleX, consoleY, slatBackdropZ);
    consoleCarcass.castShadow = true;
    tvGroup.add(consoleCarcass);

    // 3 Individual Drawer Fronts with crisp 8mm shadow gaps & recessed brass J-pulls
    const drawerW = 0.465;
    for (let d = -1; d <= 1; d++) {
        const dCenterZ = slatBackdropZ + d * (drawerW + 0.012);
        const dFront = new THREE.Mesh(
            new RoundedBoxGeometry(0.014, 0.19, drawerW, 2, 0.003),
            pbrMatteBlackSteel
        );
        dFront.position.set(consoleX + 0.162, consoleY, dCenterZ);
        dFront.castShadow = true;
        tvGroup.add(dFront);

        // Recessed brushed brass lip pull along top edge
        const dPull = new THREE.Mesh(
            new RoundedBoxGeometry(0.012, 0.008, 0.16, 2, 0.002),
            pbrBrushedBrass
        );
        dPull.position.set(consoleX + 0.165, consoleY + 0.088, dCenterZ);
        tvGroup.add(dPull);
    }

    // Styling Decor on Console:
    // Minimalist architectural soundbar
    const soundbar = new THREE.Mesh(
        new RoundedBoxGeometry(0.065, 0.045, 0.88, 4, 0.006),
        pbrMatteBlackSteel
    );
    soundbar.position.set(consoleX + 0.02, consoleY + 0.135, slatBackdropZ);
    soundbar.castShadow = true;
    tvGroup.add(soundbar);

    const sbLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.003, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0x44AAFF })
    );
    sbLed.position.set(consoleX + 0.055, consoleY + 0.135, slatBackdropZ);
    tvGroup.add(sbLed);

    // Decorative ceramic bowl & sculptural brass ring object
    const decBowl = new THREE.Mesh(
        new THREE.CylinderGeometry(0.065, 0.045, 0.035, 24),
        pbrCeramicMat
    );
    decBowl.position.set(consoleX + 0.04, consoleY + 0.128, slatBackdropZ - 0.54);
    decBowl.castShadow = true;
    tvGroup.add(decBowl);

    const decRing = new THREE.Mesh(
        new THREE.TorusGeometry(0.042, 0.008, 12, 24),
        pbrBrushedBrass
    );
    decRing.rotation.y = 0.45;
    decRing.position.set(consoleX + 0.04, consoleY + 0.155, slatBackdropZ + 0.54);
    decRing.castShadow = true;
    tvGroup.add(decRing);

    // Soft grounded contact shadow beneath floating console
    createBlobShadow(0.44, 1.55, consoleX, slatBackdropZ, tvGroup, 0.44);
    group.add(tvGroup);

    // ------------------------------------------------------------------------
    // 2. TEXTURED WOVEN JUTE/WOOL AREA RUG (BENEATH SEATING ZONE)
    // Dimensions: 1.75m wide x 2.30m long x 0.012m high
    // ------------------------------------------------------------------------
    const rugGroup = new THREE.Group();
    const rugX = 1.85;
    const rugZ = 0.65;
    const rugMesh = new THREE.Mesh(
        new RoundedBoxGeometry(1.75, 0.012, 2.30, 4, 0.02),
        pbrJuteRug
    );
    rugMesh.position.set(rugX, 0.006, rugZ);
    rugMesh.receiveShadow = true;
    rugGroup.add(rugMesh);
    createBlobShadow(1.85, 2.40, rugX, rugZ, rugGroup, 0.30);
    group.add(rugGroup);

    // ------------------------------------------------------------------------
    // 3. FLUTED WALNUT & WHITE-MARBLE COFFEE TABLE
    // - Honed Calacatta marble slab top with beveled edges
    // - Fluted dark walnut under-apron / storage shelf
    // - Slim matte-black minimalist round steel legs with brass caps
    // - Styled with ceramic vase + eucalyptus sprigs, 2 art books & coffee cup
    // ------------------------------------------------------------------------
    const tableGroup = new THREE.Group();
    const tableX = 1.42;
    const tableY = 0.38;
    const tableZ = 0.60;

    // Honed Calacatta marble slab top
    const tableTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.54, 0.032, 0.92, 6, 0.014),
        pbrMarbleTable
    );
    tableTop.position.set(tableX, tableY, tableZ);
    tableTop.castShadow = true;
    tableTop.receiveShadow = true;
    tableGroup.add(tableTop);

    // Fluted Walnut Tambour Apron Under-Shelf
    const tableTambour = new THREE.Mesh(
        new RoundedBoxGeometry(0.46, 0.10, 0.82, 6, 0.015),
        pbrFlutedWalnut
    );
    tableTambour.position.set(tableX, tableY - 0.07, tableZ);
    tableTambour.castShadow = true;
    tableGroup.add(tableTambour);

    // 4 Slim Matte-Black Steel Round Legs with Brushed Brass Foot Ferrules
    for (let lx of [-0.21, 0.21]) {
        for (let lz of [-0.36, 0.36]) {
            const leg = new THREE.Mesh(
                new THREE.CylinderGeometry(0.010, 0.008, 0.23, 16),
                pbrMatteBlackSteel
            );
            leg.position.set(tableX + lx, 0.125, tableZ + lz);
            leg.castShadow = true;
            tableGroup.add(leg);

            // Brass ferrule cap
            const ferrule = new THREE.Mesh(
                new THREE.CylinderGeometry(0.009, 0.009, 0.035, 16),
                pbrBrushedBrass
            );
            ferrule.position.set(tableX + lx, 0.025, tableZ + lz);
            tableGroup.add(ferrule);
        }
    }

    // Decor 1: Artisanal Ribbed Matte Ceramic Vase with Botanical Eucalyptus Sprigs
    const vaseGeo = new THREE.CylinderGeometry(0.042, 0.065, 0.16, 24);
    const vaseMesh = new THREE.Mesh(vaseGeo, pbrCeramicMat);
    vaseMesh.position.set(tableX - 0.10, tableY + 0.096, tableZ - 0.22);
    vaseMesh.castShadow = true;
    tableGroup.add(vaseMesh);

    // Minimalist dried botanical / eucalyptus sprigs extending from vase
    for (let s of [-0.04, 0.0, 0.04]) {
        const stem = new THREE.Mesh(
            new THREE.CylinderGeometry(0.0025, 0.0025, 0.22, 8),
            pbrScandinavianOak
        );
        stem.position.set(tableX - 0.10 + s, tableY + 0.24, tableZ - 0.22 + s * 0.7);
        stem.rotation.z = s * 3.5;
        stem.rotation.x = s * 2.0;
        tableGroup.add(stem);

        const leaf = new THREE.Mesh(
            new THREE.SphereGeometry(0.018, 8, 6),
            pbrOliveLinen
        );
        leaf.scale.set(1.4, 0.3, 0.8);
        leaf.position.set(tableX - 0.10 + s * 1.8, tableY + 0.32, tableZ - 0.22 + s);
        tableGroup.add(leaf);
    }

    // Decor 2: Stack of 2 Luxury Hardcover Architectural Art Books
    const bookBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.024, 0.24, 2, 0.004),
        pbrMatteBlackSteel
    );
    bookBottom.position.set(tableX + 0.08, tableY + 0.028, tableZ + 0.10);
    bookBottom.rotation.y = 0.12;
    bookBottom.castShadow = true;
    tableGroup.add(bookBottom);

    const bookTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.16, 0.020, 0.21, 2, 0.004),
        pbrWarmTaupe
    );
    bookTop.position.set(tableX + 0.09, tableY + 0.050, tableZ + 0.10);
    bookTop.rotation.y = -0.06;
    bookTop.castShadow = true;
    tableGroup.add(bookTop);

    // Decor 3: Modern Matte Ceramic Coffee Cup & Saucer with Coffee
    const saucer = new THREE.Mesh(
        new THREE.CylinderGeometry(0.055, 0.045, 0.008, 24),
        pbrCeramicMat
    );
    saucer.position.set(tableX - 0.08, tableY + 0.020, tableZ + 0.26);
    tableGroup.add(saucer);

    const cup = new THREE.Mesh(
        new THREE.CylinderGeometry(0.034, 0.026, 0.048, 20),
        pbrCeramicMat
    );
    cup.position.set(tableX - 0.08, tableY + 0.045, tableZ + 0.26);
    cup.castShadow = true;
    tableGroup.add(cup);

    // Dark roast espresso inside cup
    const coffeeLiquid = new THREE.Mesh(
        new THREE.CylinderGeometry(0.030, 0.030, 0.004, 16),
        pbrMatteBlackSteel
    );
    coffeeLiquid.position.set(tableX - 0.08, tableY + 0.062, tableZ + 0.26);
    tableGroup.add(coffeeLiquid);

    // Soft grounded contact shadow beneath coffee table
    createBlobShadow(0.70, 1.10, tableX, tableZ, tableGroup, 0.40);
    group.add(tableGroup);

    // ------------------------------------------------------------------------
    // 4. REALISTIC L-SHAPED LINEN SOFA & NATURAL PINCHED THROW PILLOWS
    // - Multi-part RoundedBoxGeometry seat cushions, backrest, and armrests
    // - Soft bevels, subtle piping seams & tactile oatmeal/cream bouclé texture
    // - Pinched throw pillows in muted terracotta, warm taupe, and olive linen
    // - Sculpted knitted throw blanket draped naturally over chaise
    // ------------------------------------------------------------------------
    const sofaGroup = new THREE.Group();

    // Low smoked oak / walnut recessed plinth base frame
    const sofaPlinth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.06, 2.36, 4, 0.015),
        pbrFlutedWalnut
    );
    sofaPlinth.position.set(2.42, 0.03, 0.65);
    sofaPlinth.castShadow = true;
    sofaGroup.add(sofaPlinth);

    // Chaise Return Plinth extending forward towards the coffee table / window
    const chaisePlinth = new THREE.Mesh(
        new RoundedBoxGeometry(0.68, 0.06, 0.74, 4, 0.015),
        pbrFlutedWalnut
    );
    chaisePlinth.position.set(1.68, 0.03, -0.15);
    chaisePlinth.castShadow = true;
    sofaGroup.add(chaisePlinth);

    // Main sculpted seat base platform in oatmeal/cream bouclé linen
    const sMainBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.92, 0.26, 2.38, 8, 0.05),
        pbrBoucleLinen
    );
    sMainBase.position.set(2.42, 0.19, 0.65);
    sMainBase.castShadow = true;
    sofaGroup.add(sMainBase);

    // Chaise Lounge Forward Return Platform (forming authentic L-shape)
    const sChaiseBase = new THREE.Mesh(
        new RoundedBoxGeometry(0.66, 0.26, 0.76, 8, 0.05),
        pbrBoucleLinen
    );
    sChaiseBase.position.set(1.68, 0.19, -0.15);
    sChaiseBase.castShadow = true;
    sofaGroup.add(sChaiseBase);

    // Sculpted ergonomic backrest running along the solid East wall (x = 2.76)
    const sBack = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.50, 2.38, 8, 0.06),
        pbrBoucleLinen
    );
    sBack.position.set(2.75, 0.55, 0.65);
    sBack.castShadow = true;
    sofaGroup.add(sBack);

    // Sculpted South Armrest at z = 1.80
    const armSouth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armSouth.position.set(2.40, 0.44, 1.76);
    armSouth.castShadow = true;
    sofaGroup.add(armSouth);

    // Sculpted North Chaise Armrest at z = -0.48
    const armNorth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armNorth.position.set(2.40, 0.44, -0.46);
    armNorth.castShadow = true;
    sofaGroup.add(armNorth);

    // Deep plush seat cushions with generous rounded bevels & piping seams
    // 2 Standard Seat Cushions on South / Middle section
    for (let i = 0; i < 2; i++) {
        const cz = 0.65 + (i === 0 ? 0.38 : 0.98);
        const sc = new THREE.Mesh(
            new RoundedBoxGeometry(0.72, 0.15, 0.58, 8, 0.045),
            pbrBoucleLinen
        );
        sc.position.set(2.32, 0.39, cz);
        sc.rotation.z = -0.02; // Subtle natural lean back
        sc.castShadow = true;
        sc.receiveShadow = true;
        sofaGroup.add(sc);

        // Matching ergonomic back cushions with natural backward lean
        const bc = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.40, 0.56, 8, 0.05),
            pbrBoucleLinen
        );
        bc.position.set(2.64, 0.63, cz);
        bc.rotation.z = 0.18; // Leaning back naturally against sofa back
        bc.castShadow = true;
        sofaGroup.add(bc);
    }

    // Extended Chaise Cushion with Piping Seam (Deep Lounge Zone)
    const chaiseCushion = new THREE.Mesh(
        new RoundedBoxGeometry(1.42, 0.15, 0.68, 8, 0.05),
        pbrBoucleLinen
    );
    chaiseCushion.position.set(1.97, 0.39, -0.06);
    chaiseCushion.rotation.z = -0.015;
    chaiseCushion.castShadow = true;
    chaiseCushion.receiveShadow = true;
    sofaGroup.add(chaiseCushion);

    const chaiseBackCushion = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.40, 0.66, 8, 0.05),
        pbrBoucleLinen
    );
    chaiseBackCushion.position.set(2.64, 0.63, -0.06);
    chaiseBackCushion.rotation.z = 0.18;
    chaiseBackCushion.castShadow = true;
    sofaGroup.add(chaiseBackCushion);

    // Natural Pinched Throw Pillows in Muted Terracotta, Warm Taupe & Olive Linen
    // Pillow 1: Muted Terracotta (Corner Chaise)
    const pTerracotta = new THREE.Mesh(
        new RoundedBoxGeometry(0.38, 0.38, 0.14, 6, 0.04),
        pbrMutedTerracotta
    );
    pTerracotta.position.set(2.44, 0.58, -0.22);
    pTerracotta.rotation.y = 0.28;
    pTerracotta.rotation.z = 0.14;
    pTerracotta.castShadow = true;
    sofaGroup.add(pTerracotta);

    // Pillow 2: Warm Taupe Linen (Tucked beside Terracotta)
    const pTaupe = new THREE.Mesh(
        new RoundedBoxGeometry(0.35, 0.35, 0.13, 6, 0.038),
        pbrWarmTaupe
    );
    pTaupe.position.set(2.46, 0.56, 0.22);
    pTaupe.rotation.y = -0.20;
    pTaupe.rotation.z = 0.12;
    pTaupe.castShadow = true;
    sofaGroup.add(pTaupe);

    // Pillow 3: Olive Linen (South Seating Zone)
    const pOlive = new THREE.Mesh(
        new RoundedBoxGeometry(0.36, 0.36, 0.13, 6, 0.038),
        pbrOliveLinen
    );
    pOlive.position.set(2.44, 0.58, 0.88);
    pOlive.rotation.y = 0.22;
    pOlive.rotation.z = 0.14;
    pOlive.castShadow = true;
    sofaGroup.add(pOlive);

    // Pillow 4: Oatmeal Bouclé Accent Cushion with soft piping
    const pOatmeal = new THREE.Mesh(
        new RoundedBoxGeometry(0.32, 0.32, 0.12, 6, 0.035),
        pbrBoucleLinen
    );
    pOatmeal.position.set(2.42, 0.55, 1.45);
    pOatmeal.rotation.y = -0.16;
    pOatmeal.rotation.z = 0.12;
    pOatmeal.castShadow = true;
    sofaGroup.add(pOatmeal);

    // Sculpted Knitted Throw Blanket with Folded Seams Draped Over Chaise Edge
    const throwBlanket = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.38, 0.46, 6, 0.035),
        pbrWarmTaupe
    );
    throwBlanket.position.set(1.48, 0.38, -0.10);
    throwBlanket.rotation.y = 0.15;
    throwBlanket.castShadow = true;
    sofaGroup.add(throwBlanket);

    // Grounded Contact Shadow beneath entire L-shaped Sofa footprint
    createBlobShadow(1.30, 2.50, 2.35, 0.65, sofaGroup, 0.45);
    createBlobShadow(0.75, 0.90, 1.68, -0.15, sofaGroup, 0.38);
    group.add(sofaGroup);

    // ------------------------------------------------------------------------
    // 5. DRESSED BLANK WALL: 2 FRAMED MINIMALIST ARCHITECTURAL ART PRINTS
    //    WITH WARM PICTURE-LIGHT SCONCES
    // Mounted flush against East plaster wall (x = 2.92, facing west)
    // ------------------------------------------------------------------------
    const artGroup = new THREE.Group();
    const artWallX = 2.92;
    const artY = 1.76;
    const frameW = 0.56;
    const frameH = 0.74;

    const prints = [
        { z: 0.18, tex: archArt1Tex, name: "ArtPrint1" },
        { z: 0.96, tex: archArt2Tex, name: "ArtPrint2" }
    ];

    prints.forEach((pr, idx) => {
        const pGroup = new THREE.Group();

        // Slim matte-black anodized aluminum gallery frame
        const frameMesh = new THREE.Mesh(
            new RoundedBoxGeometry(0.022, frameH, frameW, 2, 0.003),
            pbrMatteBlackSteel
        );
        frameMesh.position.set(artWallX - 0.011, artY, pr.z);
        frameMesh.castShadow = true;
        pGroup.add(frameMesh);

        // Art print canvas face
        const artCanvasGeo = new THREE.PlaneGeometry(frameW - 0.035, frameH - 0.035);
        artCanvasGeo.rotateY(-Math.PI / 2);
        const artMat = new THREE.MeshPhysicalMaterial({
            map: pr.tex,
            roughness: 0.88,
            metalness: 0.0,
            clippingPlanes: [clipHeightPlane],
            transparent: false,
            depthWrite: true
        });
        const artCanvas = new THREE.Mesh(artCanvasGeo, artMat);
        artCanvas.position.set(artWallX - 0.020, artY, pr.z);
        pGroup.add(artCanvas);

        // Protective museum glass with subtle ambient reflection
        const glassGeo = new THREE.PlaneGeometry(frameW - 0.03, frameH - 0.03);
        glassGeo.rotateY(-Math.PI / 2);
        const glassMat = new THREE.MeshPhysicalMaterial({
            color: 0xFFFFFF,
            transmission: 0.94,
            transparent: true,
            opacity: 0.88,
            roughness: 0.04,
            ior: 1.52,
            clearcoat: 0.90,
            clearcoatRoughness: 0.03,
            clippingPlanes: [clipHeightPlane]
        });
        const glassMesh = new THREE.Mesh(glassGeo, glassMat);
        glassMesh.position.set(artWallX - 0.022, artY, pr.z);
        pGroup.add(glassMesh);

        // Warm Picture-Light Sconce Mounted Overhead
        const sconceY = artY + frameH / 2 + 0.12;
        const sconceGroup = new THREE.Group();

        // Wall mounting backplate
        const backplate = new THREE.Mesh(
            new THREE.BoxGeometry(0.012, 0.06, 0.06),
            pbrBrushedBrass
        );
        backplate.position.set(artWallX - 0.006, sconceY, pr.z);
        sconceGroup.add(backplate);

        // Dual curved swan-neck brass arms extending 14cm from wall
        for (let az of [-0.08, 0.08]) {
            const armGeo = new THREE.CylinderGeometry(0.004, 0.004, 0.14, 12);
            armGeo.rotateZ(Math.PI / 2);
            const arm = new THREE.Mesh(armGeo, pbrBrushedBrass);
            arm.position.set(artWallX - 0.076, sconceY + 0.01, pr.z + az);
            sconceGroup.add(arm);
        }

        // Horizontal tubular brass light bar (0.34m long)
        const barGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.34, 16);
        barGeo.rotateX(Math.PI / 2);
        const lightBar = new THREE.Mesh(barGeo, pbrBrushedBrass);
        lightBar.position.set(artWallX - 0.146, sconceY + 0.01, pr.z);
        lightBar.castShadow = true;
        sconceGroup.add(lightBar);

        // Underside warm light diffuser emitting #FFE4B5
        const diffGeo = new THREE.CylinderGeometry(0.003, 0.003, 0.30, 12);
        diffGeo.rotateX(Math.PI / 2);
        const diffMat = new THREE.MeshBasicMaterial({ color: 0xFFE4B5 });
        const diffuser = new THREE.Mesh(diffGeo, diffMat);
        diffuser.position.set(artWallX - 0.146, sconceY + 0.002, pr.z);
        sconceGroup.add(diffuser);

        // Dedicated warm picture spotlight illuminating artwork & wall plaster
        const picLight = new THREE.PointLight(0xFFE4B5, 0.90, 1.8, 2.0);
        picLight.position.set(artWallX - 0.16, sconceY - 0.02, pr.z);
        sconceGroup.add(picLight);

        pGroup.add(sconceGroup);
        artGroup.add(pGroup);
    });

    group.add(artGroup);

    // ------------------------------------------------------------------------
    // 6. DINING SUITE (OAK & MARBLE TABLE + SCANDINAVIAN CHAIRS)
    // ------------------------------------------------------------------------
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

    // ------------------------------------------------------------------------
    // 7. WALL-MOUNTED SPLIT AIR CONDITIONER (LIVING ROOM)
    // ------------------------------------------------------------------------
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

    // ------------------------------------------------------------------------
    // 8. ARCHITECTURAL FRENCH WINDOW SYSTEM WITH MULLIONS & ARCHITECTURAL GLASS
    // ------------------------------------------------------------------------
    const windowGroup = new THREE.Group();
    windowGroup.position.set(1.575, 1.10, -1.15);

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

    const centerMullion = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.14, 0.08), pbrMatteBlackSteel);
    centerMullion.position.set(0, 0, 0);
    windowGroup.add(centerMullion);

    const fixedHorizMullion = new THREE.Mesh(new THREE.BoxGeometry(1.14, 0.04, 0.05), pbrMatteBlackSteel);
    fixedHorizMullion.position.set(0.60, 0.15, 0);
    windowGroup.add(fixedHorizMullion);

    const fixedUpperGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 0.88, 0.02), pbrArchitecturalGlass);
    fixedUpperGlass.position.set(0.60, 0.61, 0);
    windowGroup.add(fixedUpperGlass);

    const fixedLowerGlass = new THREE.Mesh(new THREE.BoxGeometry(1.13, 1.15, 0.02), pbrArchitecturalGlass);
    fixedLowerGlass.position.set(0.60, -0.45, 0);
    windowGroup.add(fixedLowerGlass);

    const handleRight = new THREE.Mesh(new RoundedBoxGeometry(0.015, 0.28, 0.025, 2, 0.005), pbrBrushedSteel);
    handleRight.position.set(0.06, 0.0, -0.04);
    windowGroup.add(handleRight);

    group.add(windowGroup);

    materialGroup.add(group);
}
"""

c = c[:start_idx] + new_living_code + "\n" + c[end_idx:]

# -----------------------------------------------------------------------------
# 4. CALIBRATE STOP 2 CAMERA WAYPOINTS FOR BALANCED COMPOSITION
# -----------------------------------------------------------------------------
old_leg2 = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.55,
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepLivingZ: -1.15,
    posX: 0.85,
    posY: 1.55,
    posZ: 2.10,
    targetX: 1.85,
    targetY: 1.15,
    targetZ: 0.50,
    duration: 0.08,
    ease: 'none'
});"""

new_leg2 = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepLivingZ: -1.15,
    posX: 0.95,
    posY: 1.50,
    posZ: 2.15,
    targetX: 1.55,
    targetY: 1.12,
    targetZ: 0.60,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepLivingZ: -1.15,
    posX: 0.95,
    posY: 1.50,
    posZ: 2.15,
    targetX: 1.55,
    targetY: 1.12,
    targetZ: 0.60,
    duration: 0.08,
    ease: 'none'
});"""

assert old_leg2 in c, "old_leg2 not found in script.js"
c = c.replace(old_leg2, new_leg2)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied Living Sanctuary Overhaul to script.js!")
