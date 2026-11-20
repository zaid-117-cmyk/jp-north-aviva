import os
import re

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. UPDATE BOUCLE LINEN TEXTURE AND COLOR TO WARM OATMEAL
# -----------------------------------------------------------------------------
boucle_func_start = "function createBoucleLinenTexture() {"
boucle_func_end = "const boucleTex = createBoucleLinenTexture();"

idx_b1 = c.find(boucle_func_start)
idx_b2 = c.find(boucle_func_end)
assert idx_b1 != -1 and idx_b2 != -1, "boucle texture function not found"

new_boucle_func = """function createBoucleLinenTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#DCD3C5';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 0; y < 512; y += 4) {
        for (let x = 0; x < 512; x += 4) {
            const pattern = ((x + y) % 8 === 0) ? 18 : -14;
            const noise = (Math.random() - 0.5) * 22;
            const val = Math.min(255, Math.max(0, 205 + pattern + noise));
            ctx.fillStyle = `rgb(${val},${Math.round(val * 0.95)},${Math.round(val * 0.88)})`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(6, 6);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const boucleTex = createBoucleLinenTexture();"""

c = c[:idx_b1] + new_boucle_func + c[idx_b2 + len(boucle_func_end):]

# -----------------------------------------------------------------------------
# 2. UPDATE ART PRINTS 1 & 2 TEXTURES (HIGH CONTRAST, RICH PIGMENTS, NO BLOCKING)
# -----------------------------------------------------------------------------
art1_start = "function createArchArtPrint1Texture() {"
art2_end = "const archArt2Tex = createArchArtPrint2Texture();"

idx_a1 = c.find(art1_start)
idx_a2 = c.find(art2_end)
assert idx_a1 != -1 and idx_a2 != -1, "art print texture functions not found"

