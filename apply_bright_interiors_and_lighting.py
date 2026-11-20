import os
import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Section 3: PMREM Neutral-Warm Environment Map & SSAO config
old_sec3_start = "// ----------------------------------------------------------------------------\n// 3. IMAGE-BASED LIGHTING (IBL) & ROOM ENVIRONMENT"
old_sec5_start = "// ----------------------------------------------------------------------------\n// 5. ARCHITECTURAL CLIPPING PLANES (PENCIL TO REALITY SYSTEM)"

idx_sec3 = code.find(old_sec3_start)
idx_sec5 = code.find(old_sec5_start)

if idx_sec3 == -1 or idx_sec5 == -1:
    raise ValueError(f"Could not find section 3 or 5: idx_sec3={idx_sec3}, idx_sec5={idx_sec5}")

new_sec3_and_4 = r'''// ----------------------------------------------------------------------------
// 3. NEUTRAL-WARM PMREM GENERATOR ENVIRONMENT MAP FOR REALISTIC REFLECTIONS
// ----------------------------------------------------------------------------
function createNeutralWarmEnvironment(renderer) {
    const pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();

    const c = document.createElement('canvas');
    c.width = 1024;
    c.height = 512;
    const ctx = c.getContext('2d');

    // Smooth architectural neutral-warm sky / interior reflection gradient
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0.0, '#FFF7F0'); // Zenith warm soft cream
    grad.addColorStop(0.35, '#FFEEDA'); // Upper horizon
    grad.addColorStop(0.50, '#FFD9B3'); // Mumbai golden hour horizon sunset band
    grad.addColorStop(0.65, '#C8B6A4'); // Warm stone floor bounce
    grad.addColorStop(1.0, '#8E7D6F');  // Ground warm taupe
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 1024, 512);

    // Subtle warm sun highlight in the environment
    const sunGrad = ctx.createRadialGradient(680, 220, 10, 680, 220, 200);
    sunGrad.addColorStop(0, 'rgba(255, 238, 200, 0.95)');
    sunGrad.addColorStop(0.3, 'rgba(255, 205, 150, 0.55)');
    sunGrad.addColorStop(1, 'rgba(255, 205, 150, 0)');
    ctx.fillStyle = sunGrad;
    ctx.fillRect(0, 0, 1024, 512);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    const envTexture = pmrem.fromEquirectangular(tex).texture;
    pmrem.dispose();
    tex.dispose();
    return envTexture;
}

const envMap = createNeutralWarmEnvironment(renderer);
scene.environment = envMap;
scene.environmentIntensity = 0.95;

// ----------------------------------------------------------------------------
// 4. POST-PROCESSING COMPOSER & SSAO PASS FOR GROUNDED CONTACT SHADOWS
// ----------------------------------------------------------------------------
const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Screen Space Ambient Occlusion (SSAO) for deep grounded contact shadows under furniture & corners
const ssaoPass = new SSAOPass(
    scene,
    camera,
    window.innerWidth,
    window.innerHeight
);
ssaoPass.kernelRadius = 0.38;
ssaoPass.minDistance = 0.002;
ssaoPass.maxDistance = 0.22;
ssaoPass.output = SSAOPass.OUTPUT.Default;
composer.addPass(ssaoPass);

const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.14, // strength
    0.35, // radius
    0.88  // threshold
);
composer.addPass(bloomPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);
'''

code = code[:idx_sec3] + new_sec3_and_4.strip() + "\n\n" + code[idx_sec5:]

# 2. Update Wall Materials in Section 7
old_mat_start = "const pbrWhisperingSmoke = new THREE.MeshPhysicalMaterial({"
old_mat_end = "const pbrBaseboard = new THREE.MeshPhysicalMaterial({"

idx_mat_start = code.find(old_mat_start)
idx_mat_end = code.find(old_mat_end)

if idx_mat_start == -1 or idx_mat_end == -1:
    raise ValueError("Could not find pbrWhisperingSmoke or pbrBaseboard")

new_materials = r'''// Warm off-white matte plaster / eggshell paint (#EAE6DF, roughness: 0.85, metalness: 0.0)
const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xEAE6DF,
    roughness: 0.85,
    metalness: 0.0,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.003,
    reflectivity: 0.20,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide
});

const pbrWhisperingSmoke = pbrWarmPlasterWall;

const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane]
});
'''

