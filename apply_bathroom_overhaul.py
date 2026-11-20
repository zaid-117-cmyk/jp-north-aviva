import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# -----------------------------------------------------------------------------
# 1. UPGRADE TRAVERTINE WALL TILE & ADD ANTI-SKID STONE FLOOR TILE TEXTURES
# -----------------------------------------------------------------------------
trav_start = "function createTravertineTileTexture() {"
trav_end = "const travertineTileTex = createTravertineTileTexture();"

idx_t1 = c.find(trav_start)
idx_t2 = c.find(trav_end)
assert idx_t1 != -1 and idx_t2 != -1, "createTravertineTileTexture not found"

new_tiles_code = """// G3. Italian Large-Format Beige Travertine 600x1200mm Bathroom Wall Tile Texture
function createTravertineTileTexture() {
    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 1024;
    const ctx = c.getContext('2d');

    // Warm beige / travertine porcelain limestone background
    ctx.fillStyle = '#EAE3D6';
    ctx.fillRect(0, 0, 1024, 1024);

    // Subtle stone sedimentary veining and mineral striations
    for (let i = 0; i < 55; i++) {
        ctx.strokeStyle = `rgba(180, 168, 150, ${0.07 + Math.random() * 0.09})`;
        ctx.lineWidth = 1.2 + Math.random() * 4.0;
        ctx.beginPath();
        let vy = Math.random() * 1024;
        ctx.moveTo(0, vy);
        for (let vx = 40; vx <= 1024; vx += 40) {
            vy += (Math.random() - 0.5) * 12;
            ctx.lineTo(vx, vy);
        }
        ctx.stroke();
    }

    // Micro-porous travertine texture specks
    for (let i = 0; i < 6000; i++) {
        const px = Math.random() * 1024;
        const py = Math.random() * 1024;
        ctx.fillStyle = `rgba(165, 152, 136, ${Math.random() * 0.06})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Large-format 600x1200mm tile grid with crisp 2mm warm-gray grout lines
    ctx.strokeStyle = '#B6ADA0';
    ctx.lineWidth = 2.5;

    // Horizontal grout lines
    for (let y = 0; y <= 1024; y += 256) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke();
    }
    // Vertical staggered grout lines (staggered every second row)
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
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const travertineTileTex = createTravertineTileTexture();

// G3-B. Travertine Recessed Grout Bump Map
function createTravertineBumpTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#808080';
    ctx.fillRect(0, 0, 512, 512);

    // Subtle tile surface grain
    for (let i = 0; i < 2000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 512;
        ctx.fillStyle = `rgba(140, 140, 140, ${Math.random() * 0.12})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // Recessed dark grout channels
    ctx.strokeStyle = '#222222';
    ctx.lineWidth = 2.0;
    for (let y = 0; y <= 512; y += 128) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(512, y); ctx.stroke();
    }
    for (let row = 0; row < 4; row++) {
        const yTop = row * 128;
        const offset = (row % 2) * 128;
        for (let x = offset; x <= 512; x += 256) {
            ctx.beginPath(); ctx.moveTo(x, yTop); ctx.lineTo(x, yTop + 128); ctx.stroke();
        }
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 2);
    return tex;
}
const travertineTileBumpTex = createTravertineBumpTexture();

// G3-C. Anti-Skid Textured Stone Bathroom Floor Tile Texture (300x300mm Grid)
function createAntiSkidFloorTexture() {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Charcoal basalt stone body
    ctx.fillStyle = '#32353A';
    ctx.fillRect(0, 0, 512, 512);

    // Flamed / textured anti-skid stipple grain
    for (let i = 0; i < 12000; i++) {
        const px = Math.random() * 512;
        const py = Math.random() * 512;
        const val = Math.floor(40 + Math.random() * 35);
        ctx.fillStyle = `rgb(${val},${val + 2},${val + 5})`;
        ctx.fillRect(px, py, 2, 2);
    }

    // 300x300mm square anti-skid tile grid with crisp dark recessed grout
    ctx.strokeStyle = '#1A1C1F';
    ctx.lineWidth = 3.0;
    for (let y = 0; y <= 512; y += 128) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(512, y); ctx.stroke();
    }
    for (let x = 0; x <= 512; x += 128) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 512); ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(3, 3);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const antiSkidFloorTex = createAntiSkidFloorTexture();"""

c = c[:idx_t1] + new_tiles_code + c[idx_t2 + len(trav_end):]