new_art_funcs = """function createArchArtPrint1Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Museum archival warm ivory paper
    ctx.fillStyle = '#F4EFE6';
    ctx.fillRect(0, 0, 512, 768);

    // Subtle paper grain
    for (let i = 0; i < 5000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        ctx.fillStyle = `rgba(100, 80, 60, ${Math.random() * 0.05})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Outer white passe-partout museum matting border (40px)
    ctx.fillStyle = '#FCFAF7';
    ctx.fillRect(36, 36, 440, 696);
    ctx.strokeStyle = '#D8D0C2';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(36, 36, 440, 696);

    // Inner art field background
    ctx.fillStyle = '#EFE9DE';
    ctx.fillRect(60, 60, 392, 540);

    // Minimalist Art Composition: Warm Terracotta Arch & Charcoal Geometry
    // 1. Terracotta grand arch
    ctx.fillStyle = '#B2533E';
    ctx.beginPath();
    ctx.arc(256, 310, 130, Math.PI, 0, false);
    ctx.lineTo(386, 520);
    ctx.lineTo(126, 520);
    ctx.closePath();
    ctx.fill();

    // 2. Bold Charcoal intersecting column / axis
    ctx.fillStyle = '#1E1D1B';
    ctx.fillRect(234, 150, 44, 370);

    // 3. Ochre sun disc
    ctx.fillStyle = '#D6A456';
    ctx.beginPath();
    ctx.arc(315, 250, 46, 0, Math.PI * 2);
    ctx.fill();

    // 4. Fine structural horizon line
    ctx.strokeStyle = '#1E1D1B';
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    ctx.moveTo(90, 460);
    ctx.lineTo(422, 460);
    ctx.stroke();

    // Modernist typography below composition
    ctx.fillStyle = '#2A2622';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('FORME & ESPACE · SÉRIE ARCHITECTURE', 75, 642);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787064';
    ctx.fillText('MUMBAI MODERN EXHIBITION · EDITION NO. 14/50', 75, 664);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt1Tex = createArchArtPrint1Texture();

function createArchArtPrint2Texture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 768;
    const ctx = c.getContext('2d');

    // Museum archival warm ivory paper
    ctx.fillStyle = '#F4EFE6';
    ctx.fillRect(0, 0, 512, 768);

    // Subtle paper grain
    for (let i = 0; i < 5000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 768;
        ctx.fillStyle = `rgba(100, 80, 60, ${Math.random() * 0.05})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Outer white passe-partout museum matting border (40px)
    ctx.fillStyle = '#FCFAF7';
    ctx.fillRect(36, 36, 440, 696);
    ctx.strokeStyle = '#D8D0C2';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(36, 36, 440, 696);

    // Inner art field background
    ctx.fillStyle = '#EBE5D8';
    ctx.fillRect(60, 60, 392, 540);

    // Minimalist Bauhaus Axonometric Pavilion Composition
    // 1. Muted sage/olive color block
    ctx.fillStyle = '#4E5E44';
    ctx.fillRect(116, 200, 160, 260);

    // 2. Warm taupe cantilever block
    ctx.fillStyle = '#8C7D70';
    ctx.fillRect(210, 290, 180, 170);

    // 3. Charcoal axonometric lines
    ctx.strokeStyle = '#1A1816';
    ctx.lineWidth = 2.5;

    // Pavilion roof plane
    ctx.beginPath();
    ctx.moveTo(130, 180);
    ctx.lineTo(340, 130);
    ctx.lineTo(410, 210);
    ctx.lineTo(200, 260);
    ctx.closePath();
    ctx.stroke();

    // Vertical structural columns
    ctx.beginPath();
    ctx.moveTo(130, 180); ctx.lineTo(130, 460);
    ctx.moveTo(340, 130); ctx.lineTo(340, 410);
    ctx.moveTo(410, 210); ctx.lineTo(410, 490);
    ctx.moveTo(200, 260); ctx.lineTo(200, 510);
    ctx.stroke();

    // Modernist typography
    ctx.fillStyle = '#2A2622';
    ctx.font = '600 13px "Plus Jakarta Sans", sans-serif';
    ctx.fillText('STRUCTURE & MATIÈRE · ÉTUDE NO. 07', 75, 642);
    ctx.font = '400 10px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = '#787064';
    ctx.fillText('ATELIER MINIMALISTE · COLLECTION PRIVÉE', 75, 664);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const archArt2Tex = createArchArtPrint2Texture();"""

c = c[:idx_a1] + new_art_funcs + c[idx_a2 + len(art2_end):]

# -----------------------------------------------------------------------------
# 3. UPDATE pbrBoucleLinen DEFINITION
# -----------------------------------------------------------------------------
pbr_boucle_target = """const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xE8E1D7,"""
pbr_boucle_replace = """const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xD8CFBF,"""
if pbr_boucle_target in c:
    c = c.replace(pbr_boucle_target, pbr_boucle_replace)

# -----------------------------------------------------------------------------
# 4. REBUILD buildHabitableRoom() WITH ACCURATE SCONCES, ART PRINTS, PINCHED PILLOWS & CLEAR FOREGROUND
# -----------------------------------------------------------------------------
living_start = "// ============================================================================\n// A. HABITABLE ROOM (LIVING & DINING SANCTUARY)\n// ============================================================================"
living_end = "// ============================================================================\n// B. GOURMET KITCHEN ALCOVE"