code = code[:idx_mat_start] + new_materials.strip() + "\n\n" + code[idx_mat_start:]

# Also update pbrCeilingMat to be double sided
code = code.replace(
    """const pbrCeilingMat = new THREE.MeshPhysicalMaterial({\n    color: 0xFAF8F5,\n    roughness: 0.92,\n    metalness: 0.0,\n    clippingPlanes: [clipHeightPlane]\n});""",
    """const pbrCeilingMat = new THREE.MeshPhysicalMaterial({\n    color: 0xFAF8F5,\n    roughness: 0.88,\n    metalness: 0.0,\n    clippingPlanes: [clipHeightPlane],\n    side: THREE.DoubleSide\n});"""
)

# 3. Update Section 9: addWall default material, 10cm MDF Skirting along ALL floor junctions,
# and Ceilings & Recessed Cove Lighting (#FFE4B5)
old_sec9_start = "// ----------------------------------------------------------------------------\n// 9. SOLID ARCHITECTURAL WALLS & STRUCTURE (2.85M ENCLOSED RESIDENCE)"
old_sec10_start = "// ----------------------------------------------------------------------------\n// 10. HIGH-END PHOTOREALISTIC APPLIANCES & FURNITURE ASSEMBLIES"

idx_sec9 = code.find(old_sec9_start)
idx_sec10 = code.find(old_sec10_start)

if idx_sec9 == -1 or idx_sec10 == -1:
    raise ValueError("Could not find section 9 or 10")