# -----------------------------------------------------------------------------
# 2. ADD & ENHANCE CURATED SANITARYWARE MATERIALS
# -----------------------------------------------------------------------------
mat_target = "const pbrTravertineTile = new THREE.MeshPhysicalMaterial({\n"
assert mat_target in c, "pbrTravertineTile marker not found"

new_materials = """// Glossy Vitreous China Porcelain for Sculpted Commode & Vessel Basin
const pbrGlossyPorcelain = new THREE.MeshPhysicalMaterial({
    color: 0xFCFCFC,
    roughness: 0.08,
    metalness: 0.02,
    clearcoat: 0.85,
    clearcoatRoughness: 0.04,
    reflectivity: 0.90,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Anti-Skid Textured Stone Floor Tiles
const pbrAntiSkidFloorTile = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: antiSkidFloorTex,
    bumpMap: antiSkidFloorTex,
    bumpScale: 0.010,
    roughness: 0.85,
    metalness: 0.04,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Plush Folded Luxury Cotton Bath Towel
const pbrPlushTowel = new THREE.MeshPhysicalMaterial({
    color: 0xF7F4EE,
    bumpMap: boucleTex,
    bumpScale: 0.018,
    roughness: 0.94,
    sheen: 0.50,
    sheenColor: new THREE.Color(0xFFFFFF),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

"""

# Also update pbrTravertineTile definition to use bumpMap & realistic clearcoat
old_pbr_trav = """const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
    color: 0xF3EFEA,
    map: travertineTileTex,
    roughness: 0.32,
    metalness: 0.02,
    clearcoat: 0.45,
    clearcoatRoughness: 0.18,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

new_pbr_trav = """const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
    color: 0xEAE3D8,
    map: travertineTileTex,
    bumpMap: travertineTileBumpTex,
    bumpScale: 0.005,
    roughness: 0.36,
    metalness: 0.02,
    clearcoat: 0.25,
    clearcoatRoughness: 0.20,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

c = c.replace(mat_target, new_materials + mat_target)
assert old_pbr_trav in c, "old_pbr_trav not found"
c = c.replace(old_pbr_trav, new_pbr_trav)

# -----------------------------------------------------------------------------
# 3. REBUILD buildBathroomSuite() WITH SCULPTED WC, COMPLETE SHOWER & FLUTED VANITY
# -----------------------------------------------------------------------------
bath_start = "// ============================================================================\n// C. DESIGNER BATH SUITE (PORCELAIN TILES, SOFT HALO MIRROR & SHOWER GLASS)\n// ============================================================================"
bath_end = "// ============================================================================\n// D. MASTER BEDROOM SUITE"

idx_b1 = c.find(bath_start)
idx_b2 = c.find(bath_end)
assert idx_b1 != -1 and idx_b2 != -1, "bath suite section not found"