idx_l1 = c.find(living_start)
idx_l2 = c.find(living_end)
assert idx_l1 != -1 and idx_l2 != -1, "living section not found"

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

    // Realistic 55-Inch Ultra-Thin Bezel OLED TV with Glass Reflection
    const tvY = 1.38;
    const tvX = slatBackdropX + 0.038;

    const tvBezel = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.704, 1.234, 4, 0.003),
        pbrMatteBlackSteel
    );
    tvBezel.position.set(tvX, tvY, slatBackdropZ);
    tvBezel.castShadow = true;
    tvGroup.add(tvBezel);

    const tvScreenGeo = new THREE.PlaneGeometry(1.22, 0.686);
    tvScreenGeo.rotateY(Math.PI / 2);
    const tvScreen = new THREE.Mesh(tvScreenGeo, pbrOLEDGlass);
    tvScreen.position.set(tvX + 0.007, tvY, slatBackdropZ);
    tvGroup.add(tvScreen);

    // Slim Matte-Black Floating Media Console with Shadow-Gap Drawers
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

        const dPull = new THREE.Mesh(
            new RoundedBoxGeometry(0.012, 0.008, 0.16, 2, 0.002),
            pbrBrushedBrass
        );
        dPull.position.set(consoleX + 0.165, consoleY + 0.088, dCenterZ);
        tvGroup.add(dPull);
    }

    // Styling Decor on Console: Soundbar, Ceramic Bowl, Brass Ring
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

    createBlobShadow(0.44, 1.55, consoleX, slatBackdropZ, tvGroup, 0.44);
    group.add(tvGroup);

    // ------------------------------------------------------------------------
    // 2. TEXTURED WOVEN JUTE/WOOL AREA RUG (BENEATH SEATING ZONE)
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

    const tableTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.56, 0.036, 0.96, 6, 0.014),
        pbrMarbleTable
    );
    tableTop.position.set(tableX, tableY, tableZ);
    tableTop.castShadow = true;
    tableTop.receiveShadow = true;
    tableGroup.add(tableTop);

    const tableTambour = new THREE.Mesh(
        new RoundedBoxGeometry(0.48, 0.11, 0.86, 6, 0.015),
        pbrFlutedWalnut
    );
    tableTambour.position.set(tableX, tableY - 0.075, tableZ);
    tableTambour.castShadow = true;
    tableGroup.add(tableTambour);

    for (let lx of [-0.21, 0.21]) {
        for (let lz of [-0.38, 0.38]) {
            const leg = new THREE.Mesh(
                new THREE.CylinderGeometry(0.010, 0.008, 0.22, 16),
                pbrMatteBlackSteel
            );
            leg.position.set(tableX + lx, 0.12, tableZ + lz);
            leg.castShadow = true;
            tableGroup.add(leg);

            const ferrule = new THREE.Mesh(
                new THREE.CylinderGeometry(0.009, 0.009, 0.035, 16),
                pbrBrushedBrass
            );
            ferrule.position.set(tableX + lx, 0.025, tableZ + lz);
            tableGroup.add(ferrule);
        }
    }

    // Decor 1: Ceramic Vase with Eucalyptus Sprigs
    const vaseMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.042, 0.065, 0.16, 24),
        pbrCeramicMat
    );
    vaseMesh.position.set(tableX - 0.10, tableY + 0.098, tableZ - 0.24);
    vaseMesh.castShadow = true;
    tableGroup.add(vaseMesh);

    for (let s of [-0.04, 0.0, 0.04]) {
        const stem = new THREE.Mesh(
            new THREE.CylinderGeometry(0.0025, 0.0025, 0.22, 8),
            pbrScandinavianOak
        );
        stem.position.set(tableX - 0.10 + s, tableY + 0.24, tableZ - 0.24 + s * 0.7);
        stem.rotation.z = s * 3.5;
        stem.rotation.x = s * 2.0;
        tableGroup.add(stem);

        const leaf = new THREE.Mesh(
            new THREE.SphereGeometry(0.018, 8, 6),
            pbrOliveLinen
        );
        leaf.scale.set(1.4, 0.3, 0.8);
        leaf.position.set(tableX - 0.10 + s * 1.8, tableY + 0.32, tableZ - 0.24 + s);
        tableGroup.add(leaf);
    }

    // Decor 2: Stack of 2 Luxury Hardcover Architectural Art Books
    const bookBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.024, 0.24, 2, 0.004),
        pbrMatteBlackSteel
    );
    bookBottom.position.set(tableX + 0.08, tableY + 0.030, tableZ + 0.08);
    bookBottom.rotation.y = 0.12;
    bookBottom.castShadow = true;
    tableGroup.add(bookBottom);

    const bookTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.16, 0.020, 0.21, 2, 0.004),
        pbrWarmTaupe
    );
    bookTop.position.set(tableX + 0.09, tableY + 0.052, tableZ + 0.08);
    bookTop.rotation.y = -0.06;
    bookTop.castShadow = true;
    tableGroup.add(bookTop);

    // Decor 3: Ceramic Coffee Cup & Saucer
    const saucer = new THREE.Mesh(
        new THREE.CylinderGeometry(0.055, 0.045, 0.008, 24),
        pbrCeramicMat
    );
    saucer.position.set(tableX - 0.08, tableY + 0.022, tableZ + 0.26);
    tableGroup.add(saucer);

    const cup = new THREE.Mesh(
        new THREE.CylinderGeometry(0.034, 0.026, 0.048, 20),
        pbrCeramicMat
    );
    cup.position.set(tableX - 0.08, tableY + 0.047, tableZ + 0.26);
    cup.castShadow = true;
    tableGroup.add(cup);

    const coffeeLiquid = new THREE.Mesh(
        new THREE.CylinderGeometry(0.030, 0.030, 0.004, 16),
        pbrMatteBlackSteel
    );
    coffeeLiquid.position.set(tableX - 0.08, tableY + 0.064, tableZ + 0.26);
    tableGroup.add(coffeeLiquid);

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

    // Sculpted ergonomic backrest running along the solid East wall (x = 2.75)
    const sBack = new THREE.Mesh(
        new RoundedBoxGeometry(0.26, 0.50, 2.38, 8, 0.06),
        pbrBoucleLinen
    );
    sBack.position.set(2.75, 0.55, 0.65);
    sBack.castShadow = true;
    sofaGroup.add(sBack);

    // Sculpted South Armrest at z = 1.76
    const armSouth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armSouth.position.set(2.40, 0.44, 1.76);
    armSouth.castShadow = true;
    sofaGroup.add(armSouth);

    // Sculpted North Chaise Armrest at z = -0.46
    const armNorth = new THREE.Mesh(
        new RoundedBoxGeometry(0.90, 0.25, 0.16, 8, 0.045),
        pbrBoucleLinen
    );
    armNorth.position.set(2.40, 0.44, -0.46);
    armNorth.castShadow = true;
    sofaGroup.add(armNorth);

    // 2 Standard Seat Cushions on South / Middle section
    for (let i = 0; i < 2; i++) {
        const cz = 0.65 + (i === 0 ? 0.38 : 0.98);
        const sc = new THREE.Mesh(
            new RoundedBoxGeometry(0.72, 0.15, 0.58, 8, 0.045),
            pbrBoucleLinen
        );
        sc.position.set(2.32, 0.39, cz);
        sc.rotation.z = -0.02;
        sc.castShadow = true;
        sc.receiveShadow = true;
        sofaGroup.add(sc);

        const bc = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.40, 0.56, 8, 0.05),
            pbrBoucleLinen
        );
        bc.position.set(2.64, 0.63, cz);
        bc.rotation.z = 0.18;
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
    // Helper to build realistic pinched pillow with piping border
    function buildPinchedPillow(w, h, d, mat, px, py, pz, rotY, rotZ) {
        const pGroup = new THREE.Group();
        pGroup.position.set(px, py, pz);
        pGroup.rotation.y = rotY;
        pGroup.rotation.z = rotZ;

        // Main soft pillow body
        const body = new THREE.Mesh(new RoundedBoxGeometry(d, h, w, 8, 0.045), mat);
        body.castShadow = true;
        pGroup.add(body);

        // Subtle perimeter piping welt
        const welt = new THREE.Mesh(new RoundedBoxGeometry(d * 0.92, h + 0.008, w + 0.008, 4, 0.008), mat);
        pGroup.add(welt);

        return pGroup;
    }

    // Pillow 1: Muted Terracotta (Corner Chaise)
    const pTerra = buildPinchedPillow(0.38, 0.38, 0.13, pbrMutedTerracotta, 2.42, 0.56, -0.20, 0.26, 0.14);
    sofaGroup.add(pTerra);

    // Pillow 2: Warm Taupe Linen (Tucked beside Terracotta)
    const pTau = buildPinchedPillow(0.35, 0.35, 0.12, pbrWarmTaupe, 2.45, 0.54, 0.22, -0.18, 0.12);
    sofaGroup.add(pTau);

    // Pillow 3: Olive Linen (South Seating Zone)
    const pOli = buildPinchedPillow(0.36, 0.36, 0.13, pbrOliveLinen, 2.42, 0.56, 0.88, 0.20, 0.14);
    sofaGroup.add(pOli);

    // Pillow 4: Oatmeal Bouclé Accent Cushion
    const pOat = buildPinchedPillow(0.32, 0.32, 0.11, pbrBoucleLinen, 2.40, 0.53, 1.45, -0.15, 0.12);
    sofaGroup.add(pOat);

    // Sculpted Knitted Throw Blanket with Folded Seams Draped Over Chaise Edge
    const throwBlanket = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.38, 0.46, 6, 0.035),
        pbrWarmTaupe
    );
    throwBlanket.position.set(1.48, 0.38, -0.10);
    throwBlanket.rotation.y = 0.15;
    throwBlanket.castShadow = true;
    sofaGroup.add(throwBlanket);

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
    const artY = 1.65;
    const frameW = 0.54;
    const frameH = 0.72;

    const prints = [
        { z: 0.10, tex: archArt1Tex, name: "ArtPrint1" },
        { z: 0.74, tex: archArt2Tex, name: "ArtPrint2" }
    ];

    prints.forEach((pr) => {
        const pGroup = new THREE.Group();

        // Slim matte-black anodized aluminum gallery frame
        const frameMesh = new THREE.Mesh(
            new RoundedBoxGeometry(0.024, frameH, frameW, 2, 0.003),
            pbrMatteBlackSteel
        );
        frameMesh.position.set(artWallX - 0.012, artY, pr.z);
        frameMesh.castShadow = true;
        pGroup.add(frameMesh);

        // Art print canvas face with built-in reflective glass clearcoat sheen (Zero blocking)
        const artCanvasGeo = new THREE.PlaneGeometry(frameW - 0.035, frameH - 0.035);
        artCanvasGeo.rotateY(-Math.PI / 2);
        const artMat = new THREE.MeshPhysicalMaterial({
            map: pr.tex,
            roughness: 0.18,
            metalness: 0.0,
            clearcoat: 0.80,
            clearcoatRoughness: 0.06,
            reflectivity: 0.60,
            clippingPlanes: [clipHeightPlane],
            side: THREE.FrontSide,
            transparent: false,
            depthWrite: true
        });
        const artCanvas = new THREE.Mesh(artCanvasGeo, artMat);
        artCanvas.position.set(artWallX - 0.025, artY, pr.z);
        pGroup.add(artCanvas);

        // Warm Picture-Light Sconce Mounted Overhead
        const sconceY = artY + frameH / 2 + 0.10;
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

        // Horizontal tubular brass light bar (0.32m long)
        const barGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.32, 16);
        barGeo.rotateX(Math.PI / 2);
        const lightBar = new THREE.Mesh(barGeo, pbrBrushedBrass);
        lightBar.position.set(artWallX - 0.146, sconceY + 0.01, pr.z);
        lightBar.castShadow = true;
        sconceGroup.add(lightBar);

        // Underside warm light diffuser emitting #FFE4B5
        const diffGeo = new THREE.CylinderGeometry(0.003, 0.003, 0.28, 12);
        diffGeo.rotateX(Math.PI / 2);
        const diffMat = new THREE.MeshBasicMaterial({ color: 0xFFE4B5 });
        const diffuser = new THREE.Mesh(diffGeo, diffMat);
        diffuser.position.set(artWallX - 0.146, sconceY + 0.002, pr.z);
        sconceGroup.add(diffuser);

        // Dedicated warm picture spotlight illuminating artwork & wall plaster
        const picLight = new THREE.PointLight(0xFFE4B5, 0.95, 1.8, 2.0);
        picLight.position.set(artWallX - 0.16, sconceY - 0.02, pr.z);
        sconceGroup.add(picLight);

        pGroup.add(sconceGroup);
        artGroup.add(pGroup);
    });

    group.add(artGroup);

    // ------------------------------------------------------------------------
    // 6. DINING SUITE (OAK & MARBLE TABLE + SCANDINAVIAN CHAIRS)
    // Positioned neatly with chairs tucked on East/West sides for clear foreground
    // ------------------------------------------------------------------------
    const diningGroup = new THREE.Group();
    const dTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 1.05, 4, 0.015), pbrCalacattaFloor);
    dTop.position.set(1.40, 0.76, 2.10);
    dTop.castShadow = true;
    diningGroup.add(dTop);

    const dPedestal = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 0.74, 24), pbrScandinavianOak);
    dPedestal.position.set(1.40, 0.37, 2.10);
    dPedestal.castShadow = true;
    diningGroup.add(dPedestal);

    // Chairs neatly tucked along East & West sides (cx = [-0.36, 0.36])
    for (let cx of [-0.36, 0.36]) {
        const chairGroup = new THREE.Group();
        chairGroup.position.set(1.40 + cx, 0, 2.10);
        chairGroup.rotation.y = (cx < 0) ? Math.PI / 2 : -Math.PI / 2;

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
        cBack.position.set(0, 0.68, -0.19);
        cBack.castShadow = true;
        chairGroup.add(cBack);

        diningGroup.add(chairGroup);
    }

    const plate1 = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
    plate1.position.set(1.22, 0.785, 2.10);
    diningGroup.add(plate1);

    const plate2 = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.10, 0.015, 24), pbrWhisperingSmoke);
    plate2.position.set(1.58, 0.785, 2.10);
    diningGroup.add(plate2);

    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.06, 0.18, 16), pbrWhisperingSmoke);
    vase.position.set(1.40, 0.87, 2.10);
    diningGroup.add(vase);

    createBlobShadow(1.20, 1.30, 1.40, 2.10, diningGroup, 0.42);
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

c = c[:idx_l1] + new_living_code + "\n" + c[idx_l2:]

# -----------------------------------------------------------------------------
# 5. CALIBRATE STOP 2 CAMERA WAYPOINTS FOR BALANCED COMPOSITION
# -----------------------------------------------------------------------------
old_leg2 = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
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

new_leg2 = """// --- STOP 2: 22% to 38% (Walk into Living & Dining Sanctuary) ---
// Leg 2A (22% to 30%): Step through front door into Living Sanctuary
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.5,
    sweepLivingZ: -1.15,
    posX: 0.88,
    posY: 1.48,
    posZ: 2.22,
    targetX: 1.58,
    targetY: 1.10,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'power2.inOut'
});
// Leg 2B (30% to 38%): Living Sanctuary Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 63.5,
    sweepLivingZ: -1.15,
    posX: 0.88,
    posY: 1.48,
    posZ: 2.22,
    targetX: 1.58,
    targetY: 1.10,
    targetZ: 0.55,
    duration: 0.08,
    ease: 'none'
});"""

assert old_leg2 in c, "old_leg2 not found in script.js"
c = c.replace(old_leg2, new_leg2)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied perfect Living Sanctuary Overhaul to script.js!")