new_sec9 = r'''// ----------------------------------------------------------------------------
// 9. SOLID ARCHITECTURAL WALLS, SKIRTING & RECESSED COVE CEILINGS
// ----------------------------------------------------------------------------
const WALL_H = 2.85;
const wallGroup = new THREE.Group();
const materialGroup = new THREE.Group();
scene.add(wallGroup);
scene.add(materialGroup);

function addWall(w, h, d, x, y, z, customPbrMat = pbrWarmPlasterWall) {
    // Draft mesh (Stop 0 Blueprint only)
    const draftGeo = new THREE.BoxGeometry(w, h, d);
    const draftMesh = new THREE.Mesh(draftGeo, draftWallMat);
    draftMesh.position.set(x, y, z);
    draftMesh.castShadow = true;
    draftMesh.receiveShadow = true;
    wallGroup.add(draftMesh);

    // Warm Off-White Matte Plaster PBR Material mesh (Stop 1 to 7)
    const pbrMesh = new THREE.Mesh(draftGeo, customPbrMat);
    pbrMesh.position.set(x, y, z);
    pbrMesh.castShadow = true;
    pbrMesh.receiveShadow = true;
    materialGroup.add(pbrMesh);

    return { draftMesh, pbrMesh };
}

// 10cm Painted MDF Skirting / Baseboards along all floor junctions
function addSkirting(w, d, x, z) {
    const bbGeo = new THREE.BoxGeometry(w, 0.10, d); // Exactly 10cm height (0.10m)
    const bb = new THREE.Mesh(bbGeo, pbrMDFSkirting);
    bb.position.set(x, 0.05, z); // Sits cleanly on the floor at y=0.0
    bb.castShadow = true;
    bb.receiveShadow = true;
    materialGroup.add(bb);
    return bb;
}

// --- Outer Perimeter Walls (Warm Off-White Matte Plaster #EAE6DF) ---
addWall(0.20, WALL_H, 4.25, 3.05, WALL_H / 2, 0.825);
addWall(2.00, WALL_H, 0.20, 1.95, WALL_H / 2, 2.90);
addWall(0.20, WALL_H, 1.45, 0.10, WALL_H / 2, 2.175);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, 1.75);
addWall(0.20, WALL_H, 1.50, -1.85, WALL_H / 2, 1.10);
addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, 0.45);
addWall(0.20, WALL_H, 3.05, -4.30, WALL_H / 2, -0.975);
addWall(2.55, WALL_H, 0.20, -3.025, WALL_H / 2, -2.50);
addWall(2.05, WALL_H, 0.20, -0.825, WALL_H / 2, -2.50);

// Kitchen Shaft / Window reveal
addWall(0.20, WALL_H, 1.30, 0.10, WALL_H / 2, -1.95);
addWall(0.20, WALL_H, 1.30, -1.85, WALL_H / 2, -1.95);

// Balcony Perimeter Walls
addWall(0.20, WALL_H, 1.30, 3.05, WALL_H / 2, -1.75);
addWall(2.95, 1.10, 0.15, 1.575, 0.55, -2.425); // Balcony parapet wall
addWall(2.95, 0.45, 0.15, 1.575, WALL_H - 0.225, -2.425); // Balcony upper lintel

// Glass Railing for Balcony
const balconyGlass = new THREE.Mesh(new THREE.BoxGeometry(2.70, 1.30, 0.02), pbrGlass);
balconyGlass.position.set(1.575, 1.75, -2.425);
materialGroup.add(balconyGlass);

// Interior Partitions
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
addWall(1.80, 0.75, 0.15, 1.575, WALL_H - 0.375, -1.15); // Balcony Sliding Lintel

// --- 10cm Painted MDF Skirting / Baseboards Along ALL Floor Junctions ---
// Living & Dining Sanctuary junctions
addSkirting(0.03, 3.90, 2.93, 0.95);  // East wall
addSkirting(0.03, 2.70, 0.22, 0.55);  // West partition
addSkirting(0.95, 0.03, 2.45, 2.78);  // South entry wall
addSkirting(0.60, 0.03, 2.65, -1.05); // North wall next to slider
addSkirting(0.40, 0.03, 0.38, -0.68); // Kitchen divider base

// Kitchen Alcove perimeter junctions
addSkirting(0.03, 1.70, -1.73, -1.50); // West wall
addSkirting(1.70, 0.03, -0.90, -2.38); // North window wall
addSkirting(0.03, 1.70, 0.02, -1.50);  // East shaft wall
addSkirting(0.45, 0.03, -1.55, -0.68); // South alcove return

// Master Bedroom Suite perimeter junctions
addSkirting(0.03, 2.75, -4.18, -1.05); // West wall
addSkirting(2.20, 0.03, -3.05, -2.38); // North window wall
addSkirting(0.03, 2.20, -1.92, -1.30); // East partition
addSkirting(2.20, 0.03, -3.05, 0.28);  // South accent wall
addSkirting(1.10, 0.03, -3.65, 0.38);  // Wardrobe niche base

// Corridor & Foyer junctions
addSkirting(1.60, 0.03, -1.00, 0.42); // Bath outer wall
addSkirting(0.90, 0.03, -0.60, 1.68); // Toilet outer wall
addSkirting(0.03, 1.20, 0.02, 2.20);  // Foyer west wall

// Balcony perimeter junctions
addSkirting(0.03, 1.20, 2.93, -1.80); // East wall
addSkirting(0.03, 1.20, 0.17, -1.80); // West wall
addSkirting(2.70, 0.03, 1.55, -2.35); // Parapet inner base

// --- CEILINGS & RECESSED WARM COVE LIGHTING (#FFE4B5) ---
function buildCeilingsAndCoveLighting() {
    const group = new THREE.Group();

    // 1. Solid Main Ceiling Slab (y = WALL_H = 2.85m) covering entire apartment
    const mainCeilingGeo = new THREE.PlaneGeometry(8.5, 6.5);
    mainCeilingGeo.rotateX(Math.PI / 2);
    const mainCeiling = new THREE.Mesh(mainCeilingGeo, pbrCeilingMat);
    mainCeiling.position.set(-0.65, WALL_H, 0.20);
    mainCeiling.receiveShadow = true;
    group.add(mainCeiling);

    // Warm Emissive Cove Material (#FFE4B5)
    const coveLightMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });

    // Downlight Bezel & Lens Materials
    const downlightBezelMat = new THREE.MeshPhysicalMaterial({
        color: 0xE8E5DE,
        roughness: 0.35,
        metalness: 0.1,
        clippingPlanes: [clipHeightPlane]
    });
    const downlightLensMat = new THREE.MeshBasicMaterial({
        color: 0xFFF2DC,
        clippingPlanes: [clipHeightPlane]
    });

    function addDownlight(x, z, intensity = 1.3, distance = 4.0, lightColor = 0xFFE8C8) {
        // Outer trim ring
        const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.012, 20), downlightBezelMat);
        bezel.position.set(x, WALL_H - 0.006, z);
        group.add(bezel);

        // Glowing center lens
        const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.014, 20), downlightLensMat);
        lens.position.set(x, WALL_H - 0.007, z);
        group.add(lens);

        // Architectural PointLight with physical decay
        const light = new THREE.PointLight(lightColor, intensity, distance, 2.0);
        light.position.set(x, WALL_H - 0.08, z);
        group.add(light);
    }

    // A. LIVING ROOM CEILING TRAY & WARM COVE (#FFE4B5)
    // False ceiling dropped tray: 2.30m wide, 3.20m deep, dropped 8cm (y = 2.77)
    const lrTrayGeo = new THREE.BoxGeometry(2.30, 0.08, 3.20);
    const lrTray = new THREE.Mesh(lrTrayGeo, pbrCeilingMat);
    lrTray.position.set(1.55, WALL_H - 0.04, 0.85);
    lrTray.receiveShadow = true;
    lrTray.castShadow = true;
    group.add(lrTray);

    // Glowing LED Cove Ribbon along the perimeter
    const coveThickness = 0.02;
    const coveNorth = new THREE.Mesh(new THREE.BoxGeometry(2.32, coveThickness, 0.03), coveLightMat);
    coveNorth.position.set(1.55, WALL_H - 0.01, -0.76);
    group.add(coveNorth);

    const coveSouth = new THREE.Mesh(new THREE.BoxGeometry(2.32, coveThickness, 0.03), coveLightMat);
    coveSouth.position.set(1.55, WALL_H - 0.01, 2.46);
    group.add(coveSouth);

    const coveWest = new THREE.Mesh(new THREE.BoxGeometry(0.03, coveThickness, 3.22), coveLightMat);
    coveWest.position.set(0.39, WALL_H - 0.01, 0.85);
    group.add(coveWest);

    const coveEast = new THREE.Mesh(new THREE.BoxGeometry(0.03, coveThickness, 3.22), coveLightMat);
    coveEast.position.set(2.71, WALL_H - 0.01, 0.85);
    group.add(coveEast);

    // 4 Warm Cove Glow Lights (#FFE4B5) washing upper ceiling & walls
    const lrCoveLight1 = new THREE.PointLight(0xFFE4B5, 2.2, 4.2, 2.0);
    lrCoveLight1.position.set(1.55, WALL_H - 0.03, -0.65);
    group.add(lrCoveLight1);

    const lrCoveLight2 = new THREE.PointLight(0xFFE4B5, 2.2, 4.2, 2.0);
    lrCoveLight2.position.set(1.55, WALL_H - 0.03, 2.35);
    group.add(lrCoveLight2);

    const lrCoveLight3 = new THREE.PointLight(0xFFE4B5, 1.8, 4.0, 2.0);
    lrCoveLight3.position.set(0.48, WALL_H - 0.03, 0.85);
    group.add(lrCoveLight3);

    const lrCoveLight4 = new THREE.PointLight(0xFFE4B5, 1.8, 4.0, 2.0);
    lrCoveLight4.position.set(2.62, WALL_H - 0.03, 0.85);
    group.add(lrCoveLight4);

    // Living Room Downlights Array (6 downlights)
    addDownlight(0.95, -0.15, 1.4, 4.2);
    addDownlight(2.15, -0.15, 1.4, 4.2);
    addDownlight(0.95, 0.85, 1.4, 4.2);
    addDownlight(2.15, 0.85, 1.4, 4.2);
    addDownlight(0.95, 1.85, 1.4, 4.2);
    addDownlight(2.15, 1.85, 1.4, 4.2);

    // B. GOURMET KITCHEN ALCOVE CEILING & COVE (#FFE4B5)
    const kTrayGeo = new THREE.BoxGeometry(1.60, 0.08, 1.45);
    const kTray = new THREE.Mesh(kTrayGeo, pbrCeilingMat);
    kTray.position.set(-0.85, WALL_H - 0.04, -1.55);
    kTray.receiveShadow = true;
    group.add(kTray);

    const kCoveRibbon = new THREE.Mesh(new THREE.BoxGeometry(1.62, 0.02, 0.03), coveLightMat);
    kCoveRibbon.position.set(-0.85, WALL_H - 0.01, -0.82);
    group.add(kCoveRibbon);

    const kCoveLight = new THREE.PointLight(0xFFE4B5, 2.4, 3.8, 2.0);
    kCoveLight.position.set(-0.85, WALL_H - 0.03, -0.90);
    group.add(kCoveLight);

    // Kitchen 4 Task Downlights
    addDownlight(-0.45, -1.20, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-1.25, -1.20, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-0.45, -1.90, 1.5, 3.5, 0xFFF5E4);
    addDownlight(-1.25, -1.90, 1.5, 3.5, 0xFFF5E4);

    // C. MASTER BEDROOM CEILING TRAY & COVE (#FFE4B5)
    const brTrayGeo = new THREE.BoxGeometry(2.00, 0.08, 2.20);
    const brTray = new THREE.Mesh(brTrayGeo, pbrCeilingMat);
    brTray.position.set(-3.05, WALL_H - 0.04, -1.05);
    brTray.receiveShadow = true;
    group.add(brTray);

    const brCoveRibbonSouth = new THREE.Mesh(new THREE.BoxGeometry(2.02, 0.02, 0.03), coveLightMat);
    brCoveRibbonSouth.position.set(-3.05, WALL_H - 0.01, 0.06);
    group.add(brCoveRibbonSouth);

    const brCoveRibbonNorth = new THREE.Mesh(new THREE.BoxGeometry(2.02, 0.02, 0.03), coveLightMat);
    brCoveRibbonNorth.position.set(-3.05, WALL_H - 0.01, -2.16);
    group.add(brCoveRibbonNorth);

    const brCoveLight1 = new THREE.PointLight(0xFFE4B5, 2.0, 4.0, 2.0);
    brCoveLight1.position.set(-3.05, WALL_H - 0.03, -0.05);
    group.add(brCoveLight1);

    const brCoveLight2 = new THREE.PointLight(0xFFE4B5, 2.0, 4.0, 2.0);
    brCoveLight2.position.set(-3.05, WALL_H - 0.03, -2.05);
    group.add(brCoveLight2);

    // Bedroom Downlights (4 soft architectural downlights)
    addDownlight(-2.45, -0.55, 1.2, 3.8);
    addDownlight(-3.65, -0.55, 1.2, 3.8);
    addDownlight(-2.45, -1.55, 1.2, 3.8);
    addDownlight(-3.65, -1.55, 1.2, 3.8);

    // D. FOYER & CORRIDOR DOWNLIGHTS
    addDownlight(0.85, 2.45, 1.5, 3.5);
    addDownlight(-0.85, 0.85, 1.3, 3.5);

    materialGroup.add(group);
    return group;
}

buildCeilingsAndCoveLighting();

// Calacatta Marble Luxury Flooring
const marbleFloorGeo = new THREE.PlaneGeometry(8.5, 6.5);
marbleFloorGeo.rotateX(-Math.PI / 2);
const marbleFloor = new THREE.Mesh(marbleFloorGeo, pbrCalacattaFloor);
marbleFloor.position.set(SHEET_CX, 0.002, SHEET_CZ);
marbleFloor.receiveShadow = true;
materialGroup.add(marbleFloor);

// Front Door (Swings open 90° inward during Stop 1)
const doorPivot = new THREE.Group();
doorPivot.position.set(0.35, 0, 2.80);
const frontDoorMesh = new THREE.Mesh(new RoundedBoxGeometry(0.95, 2.10, 0.045, 4, 0.01), pbrScandinavianOak);
frontDoorMesh.position.set(0.475, 1.05, 0);
frontDoorMesh.castShadow = true;
doorPivot.add(frontDoorMesh);
// Brushed brass door handle
const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.18, 12), pbrBrushedBrass);
handle.rotation.z = Math.PI / 2;
handle.position.set(0.85, 1.05, 0.035);
doorPivot.add(handle);
materialGroup.add(doorPivot);

// Balcony Sliding Glass Door (Slides open during Stop 6)
const balconyDoorPivot = new THREE.Group();
balconyDoorPivot.position.set(1.575, 0, -1.15);
const glassSlider = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.10, 0.03), pbrGlass);
glassSlider.position.set(0.45, 1.05, 0);
balconyDoorPivot.add(glassSlider);
const sliderFrame = new THREE.Mesh(new THREE.BoxGeometry(0.04, 2.10, 0.04), pbrMatteBlackSteel);
sliderFrame.position.set(0.02, 1.05, 0);
balconyDoorPivot.add(sliderFrame);
materialGroup.add(balconyDoorPivot);
'''