new_bath_code = """// ============================================================================
// C. DESIGNER BATH SUITE (SCULPTED SANITARYWARE & REALISTIC TILES)
// Dimensions: 1.15M x 1.30M (3'9" x 4'3" FT)
// ============================================================================
function buildBathroomSuite() {
    const group = new THREE.Group();

    // -------------------------------------------------------------------------
    // 1. ANTI-SKID STONE TILES ON FLOOR (1.15m x 1.30m)
    // -------------------------------------------------------------------------
    const bathFloorGeo = new THREE.PlaneGeometry(1.24, 1.32);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrAntiSkidFloorTile);
    bathFloor.position.set(-1.18, 0.003, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // -------------------------------------------------------------------------
    // 2. LARGE-FORMAT BEIGE TRAVERTINE PORCELAIN TILES ACROSS ALL BATHROOM WALLS
    // -------------------------------------------------------------------------
    // A. South Wet Wall behind vanity, WC & mirror (z = 1.615)
    const wetWallGeo = new THREE.PlaneGeometry(1.24, WALL_H);
    const wetWallMesh = new THREE.Mesh(wetWallGeo, pbrTravertineTile);
    wetWallMesh.position.set(-1.18, WALL_H / 2, 1.615);
    wetWallMesh.receiveShadow = true;
    group.add(wetWallMesh);

    // B. West Shower Wet Wall (x = -1.745, runs along z from 0.35 to 1.62)
    const showerWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    showerWallGeo.rotateY(Math.PI / 2);
    const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);
    showerWallMesh.position.set(-1.745, WALL_H / 2, 0.985);
    showerWallMesh.receiveShadow = true;
    group.add(showerWallMesh);

    // C. East Partition Wall (x = -0.635, facing into bathroom)
    const eastWallGeo = new THREE.PlaneGeometry(1.28, WALL_H);
    eastWallGeo.rotateY(-Math.PI / 2);
    const eastWallMesh = new THREE.Mesh(eastWallGeo, pbrTravertineTile);
    eastWallMesh.position.set(-0.635, WALL_H / 2, 0.985);
    eastWallMesh.receiveShadow = true;
    group.add(eastWallMesh);

    // D. North Doorway Wall Segments (z = 0.355, facing into bathroom)
    const northWestGeo = new THREE.PlaneGeometry(0.24, WALL_H);
    const northWestMesh = new THREE.Mesh(northWestGeo, pbrTravertineTile);
    northWestMesh.position.set(-1.62, WALL_H / 2, 0.355);
    group.add(northWestMesh);

    const northLintelGeo = new THREE.PlaneGeometry(1.00, 0.75);
    const northLintelMesh = new THREE.Mesh(northLintelGeo, pbrTravertineTile);
    northLintelMesh.position.set(-1.15, WALL_H - 0.375, 0.355);
    group.add(northLintelMesh);

    // -------------------------------------------------------------------------
    // 3. SCULPTED WALL-HUNG WC (COMMODE) & DUAL-FLUSH ACTUATOR (LEFT SIDE: X = -0.74)
    // - Curved ceramic bowl (cantilevered 16cm above floor, clearcoat: 0.85, roughness: 0.08)
    // - Contoured soft-close seat & lid with stainless steel hinge discs
    // - Brushed chrome dual-flush actuator plate with split buttons
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const wcX = -0.74;
    const wcZ = 1.34;

    // A. Rear Wall Cantilever Mounting Shroud (flush against tiled wall z = 1.615)
    const wcShroud = new THREE.Mesh(
        new RoundedBoxGeometry(0.35, 0.26, 0.18, 6, 0.03),
        pbrGlossyPorcelain
    );
    wcShroud.position.set(wcX, 0.31, 1.52);
    wcShroud.castShadow = true;
    toiletGroup.add(wcShroud);

    // B. Main Ergonomic Curved Ceramic Bowl (cantilevered floating underside at y = 0.16m)
    const wcBowl = new THREE.Mesh(
        new RoundedBoxGeometry(0.35, 0.24, 0.38, 8, 0.06),
        pbrGlossyPorcelain
    );
    wcBowl.position.set(wcX, 0.30, 1.28);
    wcBowl.castShadow = true;
    toiletGroup.add(wcBowl);

    // Contoured underside taper (gives realistic curved bell silhouette)
    const wcTaper = new THREE.Mesh(
        new THREE.CylinderGeometry(0.17, 0.10, 0.16, 24),
        pbrGlossyPorcelain
    );
    wcTaper.position.set(wcX, 0.22, 1.28);
    wcTaper.castShadow = true;
    toiletGroup.add(wcTaper);

    // C. Contoured Soft-Close Seat Ring with Beveled Rim
    const wcSeatRing = new THREE.Mesh(
        new RoundedBoxGeometry(0.35, 0.022, 0.44, 6, 0.015),
        pbrGlossyPorcelain
    );
    wcSeatRing.position.set(wcX, 0.425, 1.30);
    wcSeatRing.castShadow = true;
    toiletGroup.add(wcSeatRing);

    // D. Matching Slim Soft-Close Lid
    const wcLid = new THREE.Mesh(
        new RoundedBoxGeometry(0.34, 0.014, 0.43, 6, 0.012),
        pbrGlossyPorcelain
    );
    wcLid.position.set(wcX, 0.443, 1.30);
    wcLid.castShadow = true;
    toiletGroup.add(wcLid);

    // E. Stainless Steel Soft-Close Hinge Discs
    for (let hx of [-0.07, 0.07]) {
        const hinge = new THREE.Mesh(
            new THREE.CylinderGeometry(0.012, 0.012, 0.014, 16),
            pbrPolishedChrome
        );
        hinge.position.set(wcX + hx, 0.44, 1.50);
        toiletGroup.add(hinge);
    }

    // F. Brushed-Chrome Dual-Flush Actuator Plate on Wall
    const flushPlateX = wcX;
    const flushPlateY = 0.98;
    const flushPlateZ = 1.614;

    const flushPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.22, 0.14, 0.008, 4, 0.003),
        pbrPolishedChrome
    );
    flushPlate.position.set(flushPlateX, flushPlateY, flushPlateZ);
    toiletGroup.add(flushPlate);

    // Dual split-flush actuator buttons (Large full flush + Small eco flush)
    const btnFull = new THREE.Mesh(
        new RoundedBoxGeometry(0.08, 0.075, 0.005, 3, 0.002),
        pbrBrushedSteel
    );
    btnFull.position.set(flushPlateX - 0.046, flushPlateY, flushPlateZ + 0.005);
    toiletGroup.add(btnFull);

    const btnEco = new THREE.Mesh(
        new RoundedBoxGeometry(0.055, 0.075, 0.005, 3, 0.002),
        pbrBrushedSteel
    );
    btnEco.position.set(flushPlateX + 0.046, flushPlateY, flushPlateZ + 0.005);
    toiletGroup.add(btnEco);

    // Soft grounded contact shadow beneath cantilevered commode
    createBlobShadow(0.42, 0.52, wcX, wcZ, toiletGroup, 0.38);
    group.add(toiletGroup);

    // -------------------------------------------------------------------------
    // 4. FLOATING DARK-WALNUT FLUTED VANITY & PLUSH COTTON BATH TOWEL (CENTER: X = -1.14)
    // - Dark-walnut fluted vanity drawer with top lip pull
    // - Honed Calacatta white marble countertop with vessel basin
    // - Curved matte-black mixer tap & gold-backlit circular halo mirror
    // - Plush folded cotton bath towel with textured weave
    // -------------------------------------------------------------------------
    const vanityGroup = new THREE.Group();
    const vX = -1.14;
    const vY = 0.52;
    const vZ = 1.44;

    // A. Smoked Walnut Carcass Frame
    const vCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, 0.30, 0.34, 4, 0.012),
        pbrFlutedWalnut
    );
    vCarcass.position.set(vX, vY, vZ);
    vCarcass.castShadow = true;
    vanityGroup.add(vCarcass);

    // B. Fluted Dark-Walnut Drawer Front with crisp 8mm shadow reveals
    const vDrawer = new THREE.Mesh(
        new RoundedBoxGeometry(0.385, 0.26, 0.016, 4, 0.004),
        pbrFlutedWalnut
    );
    vDrawer.position.set(vX, vY - 0.005, vZ - 0.174);
    vDrawer.castShadow = true;
    vanityGroup.add(vDrawer);

    // Slim horizontal brushed-brass lip pull handle along top drawer edge
    const vHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.010, 0.014, 2, 0.002),
        pbrBrushedBrass
    );
    vHandle.position.set(vX, vY + 0.122, vZ - 0.176);
    vanityGroup.add(vHandle);

    // C. Honed Calacatta White Marble Countertop Slab
    const vCounter = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, 0.035, 0.37, 4, 0.010),
        pbrMarbleTable
    );
    vCounter.position.set(vX, vY + 0.165, vZ);
    vCounter.castShadow = true;
    vCounter.receiveShadow = true;
    vanityGroup.add(vCounter);

    // D. White Glossy Ceramic Vessel Basin
    const basin = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.10, 0.09, 32),
        pbrGlossyPorcelain
    );
    basin.position.set(vX, vY + 0.225, vZ - 0.01);
    basin.castShadow = true;
    vanityGroup.add(basin);

    // Chrome pop-up drain stopper & water reflection inside basin
    const basinDrain = new THREE.Mesh(
        new THREE.CylinderGeometry(0.018, 0.018, 0.004, 16),
        pbrPolishedChrome
    );
    basinDrain.position.set(vX, vY + 0.19, vZ - 0.01);
    vanityGroup.add(basinDrain);

    const basinWater = new THREE.Mesh(
        new THREE.CylinderGeometry(0.10, 0.10, 0.002, 24),
        pbrSinkWater
    );
    basinWater.position.set(vX, vY + 0.20, vZ - 0.01);
    vanityGroup.add(basinWater);

    // E. Curved Matte-Black Gooseneck Mixer Tap (TubeGeometry arch)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.017, 0.012, 20), pbrMatteBlackSteel);
    tapBase.position.set(vX, vY + 0.185, vZ + 0.11);
    tapGroup.add(tapBase);

    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.12, 0),
        new THREE.Vector3(0, 0.18, -0.02),
        new THREE.Vector3(0, 0.20, -0.07),
        new THREE.Vector3(0, 0.18, -0.11),
        new THREE.Vector3(0, 0.13, -0.12)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.0055, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(vX, vY + 0.19, vZ + 0.11);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.005, 0.012, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(vX, vY + 0.32, vZ - 0.01);
    tapGroup.add(tapNozzle);

    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.018, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(vX + 0.022, vY + 0.25, vZ + 0.11);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.050, 12), pbrMatteBlackSteel);
    pinLever.position.set(vX + 0.032, vY + 0.275, vZ + 0.11);
    pinLever.rotation.z = -0.40;
    tapGroup.add(pinLever);
    vanityGroup.add(tapGroup);

    // F. Circular Gold-Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm Halo
    const mirrorGlass = new THREE.Mesh(
        new THREE.CylinderGeometry(0.24, 0.24, 0.008, 64),
        new THREE.MeshPhysicalMaterial({
            color: 0xFFFFFF,
            roughness: 0.01,
            metalness: 0.99,
            clearcoat: 1.0,
            clippingPlanes: [clipHeightPlane]
        })
    );
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(vX, 1.35, 1.59);
    vanityGroup.add(mirrorGlass);

    const brassFrameGeo = new THREE.TorusGeometry(0.243, 0.005, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(vX, 1.35, 1.585);
    vanityGroup.add(brassFrameMesh);

    const haloRingGeo = new THREE.TorusGeometry(0.255, 0.010, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloRingMesh);

    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.35, 2.2, 1.8);
    haloWallLight.position.set(vX, 1.35, 1.605);
    vanityGroup.add(haloWallLight);

    // G. Plush Folded Cotton Bath Towel on Vanity Counter
    const towelFold1 = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.024, 0.15, 6, 0.010),
        pbrPlushTowel
    );
    towelFold1.position.set(vX + 0.13, vY + 0.195, vZ - 0.03);
    towelFold1.castShadow = true;
    vanityGroup.add(towelFold1);

    const towelFold2 = new THREE.Mesh(
        new RoundedBoxGeometry(0.11, 0.022, 0.14, 6, 0.009),
        pbrPlushTowel
    );
    towelFold2.position.set(vX + 0.13, vY + 0.220, vZ - 0.03);
    towelFold2.rotation.y = 0.06;
    towelFold2.castShadow = true;
    vanityGroup.add(towelFold2);

    // Amber Glass Hand Wash Pump Bottle
    const soapBottle = new THREE.Mesh(
        new RoundedBoxGeometry(0.045, 0.085, 0.045, 4, 0.010),
        pbrAmberGlass
    );
    soapBottle.position.set(vX - 0.14, vY + 0.225, vZ - 0.04);
    soapBottle.castShadow = true;
    vanityGroup.add(soapBottle);

    const soapPump = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.022, 12),
        pbrMatteBlackSteel
    );
    soapPump.position.set(vX - 0.14, vY + 0.280, vZ - 0.04);
    vanityGroup.add(soapPump);

    createBlobShadow(0.46, 0.40, vX, vZ, vanityGroup, 0.40);
    group.add(vanityGroup);

    // -------------------------------------------------------------------------
    // 5. COMPLETE WET-ZONE SHOWER ENCLOSURE (RIGHT SIDE: X = -1.40 to -1.745)
    // - Frameless tempered glass partition (1.95m high)
    // - Matte-black overhead square rain showerhead (TubeGeometry wall arm)
    // - Thermostatic mixer valve plate + handheld shower wand & flexible hose
    // - Recessed tiled shampoo niche with realistic amber glass bottles
    // - Brushed-steel linear floor drain
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();
    const glassX = -1.40;

    // A. 10mm Frameless Architectural Shower Glass Partition (z = 0.50 to 1.55)
    const showerGlass = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 1.95, 1.05),
        pbrShowerGlass
    );
    showerGlass.position.set(glassX, 0.975, 1.025);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim matte-black floor mounting U-channel & wall bracket
    const floorChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.016, 1.05),
        pbrMatteBlackSteel
    );
    floorChannel.position.set(glassX, 0.008, 1.025);
    showerGroup.add(floorChannel);

    const topChannel = new THREE.Mesh(
        new THREE.BoxGeometry(0.018, 0.018, 1.05),
        pbrMatteBlackSteel
    );
    topChannel.position.set(glassX, 1.95, 1.025);
    showerGroup.add(topChannel);

    // Top horizontal stabilizing tie bar anchored from west wall (x = -1.745) to glass (x = -1.40)
    const tieBar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.006, 0.006, 0.35, 12),
        pbrMatteBlackSteel
    );
    tieBar.rotation.z = Math.PI / 2;
    tieBar.position.set(-1.57, 1.92, 1.15);
    showerGroup.add(tieBar);

    // B. Matte-Black Overhead Square Rain Showerhead (TubeGeometry Wall Arm)
    // Curved wall arm starting from west wall (x = -1.745, y = 2.10, z = 1.15)
    const armCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.745, 2.10, 1.15),
        new THREE.Vector3(-1.620, 2.10, 1.15),
        new THREE.Vector3(-1.550, 2.08, 1.15),
        new THREE.Vector3(-1.540, 2.02, 1.15),
        new THREE.Vector3(-1.540, 1.96, 1.15)
    ]);
    const armGeo = new THREE.TubeGeometry(armCurve, 32, 0.009, 16, false);
    const armMesh = new THREE.Mesh(armGeo, pbrMatteBlackSteel);
    armMesh.castShadow = true;
    showerGroup.add(armMesh);

    // Square wall flange escutcheon
    const armFlange = new THREE.Mesh(
        new THREE.BoxGeometry(0.010, 0.065, 0.065),
        pbrMatteBlackSteel
    );
    armFlange.position.set(-1.740, 2.10, 1.15);
    showerGroup.add(armFlange);

    // 240mm Ultra-Slim Square Matte-Black Rain Showerhead Plate
    const rainPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.24, 0.012, 0.24, 4, 0.004),
        pbrMatteBlackSteel
    );
    rainPlate.position.set(-1.54, 1.94, 1.15);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    // Swivel ball joint collar
    const swivelJoint = new THREE.Mesh(
        new THREE.CylinderGeometry(0.014, 0.014, 0.024, 16),
        pbrMatteBlackSteel
    );
    swivelJoint.position.set(-1.54, 1.96, 1.15);
    showerGroup.add(swivelJoint);

    // C. Thermostatic Mixer Valve + Handheld Wand on West Wall (x = -1.74)
    // Concealed Thermostatic Valve Trim Plate
    const thermoPlate = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.28, 0.11, 4, 0.003),
        pbrMatteBlackSteel
    );
    thermoPlate.position.set(-1.738, 1.05, 1.15);
    showerGroup.add(thermoPlate);

    // 2 Knurled Cylindrical Thermostatic Control Dials
    for (let dy of [1.12, 0.98]) {
        const dial = new THREE.Mesh(
            new THREE.CylinderGeometry(0.020, 0.020, 0.024, 20),
            pbrMatteBlackSteel
        );
        dial.rotation.z = Math.PI / 2;
        dial.position.set(-1.725, dy, 1.15);
        showerGroup.add(dial);
    }

    // Cylindrical Hand Shower Slide Rail on West Wall
    const slideRail = new THREE.Mesh(
        new THREE.CylinderGeometry(0.007, 0.007, 0.65, 16),
        pbrMatteBlackSteel
    );
    slideRail.position.set(-1.735, 1.25, 0.95);
    showerGroup.add(slideRail);

    // Handheld Shower Wand docked in bracket
    const handWand = new THREE.Mesh(
        new THREE.CylinderGeometry(0.009, 0.007, 0.20, 16),
        pbrMatteBlackSteel
    );
    handWand.position.set(-1.722, 1.35, 0.95);
    showerGroup.add(handWand);

    // Flexible Braided Shower Hose (CatmullRomCurve3 hanging naturally in catenary loop)
    const hoseCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-1.722, 1.25, 0.95),
        new THREE.Vector3(-1.722, 0.95, 0.98),
        new THREE.Vector3(-1.722, 0.85, 1.08),
        new THREE.Vector3(-1.735, 0.90, 1.15)
    ]);
    const hoseGeo = new THREE.TubeGeometry(hoseCurve, 32, 0.005, 12, false);
    const hoseMesh = new THREE.Mesh(hoseGeo, pbrMatteBlackSteel);
    showerGroup.add(hoseMesh);

    // D. Recessed Tiled Shampoo Niche with Realistic Amber Glass Bottles
    // Recessed into West Wall (z = 1.25 to 1.55, y = 1.15 to 1.48)
    const nicheFrame = new THREE.Mesh(
        new RoundedBoxGeometry(0.024, 0.32, 0.32, 4, 0.004),
        pbrTravertineTile
    );
    nicheFrame.position.set(-1.738, 1.32, 1.40);
    showerGroup.add(nicheFrame);

    const nicheBack = new THREE.Mesh(
        new THREE.PlaneGeometry(0.30, 0.30),
        pbrTravertineTile
    );
    nicheBack.rotateY(Math.PI / 2);
    nicheBack.position.set(-1.748, 1.32, 1.40);
    showerGroup.add(nicheBack);

    // Concealed warm LED accent light washing down niche
    const nicheLight = new THREE.PointLight(0xFFE4B5, 0.95, 1.4, 2.0);
    nicheLight.position.set(-1.72, 1.44, 1.40);
    showerGroup.add(nicheLight);

    // 3 Realistic Amber Glass Soap Bottles in Niche with Chrome Dispenser Pumps
    const bottles = [
        { z: 1.31, h: 0.10, w: 0.046, pumpColor: pbrMatteBlackSteel },
        { z: 1.40, h: 0.09, w: 0.042, pumpColor: pbrBrushedBrass },
        { z: 1.48, h: 0.08, w: 0.038, pumpColor: pbrMatteBlackSteel }
    ];
    bottles.forEach(b => {
        const bot = new THREE.Mesh(
            new RoundedBoxGeometry(0.042, b.h, b.w, 4, 0.008),
            pbrAmberGlass
        );
        bot.position.set(-1.722, 1.18 + b.h / 2, b.z);
        bot.castShadow = true;
        showerGroup.add(bot);

        const pump = new THREE.Mesh(
            new THREE.CylinderGeometry(0.005, 0.005, 0.020, 12),
            b.pumpColor
        );
        pump.position.set(-1.722, 1.18 + b.h + 0.010, b.z);
        showerGroup.add(pump);
    });

    // E. Brushed-Steel Linear Floor Drain in Shower Floor
    const drainMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.065, 0.004, 0.58),
        pbrBrushedSteel
    );
    drainMesh.position.set(-1.57, 0.005, 1.05);
    showerGroup.add(drainMesh);

    // Subtle laser grate slots on linear drain
    for (let s = -0.24; s <= 0.24; s += 0.04) {
        const slot = new THREE.Mesh(
            new THREE.BoxGeometry(0.038, 0.005, 0.008),
            pbrMatteBlackSteel
        );
        slot.position.set(-1.57, 0.006, 1.05 + s);
        showerGroup.add(slot);
    }

    group.add(showerGroup);

    // -------------------------------------------------------------------------
    // 6. OVERHEAD CEILING DOWNLIGHT
    // -------------------------------------------------------------------------
    const bathDownlight = new THREE.PointLight(0xFFF2DC, 1.2, 3.0, 1.8);
    bathDownlight.position.set(-1.14, 2.75, 1.05);
    group.add(bathDownlight);

    materialGroup.add(group);
}
"""