code = code[:idx_sec9] + new_sec9.strip() + "\n\n" + code[idx_sec10:]

# 4. Remove duplicate downlights in buildHabitableRoom
old_hr_downlights = """    // 6. Recessed Architectural Downlights in Ceiling
    for (let rx of [0.90, 2.20]) {
        for (let rz of [-0.40, 0.60, 1.80]) {
            const spot = new THREE.PointLight(0xFFE4C4, 1.2, 4.0, 2.0);
            spot.position.set(rx, WALL_H - 0.05, rz);
            group.add(spot);
            const bezel = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.015, 16), pbrWhisperingSmoke);
            bezel.position.set(rx, WALL_H - 0.008, rz);
            group.add(bezel);
        }
    }"""
if old_hr_downlights in code:
    code = code.replace(old_hr_downlights, "    // Downlights managed in buildCeilingsAndCoveLighting")

# 5. Update Section 11: Sunlight angled through Enclosed Balcony & Master Bedroom Windows
old_sec11_start = "// ----------------------------------------------------------------------------\n// 11. LIGHTING SETUP (MUMBAI GOLDEN HOUR 3-TIER LIGHTING)"
old_sec12_start = "// ----------------------------------------------------------------------------\n// 12. CINEMATIC 55-SECOND GSAP SCROLL & PROGRESS TIMELINE"

idx_sec11 = code.find(old_sec11_start)
idx_sec12 = code.find(old_sec12_start)

if idx_sec11 == -1 or idx_sec12 == -1:
    raise ValueError("Could not find section 11 or 12")

new_sec11 = r'''// ----------------------------------------------------------------------------
// 11. LIGHTING SETUP (GOLDEN HOUR SUNLIGHT & CONTACT SHADOW CONFIGURATION)
// ----------------------------------------------------------------------------
// Soft Directional Sunlight angled directly through Enclosed Balcony and Master Bedroom windows
const sunLight = new THREE.DirectionalLight(0xFFB570, 4.2);
sunLight.position.set(3.8, 4.5, -6.8);
sunLight.target.position.set(-0.6, 0.8, -0.4);
scene.add(sunLight.target);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 28.0;
sunLight.shadow.camera.left = -6.0;
sunLight.shadow.camera.right = 6.0;
sunLight.shadow.camera.top = 5.0;
sunLight.shadow.camera.bottom = -5.0;
sunLight.shadow.bias = -0.0003;
sunLight.shadow.normalBias = 0.02;
sunLight.shadow.radius = 2.8;
scene.add(sunLight);

// Balanced Hemisphere ambient fill (Sky warm-white, Ground warm-taupe)
const hemiFill = new THREE.HemisphereLight(0xFFF2E0, 0x5C4E42, 0.65);
scene.add(hemiFill);
'''

code = code[:idx_sec11] + new_sec11.strip() + "\n\n" + code[idx_sec12:]

# 6. Ensure wallGroup.visible = (camState.clipHeight <= 1.30) in both render() and applyProgressToScene(p)
# In render():
code = code.replace(
    "materialGroup.visible = (camState.clipHeight > 1.25);",
    "wallGroup.visible = (camState.clipHeight <= 1.30);\n    materialGroup.visible = (camState.clipHeight > 1.25);"
)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied bright architectural wall finishes, ceilings & recessed cove lighting, and golden hour contact shadows successfully!")