c = c[:idx_b1] + new_bath_code + "\n" + c[idx_b2:]

# -----------------------------------------------------------------------------
# 4. CALIBRATE STOP 4 CAMERA WAYPOINTS TO SHOWCASE FULL BATH & W.C. COMPOSITION
# -----------------------------------------------------------------------------
old_leg4 = """// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.15,
    posY: 1.50,
    posZ: -0.15,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.40,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.48,
    posZ: -0.05,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.48,
    posZ: -0.05,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});"""

new_leg4 = """// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -1.14,
    posY: 1.52,
    posZ: -0.22,
    targetX: -1.14,
    targetY: 1.14,
    targetZ: 1.40,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Settle at Bathroom Doorway threshold with wide architectural framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.16,
    targetX: -1.14,
    targetY: 1.12,
    targetZ: 1.42,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): BATH & W.C. Steady Hold (Full Architecture Composition: Vanity, WC & Shower Glass)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.5,
    sweepBathroomZ: 0.40,
    posX: -1.14,
    posY: 1.50,
    posZ: -0.16,
    targetX: -1.14,
    targetY: 1.12,
    targetZ: 1.42,
    duration: 0.05,
    ease: 'none'
});"""

assert old_leg4 in c, "old_leg4 not found in script.js"
c = c.replace(old_leg4, new_leg4)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied Sculpted Bathroom Suite Overhaul to script.js!")
