# Complete script builder for JP North Aviva Checkpoint 4
import os

def create_complete_script():
    parts = []

    # Read part 1 from generate_script.py (up to end of Section 6)
    with open(r"d:\floor plans\jp-aviva-3d\generate_script.py", "r", encoding="utf-8") as f:
        code = f.read()
    
    # Extract the JS string inside write_script
    start_marker = "f.write('''"
    end_marker = "'''"
    s_idx = code.find(start_marker) + len(start_marker)
    e_idx = code.rfind(end_marker)
    base_js = code[s_idx:e_idx]

    parts.append(base_js)

    # Section 7: Material Palettes
    parts.append('''
// ---------------------------------------------------------
// 7. MATERIAL PALETTES (LAYER A: DRAFTING, LAYER B: PBR PHYSICAL)
// ---------------------------------------------------------

// --- 1. DRAFTING MATERIALS (Layer A: Pure Architectural Ink) ---
const draftWallMat = new THREE.MeshBasicMaterial({
    color: 0xFAF8F2,
    clippingPlanes: [clipHeightPlane],
    polygonOffset: true,
    polygonOffsetFactor: 1,
    polygonOffsetUnits: 1
});
const draftEdgeMat = new THREE.LineBasicMaterial({
    color: 0x111317,
    linewidth: 2,
    clippingPlanes: [clipHeightPlane]
});
const draftDoorMat = new THREE.MeshBasicMaterial({
    color: 0x383026,
    clippingPlanes: [clipHeightPlane, livingDraftPlane]
});

// --- 2. CORE PBR WALLS ---
const pbrWhisperingSmoke = new THREE.MeshStandardMaterial({
    color: 0xECE8E1,
    roughness: 0.88,
    metalness: 0.01,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane]
});
const pbrWildMushroom = new THREE.MeshStandardMaterial({
    color: 0x998878, // Asian Paints Wild Mushroom signature wall
    roughness: 0.85,
    metalness: 0.02,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane]
});

// --- 3. POLISHED VITRIFIED FLOORS (Calacatta Marble with Roughness Map smudges & Clearcoat) ---
const pbrLivingFloor = new THREE.MeshPhysicalMaterial({
    map: calacattaTex.diffuseTex,
    roughnessMap: calacattaTex.roughnessTex,
    normalMap: calacattaTex.normalTex,
    roughness: 0.05,
    metalness: 0.08,
    clearcoat: 1.0,
    clearcoatRoughness: 0.06,
    envMapIntensity: 1.4,
    clippingPlanes: [livingMaterialPlane]
});
const pbrKitchenFloor = new THREE.MeshPhysicalMaterial({
    map: calacattaTex.diffuseTex,
    roughnessMap: calacattaTex.roughnessTex,
    normalMap: calacattaTex.normalTex,
    roughness: 0.05,
    metalness: 0.08,
    clearcoat: 1.0,
    clearcoatRoughness: 0.06,
    envMapIntensity: 1.4,
    clippingPlanes: [kitchenMaterialPlane]
});
const pbrBedroomFloor = new THREE.MeshPhysicalMaterial({
    map: calacattaTex.diffuseTex,
    roughnessMap: calacattaTex.roughnessTex,
    normalMap: calacattaTex.normalTex,
    roughness: 0.05,
    metalness: 0.08,
    clearcoat: 1.0,
    clearcoatRoughness: 0.06,
    envMapIntensity: 1.4,
    clippingPlanes: [bedroomMaterialPlane]
});

// --- 4. WOOD MATERIALS (Directional Grain Normal Map, Non-Uniform Roughness & Clearcoat) ---
const pbrOakWood = new THREE.MeshPhysicalMaterial({
    map: oakTex.diffuseTex,
    normalMap: oakTex.normalTex,
    roughnessMap: oakTex.roughnessTex,
    roughness: 0.55,
    metalness: 0.02,
    clearcoat: 0.15,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrDarkWalnut = new THREE.MeshPhysicalMaterial({
    color: 0x3A2B1E,
    normalMap: oakTex.normalTex,
    roughnessMap: oakTex.roughnessTex,
    roughness: 0.60,
    metalness: 0.02,
    clearcoat: 0.12,
    clearcoatRoughness: 0.30,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 5. FABRIC MATERIALS (Micro-Woven Twill Normal Map & High Light Absorption) ---
const pbrSofaFabric = new THREE.MeshStandardMaterial({
    map: fabricTex.diffuseTex,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrCushionRust = new THREE.MeshStandardMaterial({
    color: 0xB85736,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrCushionMustard = new THREE.MeshStandardMaterial({
    color: 0xD4A034,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrLivingBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrMatteWhite = new THREE.MeshStandardMaterial({
    color: 0xF5F5F3,
    roughness: 0.65,
    envMapIntensity: 1.0,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});
const pbrGreenVelvetChair = new THREE.MeshStandardMaterial({
    color: 0x264639,
    normalMap: fabricTex.normalTex,
    roughness: 0.88,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 6. GLASS (Physical Transmission & Refraction) ---
const pbrPhysicalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xE6F2FA,
    transmission: 1.0,
    ior: 1.5,
    roughness: 0.02,
    transparent: true,
    opacity: 1.0,
    metalness: 0.0,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane]
});
const pbrCurtain = new THREE.MeshStandardMaterial({
    color: 0xF3EFE6,
    roughness: 0.88,
    transparent: true,
    opacity: 0.88,
    envMapIntensity: 0.6,
    clippingPlanes: [clipHeightPlane, livingMaterialPlane]
});

// --- 7. METALS (Gleaming Chrome for true IBL reflections) ---
const pbrPolishedChrome = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.05,
    metalness: 1.0,
    envMapIntensity: 1.8,
    clippingPlanes: [clipHeightPlane]
});

// --- 8. BATHROOM PBR MATERIALS ---
const pbrSlateFloor = new THREE.MeshPhysicalMaterial({
    map: slateTex.diffuseTex,
    normalMap: slateTex.normalTex,
    roughness: 0.58,
    metalness: 0.06,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.1,
    clippingPlanes: [bathroomMaterialPlane]
});
const pbrFlutedCeramic = new THREE.MeshStandardMaterial({
    map: flutedTex.diffuseTex,
    normalMap: flutedTex.normalTex,
    roughness: 0.32,
    metalness: 0.02,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrBathroomOak = new THREE.MeshPhysicalMaterial({
    map: oakTex.diffuseTex,
    normalMap: oakTex.normalTex,
    roughnessMap: oakTex.roughnessTex,
    roughness: 0.55,
    metalness: 0.02,
    clearcoat: 0.15,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrCeramicSanitary = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.12,
    metalness: 0.02,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrMirrorGlass = new THREE.MeshStandardMaterial({
    color: 0xFAFAFA,
    roughness: 0.01,
    metalness: 1.0,
    envMapIntensity: 1.8,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});
const pbrBathroomBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
});

// --- 9. KITCHEN PBR MATERIALS ---
const pbrBlackQuartz = new THREE.MeshStandardMaterial({
    map: quartzTex.diffuseTex,
    normalMap: quartzTex.normalTex,
    color: 0x1A1C1E,
    roughness: 0.18,
    metalness: 0.15,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrSubwayTile = new THREE.MeshStandardMaterial({
    map: subwayTex.diffuseTex,
    normalMap: subwayTex.normalTex,
    roughness: 0.10,
    metalness: 0.02,
    clearcoat: 0.40,
    envMapIntensity: 1.3,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrInductionGlass = new THREE.MeshStandardMaterial({
    color: 0x111315,
    roughness: 0.06,
    metalness: 0.10,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrKitchenOak = new THREE.MeshPhysicalMaterial({
    map: oakTex.diffuseTex,
    normalMap: oakTex.normalTex,
    roughnessMap: oakTex.roughnessTex,
    roughness: 0.55,
    metalness: 0.02,
    clearcoat: 0.15,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});
const pbrKitchenBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, kitchenMaterialPlane]
});

// --- 10. BEDROOM PBR MATERIALS ---
const pbrBedroomOak = new THREE.MeshPhysicalMaterial({
    map: oakTex.diffuseTex,
    normalMap: oakTex.normalTex,
    roughnessMap: oakTex.roughnessTex,
    roughness: 0.55,
    metalness: 0.02,
    clearcoat: 0.15,
    clearcoatRoughness: 0.25,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrCrispWhiteLinen = new THREE.MeshStandardMaterial({
    color: 0xFAF8F4,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBedThrowCamel = new THREE.MeshStandardMaterial({
    color: 0xB5885C,
    normalMap: fabricTex.normalTex,
    roughness: 0.92,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBeigeBoucle = new THREE.MeshStandardMaterial({
    color: 0xE4DDD3,
    normalMap: fabricTex.normalTex,
    roughness: 0.94,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrBedroomBlackSteel = new THREE.MeshStandardMaterial({
    color: 0x1A1C1E,
    roughness: 0.30,
    metalness: 0.85,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});
const pbrSmokedMirror = new THREE.MeshStandardMaterial({
    color: 0x3A3A3D,
    roughness: 0.05,
    metalness: 0.95,
    envMapIntensity: 1.5,
    clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
});

// --- 11. BALCONY PBR MATERIALS ---
const pbrTeakDeck = new THREE.MeshPhysicalMaterial({
    map: teakTex.diffuseTex,
    normalMap: teakTex.normalTex,
    roughness: 0.55,
    metalness: 0.04,
    clearcoat: 0.10,
    envMapIntensity: 1.1,
    clippingPlanes: [balconyMaterialPlane]
});
const pbrBalconyChairFabric = new THREE.MeshStandardMaterial({
    color: 0x2A2E33,
    normalMap: fabricTex.normalTex,
    roughness: 0.90,
    metalness: 0.0,
    envMapIntensity: 0.5,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});
const pbrMonsteraLeaf = new THREE.MeshStandardMaterial({
    color: 0x224928,
    roughness: 0.38,
    metalness: 0.04,
    clearcoat: 0.25,
    clearcoatRoughness: 0.30,
    envMapIntensity: 1.2,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});
const pbrCeramicPot = new THREE.MeshStandardMaterial({
    color: 0xECE9E2,
    roughness: 0.50,
    envMapIntensity: 1.1,
    clippingPlanes: [clipHeightPlane, balconyMaterialPlane]
});

// ---------------------------------------------------------
// 8. GOLDEN HOUR LIGHTING (4:30 PM MUMBAI SUNLIGHT & COVE LIGHTS)
// ---------------------------------------------------------
// Warm afternoon Mumbai sunlight streaming through West-facing balcony
const sunLight = new THREE.DirectionalLight(0xFFDF9E, 4.5);
sunLight.position.set(-2.8, 3.2, -6.8);
sunLight.target.position.set(-0.8, 0.4, 0.0);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 16.0;
sunLight.shadow.camera.left = -4.5;
sunLight.shadow.camera.right = 4.5;
sunLight.shadow.camera.top = 4.5;
sunLight.shadow.camera.bottom = -4.5;
sunLight.shadow.bias = -0.00015;
scene.add(sunLight);
scene.add(sunLight.target);

// Subtle warm ambient bounce
const ambientLight = new THREE.AmbientLight(0xFFF3E2, 0.75);
scene.add(ambientLight);

// Entrance Foyer warm flush ceiling spotlight
const foyerSpot = new THREE.PointLight(0xFFE2B8, 1.8, 3.8);
foyerSpot.position.set(-2.35, 2.70, 2.15);
scene.add(foyerSpot);

// Living room warm flush ceiling spotlight
const livingSpot = new THREE.PointLight(0xFFEADB, 2.2, 5.0);
livingSpot.position.set(-1.10, 2.70, -0.20);
scene.add(livingSpot);

// Kitchen under-cabinet LED task light
const kitchenTaskLight = new THREE.PointLight(0xFFF6E8, 2.0, 3.2);
kitchenTaskLight.position.set(0.15, 1.45, 2.05);
scene.add(kitchenTaskLight);

// Master Bedroom Ceiling Cove Light (Warm ambient strip along top cornice - Ref Image 1)
const bedCoveLight = new THREE.PointLight(0xFFDFB0, 2.5, 4.2);
bedCoveLight.position.set(1.90, 2.70, 0.40);
scene.add(bedCoveLight);

// Master Bedroom bedside reading lights
const bedSpot = new THREE.PointLight(0xFFE8D4, 1.8, 3.5);
bedSpot.position.set(1.90, 1.40, 0.45);
scene.add(bedSpot);

// Common Bathroom vanity mirror glow light
const bathMirrorLight = new THREE.PointLight(0xFFE5B5, 2.2, 2.8);
bathMirrorLight.position.set(-1.25, 1.45, 1.15);
scene.add(bathMirrorLight);
''')

    # Section 9: Floors and Blueprint
    parts.append('''
// ---------------------------------------------------------
// 9. ARCHITECTURAL DRAFTING SHEET & FLOORS
// ---------------------------------------------------------
const FLOOR_W = 5.95;
const FLOOR_D = 5.20;
const WALL_H = 2.85;

// Blueprint Canvas Texture
function createBlueprintTexture() {
    const size = 2048;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#FAF8F2';
    ctx.fillRect(0, 0, size, size);

    // Fine drafting grid
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(22, 24, 27, 0.05)';
    const step = size / 40;
    for (let x = 0; x < size; x += step) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, size); ctx.stroke();
    }
    for (let y = 0; y < size; y += step) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(size, y); ctx.stroke();
    }

    // Outer border
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#111317';
    ctx.strokeRect(size * 0.04, size * 0.04, size * 0.92, size * 0.92);

    function toCanvas(wx, wz) {
        const u = (wx + FLOOR_W / 2) / FLOOR_W;
        const v = (wz + FLOOR_D / 2) / FLOOR_D;
        return [size * (0.04 + u * 0.92), size * (0.04 + v * 0.92)];
    }

    ctx.fillStyle = '#16181B';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.font = 'bold 34px "Playfair Display", Georgia, serif';
    let [rx, ry] = toCanvas(-1.45, -0.15);
    ctx.fillText('LIVING / DINING', rx, ry - 14);
    ctx.font = '22px monospace';
    ctx.fillText('10\\'6" × 12\\'2"', rx, ry + 16);

    ctx.font = 'bold 28px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-2.30, 2.10);
    ctx.fillText('FOYER', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('4\\'0" × 4\\'6"', rx, ry + 14);

    ctx.font = 'bold 26px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-1.25, 1.70);
    ctx.fillText('BATH', rx, ry - 12);
    ctx.font = '18px monospace';
    ctx.fillText('3\\'9" × 5\\'11"', rx, ry + 12);

    ctx.font = 'bold 30px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(0.25, 1.85);
    ctx.fillText('KITCHEN', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('7\\'2" × 6\\'8"', rx, ry + 14);

    ctx.font = 'bold 34px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(1.70, -0.30);
    ctx.fillText('MASTER BEDROOM', rx, ry - 14);
    ctx.font = '22px monospace';
    ctx.fillText('11\\'0" × 10\\'0"', rx, ry + 16);

    ctx.font = 'bold 28px "Playfair Display", Georgia, serif';
    [rx, ry] = toCanvas(-1.45, -2.15);
    ctx.fillText('BALCONY SANCTUARY', rx, ry - 12);
    ctx.font = '20px monospace';
    ctx.fillText('10\\'6" × 3\\'4"', rx, ry + 14);

    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}

const blueprintTex = createBlueprintTexture();

// 1. Layer A Drafting Floor Mesh (Full plan sheet)
const draftFloorGeo = new THREE.PlaneGeometry(FLOOR_W, FLOOR_D);
const draftFloorMat = new THREE.MeshBasicMaterial({
    map: blueprintTex,
    polygonOffset: true,
    polygonOffsetFactor: 2,
    polygonOffsetUnits: 2
});
const draftFloorMesh = new THREE.Mesh(draftFloorGeo, draftFloorMat);
draftFloorMesh.rotation.x = -Math.PI / 2;
draftFloorMesh.position.y = 0.001;
draftingGroup.add(draftFloorMesh);

// 2. Layer B Room-Specific Physical Floor Meshes
const livingFloorGeo = new THREE.PlaneGeometry(2.80, 4.40);
const livingFloorMesh = new THREE.Mesh(livingFloorGeo, pbrLivingFloor);
livingFloorMesh.rotation.x = -Math.PI / 2;
livingFloorMesh.position.set(-1.575, 0.002, 0.40);
livingFloorMesh.receiveShadow = true;
materialGroup.add(livingFloorMesh);

const bathroomFloorGeo = new THREE.PlaneGeometry(1.15, 1.80);
const bathroomFloorMesh = new THREE.Mesh(bathroomFloorGeo, pbrSlateFloor);
bathroomFloorMesh.rotation.x = -Math.PI / 2;
bathroomFloorMesh.position.set(-1.25, 0.003, 1.70);
bathroomFloorMesh.receiveShadow = true;
materialGroup.add(bathroomFloorMesh);

const kitchenFloorGeo = new THREE.PlaneGeometry(1.95, 1.85);
const kitchenFloorMesh = new THREE.Mesh(kitchenFloorGeo, pbrKitchenFloor);
kitchenFloorMesh.rotation.x = -Math.PI / 2;
kitchenFloorMesh.position.set(0.30, 0.002, 1.675);
kitchenFloorMesh.receiveShadow = true;
materialGroup.add(kitchenFloorMesh);

const bedFloorGeo = new THREE.PlaneGeometry(2.35, 3.45);
const bedFloorMesh = new THREE.Mesh(bedFloorGeo, pbrBedroomFloor);
bedFloorMesh.rotation.x = -Math.PI / 2;
bedFloorMesh.position.set(1.80, 0.002, -0.875);
bedFloorMesh.receiveShadow = true;
materialGroup.add(bedFloorMesh);

const balconyFloorGeo = new THREE.PlaneGeometry(2.80, 0.85);
const balconyFloorMesh = new THREE.Mesh(balconyFloorGeo, pbrTeakDeck);
balconyFloorMesh.rotation.x = -Math.PI / 2;
balconyFloorMesh.position.set(-1.575, 0.004, -2.175);
balconyFloorMesh.receiveShadow = true;
materialGroup.add(balconyFloorMesh);

// 3. Glowing Golden Transition Wavefront Beam
const beamCanvas = document.createElement('canvas');
beamCanvas.width = 256; beamCanvas.height = 16;
const bCtx = beamCanvas.getContext('2d');
const bGrad = bCtx.createLinearGradient(0, 0, 256, 0);
bGrad.addColorStop(0, 'rgba(235, 175, 85, 0)');
bGrad.addColorStop(0.5, 'rgba(255, 230, 160, 0.95)');
bGrad.addColorStop(1, 'rgba(235, 175, 85, 0)');
bCtx.fillStyle = bGrad;
bCtx.fillRect(0, 0, 256, 16);
const beamTex = new THREE.CanvasTexture(beamCanvas);

const beamGeo = new THREE.PlaneGeometry(3.0, 0.12);
const beamMat = new THREE.MeshBasicMaterial({
    map: beamTex,
    transparent: true,
    opacity: 0.92,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});
const sweepBeam = new THREE.Mesh(beamGeo, beamMat);
sweepBeam.rotation.x = -Math.PI / 2;
sweepBeam.visible = false;
scene.add(sweepBeam);

const sweepLight = new THREE.PointLight(0xFFA533, 1.8, 1.8);
sweepLight.visible = false;
scene.add(sweepLight);
''')

    # Section 10: Walls Geometry
    parts.append('''
// ---------------------------------------------------------
// 10. ARCHITECTURAL WALL GEOMETRY (5.95m x 5.20m x 2.85m)
// ---------------------------------------------------------
const WALL_THICK = 0.15;

function createDraftWall(w, h, d, x, y, z) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, draftWallMat);
    mesh.position.set(x, y, z);
    draftingGroup.add(mesh);

    const edges = new THREE.EdgesGeometry(geo);
    const line = new THREE.LineSegments(edges, draftEdgeMat);
    line.position.set(x, y, z);
    draftingGroup.add(line);
}

function createPBRWall(w, h, d, x, y, z, mat) {
    const geo = new THREE.BoxGeometry(w, h, d);
    const mesh = new THREE.Mesh(geo, mat || pbrWhisperingSmoke);
    mesh.position.set(x, y, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    materialGroup.add(mesh);
}

function addDualWall(w, h, d, x, y, z, pbrMat) {
    createDraftWall(w, h, d, x, y, z);
    createPBRWall(w, h, d, x, y, z, pbrMat);
}

// 1. Perimeter Walls
// North Exterior Wall (Balcony & Bedroom North Window)
addDualWall(3.10, WALL_H, WALL_THICK, 1.425, WALL_H / 2, -2.60);
addDualWall(0.20, WALL_H, WALL_THICK, -2.875, WALL_H / 2, -2.60);
addDualWall(0.20, WALL_H, WALL_THICK, -0.175, WALL_H / 2, -2.60);

// South Perimeter Wall with Main Entrance Door Cutout
addDualWall(3.00, WALL_H, WALL_THICK, 1.475, WALL_H / 2, 2.60);
addDualWall(0.40, WALL_H, WALL_THICK, -0.875, WALL_H / 2, 2.60);
addDualWall(0.45, WALL_H, WALL_THICK, -2.75, WALL_H / 2, 2.60);
// Lintel above 2.10m Entrance Door
addDualWall(1.05, WALL_H - 2.10, WALL_THICK, -2.00, 2.10 + (WALL_H - 2.10) / 2, 2.60);

// West Exterior Wall
addDualWall(WALL_THICK, WALL_H, FLOOR_D, -2.975 + WALL_THICK / 2, WALL_H / 2, 0);

// East Exterior Wall
addDualWall(WALL_THICK, WALL_H, FLOOR_D, 2.975 - WALL_THICK / 2, WALL_H / 2, 0);

// 2. Interior Partitions
// Balcony Divider Wall with Sliding French Glass Doorway
addDualWall(0.45, WALL_H, WALL_THICK, -2.75, WALL_H / 2, -1.75);
addDualWall(0.35, WALL_H, WALL_THICK, -0.35, WALL_H / 2, -1.75);
addDualWall(2.00, WALL_H - 2.30, WALL_THICK, -1.55, 2.30 + (WALL_H - 2.30) / 2, -1.75);

// Bedroom West Partition Wall with Bedroom Door Opening
addDualWall(WALL_THICK, WALL_H, 2.20, 0.70, WALL_H / 2, -1.50, pbrWildMushroom);
addDualWall(WALL_THICK, WALL_H - 2.10, 0.95, 0.70, 2.10 + (WALL_H - 2.10) / 2, 0.10);

// Kitchen Divider Wall (North of Kitchen)
addDualWall(2.10, WALL_H, WALL_THICK, 1.75, WALL_H / 2, 0.75);

// Common Bathroom Enclosure Walls (1.15m x 1.80m)
// North partition separating Bathroom from Living room (Z = 0.80)
addDualWall(1.15, WALL_H, WALL_THICK, -1.25, WALL_H / 2, 0.80);
// East partition separating Bathroom from Kitchen (X = -0.675)
addDualWall(WALL_THICK, WALL_H, 1.80, -0.675, WALL_H / 2, 1.70);
// West partition facing Foyer corridor with open bathroom door (Z: 1.20 to 2.00 open)
addDualWall(WALL_THICK, WALL_H, 0.40, -1.825, WALL_H / 2, 1.00);
addDualWall(WALL_THICK, WALL_H, 0.60, -1.825, WALL_H / 2, 2.30);
addDualWall(WALL_THICK, WALL_H - 2.10, 0.80, -1.825, 2.10 + (WALL_H - 2.10) / 2, 1.60);

// Main Entrance Door (Pivot at X = -2.525, Z = 2.60)
const doorPivot = new THREE.Group();
doorPivot.position.set(-2.525, 0, 2.60);
scene.add(doorPivot);

const draftDoor = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.08, 0.04), draftDoorMat);
draftDoor.position.set(0.475, 1.04, 0);
doorPivot.add(draftDoor);

const pbrDoor = new THREE.Mesh(new THREE.BoxGeometry(0.95, 2.08, 0.04), pbrDarkWalnut);
pbrDoor.position.set(0.475, 1.04, 0);
pbrDoor.castShadow = true;
doorPivot.add(pbrDoor);

const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 12), pbrPolishedChrome);
handle.rotation.z = Math.PI / 2;
handle.position.set(0.85, 1.0, 0.035);
doorPivot.add(handle);
''')

    # Section 11: Common Bathroom
    parts.append('''
// ---------------------------------------------------------
// 11. COMMON DESIGNER BATHROOM SUITE (1.15m x 1.80m ADJACENT TO FOYER)
// ---------------------------------------------------------
function buildCommonBathroom() {
    const group = new THREE.Group();

    // 1. Warm Fluted Ceramic Wall Cladding
    const northWallTile = new THREE.Mesh(new THREE.BoxGeometry(1.14, WALL_H, 0.02), pbrFlutedCeramic);
    northWallTile.position.set(-1.25, WALL_H / 2, 0.81);
    group.add(northWallTile);

    const southWallTile = new THREE.Mesh(new THREE.BoxGeometry(1.14, WALL_H, 0.02), pbrFlutedCeramic);
    southWallTile.position.set(-1.25, WALL_H / 2, 2.59);
    group.add(southWallTile);

    const eastWallTile = new THREE.Mesh(new THREE.BoxGeometry(0.02, WALL_H, 1.78), pbrFlutedCeramic);
    eastWallTile.position.set(-0.685, WALL_H / 2, 1.70);
    group.add(eastWallTile);

    // 2. Floating Natural Oak Vanity Counter (RoundedBoxGeometry)
    const vanityW = 0.65, vanityH = 0.26, vanityD = 0.40;
    const vanityCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(vanityW, vanityH, vanityD, 4, 0.02),
        pbrBathroomOak
    );
    vanityCarcass.position.set(-1.25, 0.58, 0.82 + vanityD / 2);
    vanityCarcass.castShadow = true;
    group.add(vanityCarcass);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.16, 0.12, 24), pbrCeramicSanitary);
    basin.position.set(-1.25, 0.77, 0.82 + vanityD / 2);
    basin.castShadow = true;
    group.add(basin);

    // Polished Chrome Mixer Faucet
    const bFaucetBase = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.02, 0.24, 12), pbrPolishedChrome);
    bFaucetBase.position.set(-1.25, 0.84, 0.82 + 0.09);
    group.add(bFaucetBase);

    const bFaucetSpout = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.015, 0.14), pbrPolishedChrome);
    bFaucetSpout.position.set(-1.25, 0.95, 0.82 + 0.15);
    group.add(bFaucetSpout);

    // 3. Glowing Backlit Circular LED Mirror
    const mirrorRadius = 0.30;
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(mirrorRadius, mirrorRadius, 0.015, 32), pbrMirrorGlass);
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.25, 1.45, 0.84);
    group.add(mirrorGlass);

    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE0A0,
        clippingPlanes: [clipHeightPlane, bathroomMaterialPlane]
    });
    const haloRing = new THREE.Mesh(new THREE.RingGeometry(mirrorRadius - 0.02, mirrorRadius + 0.04, 32), haloRingMat);
    haloRing.position.set(-1.25, 1.45, 0.825);
    group.add(haloRing);

    // 4. Wall-Hung Ceramic Toilet (South Wall: Z = 2.45)
    const toiletGroup = new THREE.Group();
    const cisternDuct = new THREE.Mesh(new THREE.BoxGeometry(0.60, 1.15, 0.16), pbrFlutedCeramic);
    cisternDuct.position.set(-1.25, 0.575, 2.59 - 0.08);
    toiletGroup.add(cisternDuct);

    // Chrome dual-flush actuator plate
    const flushPlate = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.12, 0.01), pbrPolishedChrome);
    flushPlate.position.set(-1.25, 0.92, 2.59 - 0.165);
    toiletGroup.add(flushPlate);

    // Toilet bowl with soft rounded geometry
    const pan = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.34, 0.54, 4, 0.06), pbrCeramicSanitary);
    pan.position.set(-1.25, 0.40, 2.59 - 0.16 - 0.27);
    pan.castShadow = true;
    toiletGroup.add(pan);
    group.add(toiletGroup);

    // 5. Sleek Fluted Glass Shower Partition
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.015, 2.10, 0.75), pbrPhysicalGlass);
    showerGlass.position.set(-1.05, 1.05, 1.40);
    group.add(showerGlass);

    const glassClampMat = pbrBathroomBlackSteel;
    const clamp1 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.06, 0.04), glassClampMat);
    clamp1.position.set(-1.05, 0.20, 1.70);
    group.add(clamp1);

    const clamp2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.06, 0.04), glassClampMat);
    clamp2.position.set(-1.05, 1.95, 1.70);
    group.add(clamp2);

    // Chrome Rain Shower Head and Arm
    const showerPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.45, 12), pbrPolishedChrome);
    showerPipe.position.set(-0.74, 2.15, 1.40);
    group.add(showerPipe);

    const showerHead = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.015, 24), pbrPolishedChrome);
    showerHead.position.set(-0.74, 2.05, 1.40);
    group.add(showerHead);

    materialGroup.add(group);
}
buildCommonBathroom();
''')

    # Section 12: Living & Dining Furniture with Study Desk & Plants (Image 3)
    parts.append('''
// ---------------------------------------------------------
// 12. LIVING & DINING ROOM FURNITURE (IMAGE 3 ENHANCEMENTS)
// ---------------------------------------------------------
function buildLShapedSofa() {
    const group = new THREE.Group();

    const baseW = 0.90, baseD = 1.65, baseH = 0.22;
    const base = new THREE.Mesh(new RoundedBoxGeometry(baseW, baseH, baseD, 4, 0.05), pbrSofaFabric);
    base.position.set(0, 0.22, 0);
    base.castShadow = true;
    group.add(base);

    const chaiseW = 0.95, chaiseD = 0.85;
    const chaise = new THREE.Mesh(new RoundedBoxGeometry(chaiseW, baseH, chaiseD, 4, 0.05), pbrSofaFabric);
    chaise.position.set(baseW / 2 + chaiseW / 2, 0.22, -baseD / 2 + chaiseD / 2);
    chaise.castShadow = true;
    group.add(chaise);

    const back1 = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.46, baseD, 4, 0.04), pbrSofaFabric);
    back1.position.set(-baseW / 2 + 0.09, 0.52, 0);
    back1.castShadow = true;
    group.add(back1);

    const armSouth = new THREE.Mesh(new RoundedBoxGeometry(baseW, 0.32, 0.16, 4, 0.04), pbrSofaFabric);
    armSouth.position.set(0, 0.38, baseD / 2 - 0.08);
    armSouth.castShadow = true;
    group.add(armSouth);

    const c1 = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.12, 0.75, 4, 0.04), pbrSofaFabric);
    c1.position.set(0.04, 0.38, 0.4);
    group.add(c1);

    const c2 = new THREE.Mesh(new RoundedBoxGeometry(0.72, 0.12, 0.75, 4, 0.04), pbrSofaFabric);
    c2.position.set(0.04, 0.38, -0.38);
    group.add(c2);

    // Accent Pillows (Rust & Mustard)
    const pillow1 = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.14, 4, 0.045), pbrCushionRust);
    pillow1.position.set(-0.18, 0.50, 0.45);
    pillow1.rotation.set(0.12, 0.26, -0.06);
    pillow1.scale.set(1.05, 1.0, 0.95);
    group.add(pillow1);

    const pillow2 = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.34, 0.13, 4, 0.04), pbrCushionMustard);
    pillow2.position.set(-0.15, 0.48, -0.15);
    pillow2.rotation.set(-0.08, -0.19, 0.07);
    pillow2.scale.set(0.96, 1.02, 1.0);
    group.add(pillow2);

    // Soft folded throw blanket draped across chaise (Ref Image 3)
    const throwBlanket = new THREE.Mesh(new RoundedBoxGeometry(0.48, 0.03, 0.70, 4, 0.015), pbrCrispWhiteLinen);
    throwBlanket.position.set(0.90, 0.36, -0.45);
    throwBlanket.rotation.y = 0.08;
    group.add(throwBlanket);

    const legGeo = new THREE.CylinderGeometry(0.022, 0.016, 0.14, 8);
    const legPositions = [
        [-baseW / 2 + 0.06, -baseD / 2 + 0.06],
        [baseW / 2 - 0.06, baseD / 2 - 0.06],
        [-baseW / 2 + 0.06, baseD / 2 - 0.06],
        [baseW / 2 + chaiseW - 0.06, -baseD / 2 + 0.06],
        [baseW / 2 + chaiseW - 0.06, -baseD / 2 + chaiseD - 0.06]
    ];
    legPositions.forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(legGeo, pbrDarkWalnut);
        leg.position.set(lx, 0.07, lz);
        group.add(leg);
    });

    group.position.set(-2.45, 0, -0.05);
    materialGroup.add(group);
}
buildLShapedSofa();

function buildCoffeeTable() {
    const group = new THREE.Group();
    const radius = 0.34, thickness = 0.035;

    const top = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, thickness, 32), pbrOakWood);
    top.position.y = 0.38;
    top.castShadow = true;
    group.add(top);

    const legGeo = new THREE.CylinderGeometry(0.015, 0.012, 0.36, 12);
    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const leg = new THREE.Mesh(legGeo, pbrLivingBlackSteel);
        leg.position.set(Math.cos(angle) * (radius * 0.65), 0.18, Math.sin(angle) * (radius * 0.65));
        leg.rotation.z = Math.sin(angle) * 0.08;
        leg.rotation.x = -Math.cos(angle) * 0.08;
        group.add(leg);
    }

    // Ceramic vase & art book
    const vase = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.065, 0.16, 16), pbrMatteWhite);
    vase.position.set(0.06, 0.48, -0.04);
    group.add(vase);

    const book = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.02, 0.15), pbrMatteWhite);
    book.position.set(-0.06, 0.405, 0.05);
    book.rotation.y = 0.3;
    group.add(book);

    group.position.set(-1.25, 0, 0.05);
    materialGroup.add(group);
}
buildCoffeeTable();

// Scandinavian Study Desk & Chair (Directly Inspired by Ref Image 3)
function buildStudyDeskAndNook() {
    const group = new THREE.Group();

    // 1. Light oak study desktop with rounded edges
    const deskTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 0.45, 4, 0.015), pbrOakWood);
    deskTop.position.set(0, 0.74, 0);
    deskTop.castShadow = true;
    group.add(deskTop);

    // Back cubby shelf riser (Ref Image 3)
    const cubbyBack = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.16, 0.12, 4, 0.015), pbrOakWood);
    cubbyBack.position.set(0, 0.83, -0.16);
    group.add(cubbyBack);

    // Slim black steel angled hairpin legs
    const legGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.72, 8);
    for (const sx of [-0.38, 0.38]) {
        for (const sz of [-0.18, 0.18]) {
            const leg = new THREE.Mesh(legGeo, pbrLivingBlackSteel);
            leg.position.set(sx, 0.36, sz);
            group.add(leg);
        }
    }

    // Modern desk lamp with warm bulb glow (Ref Image 3)
    const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.015, 16), pbrLivingBlackSteel);
    lampBase.position.set(-0.28, 0.765, -0.10);
    group.add(lampBase);

    const lampArm = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.28, 8), pbrLivingBlackSteel);
    lampArm.position.set(-0.28, 0.90, -0.10);
    group.add(lampArm);

    const lampShade = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.08, 16), pbrLivingBlackSteel);
    lampShade.position.set(-0.24, 1.02, -0.05);
    lampShade.rotation.z = -0.5;
    group.add(lampShade);

    const lampBulb = new THREE.Mesh(new THREE.SphereGeometry(0.02, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFE0B0 }));
    lampBulb.position.set(-0.24, 1.00, -0.05);
    group.add(lampBulb);

    const lampLight = new THREE.PointLight(0xFFE2B8, 1.4, 1.8);
    lampLight.position.set(-0.24, 0.98, -0.05);
    group.add(lampLight);

    // Open notebook & ceramic mug
    const notebook = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.012, 0.16), pbrMatteWhite);
    notebook.position.set(0.05, 0.762, 0.05);
    notebook.rotation.y = 0.08;
    group.add(notebook);

    const mug = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.028, 0.07, 12), new THREE.MeshStandardMaterial({ color: 0x4A5859, roughness: 0.3 }));
    mug.position.set(0.25, 0.795, -0.05);
    group.add(mug);

    // Green velvet study chair with slim steel frame (Ref Image 3)
    const chairGroup = new THREE.Group();
    const seat = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.05, 0.38, 4, 0.025), pbrGreenVelvetChair);
    seat.position.y = 0.46;
    chairGroup.add(seat);

    const backrest = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.38, 0.04, 4, 0.02), pbrGreenVelvetChair);
    backrest.position.set(0, 0.68, 0.16);
    backrest.rotation.x = 0.10;
    chairGroup.add(backrest);

    const chairLegGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.45, 8);
    for (const cx of [-0.15, 0.15]) {
        for (const cz of [-0.15, 0.15]) {
            const cl = new THREE.Mesh(chairLegGeo, pbrLivingBlackSteel);
            cl.position.set(cx, 0.225, cz);
            chairGroup.add(cl);
        }
    }
    chairGroup.position.set(0, 0, 0.35);
    group.add(chairGroup);

    // Position study desk along West wall north of sofa
    group.position.set(-2.40, 0, -1.15);
    materialGroup.add(group);
}
buildStudyDeskAndNook();

// Wall Wire Planter Shelf with Green Ivy/Pothos Foliage (Ref Image 3)
function buildWallPlanterShelf() {
    const group = new THREE.Group();
    const wireMat = pbrLivingBlackSteel;

    // Outer wire frame
    const frame = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.60, 0.50), wireMat);
    frame.position.set(0, 0, 0);
    group.add(frame);

    // Two small wooden shelves
    const shelf1 = new THREE.Mesh(new RoundedBoxGeometry(0.12, 0.015, 0.46, 4, 0.005), pbrOakWood);
    shelf1.position.set(0.05, -0.12, 0);
    group.add(shelf1);

    const shelf2 = new THREE.Mesh(new RoundedBoxGeometry(0.12, 0.015, 0.46, 4, 0.005), pbrOakWood);
    shelf2.position.set(0.05, 0.15, 0);
    group.add(shelf2);

    // Potted plants with cascading trailing leaves
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.035, 0.08, 12), pbrCeramicPot);
    pot.position.set(0.05, 0.20, -0.10);
    group.add(pot);

    for (let i = 0; i < 8; i++) {
        const leaf = new THREE.Mesh(new THREE.SphereGeometry(0.025, 8, 8), pbrMonsteraLeaf);
        leaf.scale.set(1.4, 0.4, 1.2);
        leaf.position.set(0.06 + (Math.random() - 0.5) * 0.05, 0.18 - i * 0.04, -0.10 + (Math.random() - 0.5) * 0.06);
        leaf.rotation.set(0.4, Math.random() * Math.PI, 0.2);
        group.add(leaf);
    }

    group.position.set(-2.88, 1.65, -1.15);
    materialGroup.add(group);
}
buildWallPlanterShelf();

// Modern Branching 3-Arm Chandelier Fixture (Ref Image 3)
function buildLivingChandelier() {
    const group = new THREE.Group();
    const rodMat = pbrLivingBlackSteel;

    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.40, 8), rodMat);
    stem.position.set(0, WALL_H - 0.20, 0);
    group.add(stem);

    for (let i = 0; i < 3; i++) {
        const angle = (i * Math.PI * 2) / 3;
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.35, 8), rodMat);
        arm.position.set(Math.cos(angle) * 0.15, WALL_H - 0.38, Math.sin(angle) * 0.15);
        arm.rotation.z = Math.PI / 2;
        arm.rotation.y = angle;
        group.add(arm);

        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFF0D0 }));
        bulb.position.set(Math.cos(angle) * 0.30, WALL_H - 0.38, Math.sin(angle) * 0.30);
        group.add(bulb);
    }

    group.position.set(-1.10, 0, -0.20);
    materialGroup.add(group);
}
buildLivingChandelier();

function buildDiningNook() {
    const group = new THREE.Group();

    const tableTop = new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.035, 0.60, 4, 0.015), pbrOakWood);
    tableTop.position.set(0, 0.74, 0);
    tableTop.castShadow = true;
    group.add(tableTop);

    const tLegGeo = new THREE.BoxGeometry(0.03, 0.72, 0.03);
    for (const sx of [-0.38, 0.38]) {
        for (const sz of [-0.25, 0.25]) {
            const tLeg = new THREE.Mesh(tLegGeo, pbrLivingBlackSteel);
            tLeg.position.set(sx, 0.36, sz);
            group.add(tLeg);
        }
    }

    function buildChair(cz, rotY) {
        const cg = new THREE.Group();
        const seat = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.04, 0.38, 4, 0.02), pbrWhisperingSmoke);
        seat.position.y = 0.45;
        cg.add(seat);

        const back = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.38, 0.025, 4, 0.015), pbrWhisperingSmoke);
        back.position.set(0, 0.65, -0.17);
        cg.add(back);

        const cLegGeo = new THREE.CylinderGeometry(0.012, 0.008, 0.44, 6);
        for (const cx of [-0.15, 0.15]) {
            for (const cz2 of [-0.15, 0.15]) {
                const cLeg = new THREE.Mesh(cLegGeo, pbrLivingBlackSteel);
                cLeg.position.set(cx, 0.22, cz2);
                cg.add(cLeg);
            }
        }
        cg.position.set(0, 0, cz);
        cg.rotation.y = rotY;
        return cg;
    }

    group.add(buildChair(-0.48, 0));
    group.add(buildChair(0.48, Math.PI));

    group.position.set(0.15, 0, 0.35);
    materialGroup.add(group);
}
buildDiningNook();

function buildMediaWall() {
    const group = new THREE.Group();

    const cw = 1.40, ch = 0.30, cd = 0.32;
    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(cd, ch, cw, 4, 0.025), pbrOakWood);
    consoleBox.position.set(0, 0.48, 0);
    consoleBox.castShadow = true;
    group.add(consoleBox);

    const drawerFront = new THREE.Mesh(new RoundedBoxGeometry(0.02, ch - 0.05, cw - 0.06, 4, 0.015), pbrMatteWhite);
    drawerFront.position.set(-cd / 2 - 0.01, 0.48, 0);
    group.add(drawerFront);

    // Slim 50" 4K TV Screen
    const tvW = 1.15, tvH = 0.66;
    const tvBezel = new THREE.Mesh(new THREE.BoxGeometry(0.02, tvH, tvW), pbrLivingBlackSteel);
    tvBezel.position.set(-0.06, 1.25, 0);
    group.add(tvBezel);

    const tvScreen = new THREE.Mesh(new THREE.BoxGeometry(0.005, tvH - 0.03, tvW - 0.03), new THREE.MeshStandardMaterial({ color: 0x0A0B0D, roughness: 0.15, metalness: 0.9 }));
    tvScreen.position.set(-0.075, 1.25, 0);
    group.add(tvScreen);

    // Soundbar
    const soundbar = new THREE.Mesh(new RoundedBoxGeometry(0.06, 0.05, 0.70, 4, 0.01), pbrLivingBlackSteel);
    soundbar.position.set(-0.06, 0.66, 0);
    group.add(soundbar);

    group.position.set(0.62, 0, -0.65);
    materialGroup.add(group);
}
buildMediaWall();

function buildBalconySlidingDoors() {
    const group = new THREE.Group();

    const frameMat = pbrLivingBlackSteel;
    const outerFrame = new THREE.Mesh(new THREE.BoxGeometry(2.02, 2.30, 0.06), frameMat);
    outerFrame.position.set(0, 1.15, 0);

    const leftGlass = new THREE.Mesh(new THREE.BoxGeometry(0.96, 2.22, 0.015), pbrPhysicalGlass);
    leftGlass.position.set(-0.48, 1.15, -0.015);
    group.add(leftGlass);

    const rightGlass = new THREE.Mesh(new THREE.BoxGeometry(0.96, 2.22, 0.015), pbrPhysicalGlass);
    rightGlass.position.set(0.48, 1.15, 0.015);
    group.add(rightGlass);

    // Sheer Curtains with soft opacity
    const curtainGeo = new THREE.PlaneGeometry(0.90, 2.30);
    const cLeft = new THREE.Mesh(curtainGeo, pbrCurtain);
    cLeft.position.set(-0.85, 1.15, 0.06);
    group.add(cLeft);

    const cRight = new THREE.Mesh(curtainGeo, pbrCurtain);
    cRight.position.set(0.85, 1.15, 0.06);
    group.add(cRight);

    group.position.set(-1.55, 0, -1.75);
    materialGroup.add(group);
}
buildBalconySlidingDoors();
''')

    # Section 13: Kitchen Hub
    parts.append('''
// ---------------------------------------------------------
// 13. L-SHAPED KITCHEN HUB
// ---------------------------------------------------------
function buildKitchen() {
    const group = new THREE.Group();

    // 1. Black Quartz Countertops
    const mainCounter = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.04, 0.60), pbrBlackQuartz);
    mainCounter.position.set(0.15, 0.86, 2.25);
    mainCounter.castShadow = true;
    group.add(mainCounter);

    const returnCounter = new THREE.Mesh(new THREE.BoxGeometry(0.60, 0.04, 0.90), pbrBlackQuartz);
    returnCounter.position.set(0.65, 0.86, 1.50);
    returnCounter.castShadow = true;
    group.add(returnCounter);

    // 2. Base Oak Cabinets
    const baseCabinets = new THREE.Mesh(new RoundedBoxGeometry(1.58, 0.74, 0.58, 4, 0.02), pbrKitchenOak);
    baseCabinets.position.set(0.15, 0.42, 2.25);
    baseCabinets.castShadow = true;
    group.add(baseCabinets);

    const returnBase = new THREE.Mesh(new RoundedBoxGeometry(0.58, 0.74, 0.88, 4, 0.02), pbrKitchenOak);
    returnBase.position.set(0.65, 0.42, 1.50);
    returnBase.castShadow = true;
    group.add(returnBase);

    // 3. Glazed White Subway Tile Backsplash
    const backsplashMain = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.65, 0.02), pbrSubwayTile);
    backsplashMain.position.set(0.15, 1.20, 2.54);
    group.add(backsplashMain);

    // 4. Upper Fluted Glass & Oak Cabinets
    const upperCabinets = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.65, 0.35, 4, 0.02), pbrKitchenOak);
    upperCabinets.position.set(0.15, 1.85, 2.38);
    upperCabinets.castShadow = true;
    group.add(upperCabinets);

    // 5. Stainless Steel Undermount Sink & Chrome Faucet
    const sinkRim = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.02, 0.38), pbrPolishedChrome);
    sinkRim.position.set(-0.25, 0.88, 2.25);
    group.add(sinkRim);

    const faucetBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 12), pbrPolishedChrome);
    faucetBase.position.set(-0.25, 0.99, 2.44);
    group.add(faucetBase);

    const faucetSpout = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.16, 12), pbrPolishedChrome);
    faucetSpout.rotation.x = Math.PI / 2;
    faucetSpout.position.set(-0.25, 1.10, 2.36);
    group.add(faucetSpout);

    // 6. Flat Glass Induction Cooktop with red LED burner indicators
    const cooktop = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.01, 0.45), pbrInductionGlass);
    cooktop.position.set(0.40, 0.885, 2.25);
    group.add(cooktop);

    const burner1 = new THREE.Mesh(new THREE.RingGeometry(0.08, 0.09, 24), new THREE.MeshBasicMaterial({ color: 0xFF3300, clippingPlanes: [clipHeightPlane, kitchenMaterialPlane] }));
    burner1.rotation.x = -Math.PI / 2;
    burner1.position.set(0.32, 0.892, 2.25);
    group.add(burner1);

    const burner2 = new THREE.Mesh(new THREE.RingGeometry(0.06, 0.07, 24), new THREE.MeshBasicMaterial({ color: 0xFF3300, clippingPlanes: [clipHeightPlane, kitchenMaterialPlane] }));
    burner2.rotation.x = -Math.PI / 2;
    burner2.position.set(0.48, 0.892, 2.25);
    group.add(burner2);

    materialGroup.add(group);
}
buildKitchen();
''')

    # Section 14: Master Bedroom (with Cove Light & Tufted Headboard - Ref Image 1)
    parts.append('''
// ---------------------------------------------------------
// 14. MASTER BEDROOM SUITE (REF IMAGE 1 ENHANCEMENTS)
// ---------------------------------------------------------
function buildMasterBedroom() {
    const group = new THREE.Group();

    // Bed Plinth
    const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.12, 1.75), pbrBedroomBlackSteel);
    plinth.position.set(1.90, 0.06, -0.25);
    group.add(plinth);

    // Oak Platform Frame with rounded corners
    const frame = new THREE.Mesh(new RoundedBoxGeometry(1.65, 0.18, 2.05, 4, 0.02), pbrBedroomOak);
    frame.position.set(1.90, 0.21, -0.25);
    frame.castShadow = true;
    group.add(frame);

    // Mattress with soft radius
    const mattress = new THREE.Mesh(new RoundedBoxGeometry(1.55, 0.24, 1.95, 4, 0.055), pbrCrispWhiteLinen);
    mattress.position.set(1.90, 0.42, -0.25);
    mattress.castShadow = true;
    group.add(mattress);

    // Duvet
    const duvet = new THREE.Mesh(new RoundedBoxGeometry(1.58, 0.13, 1.48, 4, 0.05), pbrCrispWhiteLinen);
    duvet.position.set(1.90, 0.525, -0.48);
    duvet.castShadow = true;
    group.add(duvet);

    // Camel Bed Runner
    const bedRunner = new THREE.Mesh(new RoundedBoxGeometry(1.60, 0.02, 0.45, 4, 0.01), pbrBedThrowCamel);
    bedRunner.position.set(1.90, 0.59, -0.95);
    group.add(bedRunner);

    // Dual Pillows with organic slight tilts
    const pLeft = new THREE.Mesh(new RoundedBoxGeometry(0.63, 0.22, 0.35, 4, 0.045), pbrCrispWhiteLinen);
    pLeft.position.set(1.55, 0.56, 0.50);
    pLeft.rotation.set(-0.30, 0.04, 0.02);
    group.add(pLeft);

    const pRight = new THREE.Mesh(new RoundedBoxGeometry(0.61, 0.23, 0.34, 4, 0.045), pbrCrispWhiteLinen);
    pRight.position.set(2.25, 0.56, 0.50);
    pRight.rotation.set(-0.28, -0.05, -0.02);
    group.add(pRight);

    // Tufted Geometric Headboard (Ref Image 1)
    const hbGroup = new THREE.Group();
    const hbBack = new THREE.Mesh(new RoundedBoxGeometry(2.10, 1.10, 0.06, 4, 0.02), pbrBedroomOak);
    hbBack.position.set(1.90, 0.85, 0.72);
    hbGroup.add(hbBack);

    for (let col = 0; col < 3; col++) {
        for (let row = 0; row < 2; row++) {
            const tuft = new THREE.Mesh(new RoundedBoxGeometry(0.56, 0.44, 0.06, 4, 0.035), pbrBeigeBoucle);
            tuft.position.set(1.30 + col * 0.60, 0.60 + row * 0.48, 0.68);
            hbGroup.add(tuft);
        }
    }
    group.add(hbGroup);

    // Warm Ceiling Cove Lighting Strip along cornice (Ref Image 1)
    const coveStrip = new THREE.Mesh(
        new THREE.BoxGeometry(2.00, 0.03, 0.05),
        new THREE.MeshBasicMaterial({ color: 0xFFF0D0, clippingPlanes: [clipHeightPlane, bedroomMaterialPlane] })
    );
    coveStrip.position.set(1.90, WALL_H - 0.06, 0.70);
    group.add(coveStrip);

    // Floating Nightstands
    function buildNightstand(nx) {
        const nGroup = new THREE.Group();
        const nBox = new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.18, 0.34, 4, 0.02), pbrBedroomOak);
        nBox.position.set(nx, 0.46, 0.55);
        nBox.castShadow = true;
        nGroup.add(nBox);

        // Wall reading sconce
        const sconceBase = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.12, 0.02), pbrBedroomBlackSteel);
        sconceBase.position.set(nx, 1.25, 0.72);
        nGroup.add(sconceBase);

        const bulbMat = new THREE.MeshBasicMaterial({
            color: 0xFFE0A0,
            clippingPlanes: [clipHeightPlane, bedroomMaterialPlane]
        });
        const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.035, 16, 16), bulbMat);
        bulb.position.set(nx, 1.25, 0.67);
        nGroup.add(bulb);

        return nGroup;
    }

    group.add(buildNightstand(0.85));
    group.add(buildNightstand(2.72));

    // Floating Study / Vanity Desk on Opposite Wall (Ref Image 1)
    const deskConsole = new THREE.Mesh(new RoundedBoxGeometry(1.20, 0.08, 0.38, 4, 0.015), pbrBedroomOak);
    deskConsole.position.set(1.90, 0.74, -1.80);
    deskConsole.castShadow = true;
    group.add(deskConsole);

    const stool = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.44, 0.30, 4, 0.02), pbrDarkWalnut);
    stool.position.set(1.90, 0.22, -1.55);
    group.add(stool);

    // Sleek Sliding Wardrobe
    const wardrobeW = 1.35, wardrobeH = 2.45, wardrobeD = 0.58;
    const wardrobeBox = new THREE.Mesh(new RoundedBoxGeometry(wardrobeW, wardrobeH, wardrobeD, 4, 0.02), pbrBedroomOak);
    wardrobeBox.position.set(1.90, wardrobeH / 2, -2.15);
    wardrobeBox.castShadow = true;
    group.add(wardrobeBox);

    const mirrorDoor = new THREE.Mesh(new THREE.BoxGeometry(wardrobeW / 2 - 0.02, wardrobeH - 0.08, 0.015), pbrSmokedMirror);
    mirrorDoor.position.set(1.90 + wardrobeW / 4, wardrobeH / 2, -2.15 + wardrobeD / 2 + 0.01);
    group.add(mirrorDoor);

    materialGroup.add(group);
}
buildMasterBedroom();
''')

    # Section 15: Balcony Sanctuary
    parts.append('''
// ---------------------------------------------------------
// 15. ENCLOSED BALCONY SANCTUARY & EXTERIOR SKYLINE
// ---------------------------------------------------------
let skyMesh = null;

function buildBalcony() {
    const group = new THREE.Group();

    // 1. Modern Minimalist Outdoor Lounge Chair
    const chairGroup = new THREE.Group();
    const cFrame = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.04, 0.70), pbrBedroomBlackSteel);
    cFrame.position.set(0, 0.24, 0);
    chairGroup.add(cFrame);

    const legGeo = new THREE.CylinderGeometry(0.014, 0.010, 0.24, 8);
    for (const sx of [-0.28, 0.28]) {
        for (const sz of [-0.30, 0.30]) {
            const leg = new THREE.Mesh(legGeo, pbrBedroomBlackSteel);
            leg.position.set(sx, 0.12, sz);
            chairGroup.add(leg);
        }
    }

    const seatCushion = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.10, 0.64, 4, 0.03), pbrBalconyChairFabric);
    seatCushion.position.set(0, 0.31, 0);
    seatCushion.castShadow = true;
    chairGroup.add(seatCushion);

    const backCushion = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.38, 0.10, 4, 0.03), pbrBalconyChairFabric);
    backCushion.position.set(0, 0.50, 0.26);
    backCushion.rotation.x = -0.18;
    backCushion.castShadow = true;
    chairGroup.add(backCushion);

    chairGroup.position.set(-2.15, 0, -2.15);
    chairGroup.rotation.y = 0.45;
    group.add(chairGroup);

    // 2. Minimalist Ceramic Planter with Monstera Plant
    const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.14, 0.36, 24), pbrCeramicPot);
    pot.position.set(-0.65, 0.18, -2.25);
    pot.castShadow = true;
    group.add(pot);

    const stemGeo = new THREE.CylinderGeometry(0.008, 0.006, 0.45, 8);
    const leafGeo = new THREE.SphereGeometry(0.12, 12, 12);

    const leafOffsets = [
        [0.0, 0.38, 0.0, 0.3, 0.4],
        [0.10, 0.48, -0.08, -0.2, 1.2],
        [-0.08, 0.52, 0.06, 0.4, -0.8],
        [0.06, 0.60, 0.04, -0.3, 2.1],
        [-0.05, 0.65, -0.06, 0.2, -2.4]
    ];

    leafOffsets.forEach(([ox, oy, oz, rx, ry]) => {
        const stem = new THREE.Mesh(stemGeo, pbrMonsteraLeaf);
        stem.position.set(-0.65 + ox * 0.5, 0.36 + oy * 0.4, -2.25 + oz * 0.5);
        stem.rotation.set(rx * 0.5, ry, 0);
        group.add(stem);

        const leaf = new THREE.Mesh(leafGeo, pbrMonsteraLeaf);
        leaf.scale.set(1.5, 0.08, 1.1);
        leaf.position.set(-0.65 + ox, 0.36 + oy, -2.25 + oz);
        leaf.rotation.set(rx, ry, 0.2);
        leaf.castShadow = true;
        group.add(leaf);
    });

    // 3. Full-Height Balcony Windows
    const windowGlass = new THREE.Mesh(new THREE.BoxGeometry(2.70, 2.70, 0.015), pbrPhysicalGlass);
    windowGlass.position.set(-1.575, 1.35, -2.60);
    group.add(windowGlass);

    materialGroup.add(group);

    // 4. Photorealistic Exterior Skyline Panorama
    const skyCanvas = document.createElement('canvas');
    skyCanvas.width = 1024; skyCanvas.height = 512;
    const sCtx = skyCanvas.getContext('2d');

    const skyGrad = sCtx.createLinearGradient(0, 0, 0, 512);
    skyGrad.addColorStop(0, '#5E88B8');
    skyGrad.addColorStop(0.40, '#DDA46B');
    skyGrad.addColorStop(0.65, '#E88C48');
    skyGrad.addColorStop(1, '#B25329');
    sCtx.fillStyle = skyGrad;
    sCtx.fillRect(0, 0, 1024, 512);

    // Golden sun glow
    const sunGrad = sCtx.createRadialGradient(320, 260, 20, 320, 260, 220);
    sunGrad.addColorStop(0, 'rgba(255, 245, 210, 0.95)');
    sunGrad.addColorStop(0.3, 'rgba(255, 200, 120, 0.6)');
    sunGrad.addColorStop(1, 'rgba(232, 140, 72, 0)');
    sCtx.fillStyle = sunGrad;
    sCtx.fillRect(0, 0, 1024, 512);

    // Distant towers
    sCtx.fillStyle = 'rgba(70, 48, 40, 0.35)';
    for (let i = 0; i < 28; i++) {
        const bx = i * 38;
        const bw = 24 + (i % 4) * 8;
        const bh = 90 + ((i * 37) % 180);
        sCtx.fillRect(bx, 512 - bh, bw, bh);
    }
    sCtx.fillStyle = 'rgba(40, 25, 20, 0.65)';
    for (let j = 0; j < 22; j++) {
        const bx = j * 48 + 12;
        const bw = 28 + (j % 3) * 10;
        const bh = 50 + ((j * 43) % 130);
        sCtx.fillRect(bx, 512 - bh, bw, bh);
    }

    const skyTex = new THREE.CanvasTexture(skyCanvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    skyMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(28, 28, 20, 32, 1, true, -Math.PI / 2, Math.PI),
        new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide })
    );
    skyMesh.position.set(0, 4, -4);
    skyMesh.visible = false;
    scene.add(skyMesh);
}
buildBalcony();
''')

    # Section 16: GSAP Timeline with cameraTarget panning
    parts.append('''
// ---------------------------------------------------------
// 16. SCROLL TIMELINE ANIMATION (GSAP + SCROLLTRIGGER)
// ---------------------------------------------------------
const camState = {
    progress: 0,
    posX: -0.20,
    posY: 11.5,
    posZ: 0.0001,
    targetX: -0.20,
    targetY: 0,
    targetZ: 0,
    clipHeight: 1.20,
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 1.00,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0
};

// Dedicated GSAP LookAt Target Vector
const cameraTarget = new THREE.Vector3(camState.targetX, camState.targetY, camState.targetZ);

// HUD Elements
const progressPercentEl = document.getElementById('progress-percent');
const progressBarFillEl = document.getElementById('progress-bar-fill');
const phaseStepEl = document.getElementById('phase-step');
const phaseLabelEl = document.getElementById('phase-label');

function updateUI() {
    const p = Math.round(camState.progress * 100);
    if (progressPercentEl) progressPercentEl.textContent = `${p}%`;
    if (progressBarFillEl) progressBarFillEl.style.width = `${p}%`;

    if (p < 10) {
        phaseStepEl.textContent = 'STOP 0 — 0%-10%';
        phaseLabelEl.textContent = 'The Architectural Plan Sheet (2D Drafting Cut @ 1.2m)';
    } else if (p < 20) {
        phaseStepEl.textContent = 'STOP 1 — 10%-20%';
        phaseLabelEl.textContent = 'Walls Rising & Threshold Descent (Extruding to 2.85m)';
    } else if (p < 32) {
        phaseStepEl.textContent = 'STOP 2 — 20%-32%';
        phaseLabelEl.textContent = 'Entrance Foyer & Bathroom Pan (Ink Dissolve to Slate Tiles)';
    } else if (p < 44) {
        phaseStepEl.textContent = 'STOP 3 — 32%-44%';
        phaseLabelEl.textContent = 'Common Designer Bathroom Suite (Vanity, Backlit LED Mirror & Shower)';
    } else if (p < 58) {
        phaseStepEl.textContent = 'STOP 4 — 44%-58%';
        phaseLabelEl.textContent = 'Living Room Entry & Kitchen Panorama Sweep (Quartz & Subway Tiles)';
    } else if (p < 72) {
        phaseStepEl.textContent = 'STOP 5 — 58%-72%';
        phaseLabelEl.textContent = 'Living & Dining Sanctuary (L-Shaped Sofa, Study Desk & Wall Plants)';
    } else if (p < 86) {
        phaseStepEl.textContent = 'STOP 6 — 72%-86%';
        phaseLabelEl.textContent = 'Master Bedroom Suite (Cove Lighting, Tufted Bed & Wild Mushroom Wall)';
    } else {
        phaseStepEl.textContent = 'STOP 7 — 86%-100%';
        phaseLabelEl.textContent = 'Enclosed Balcony Finale (Teak Deck Parquet & 4:30 PM Sunset)';
    }
}

// Master GSAP Timeline tied to the 800vh scroll container
const tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#scroll-container',
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.8,
        onUpdate: (self) => {
            camState.progress = self.progress;
            cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
            camera.lookAt(cameraTarget);
            updateUI();
        }
    }
});

// --- STOP 0: 0% to 10% (Flat 2D Blueprint Sheet) ---
tl.to(camState, {
    posX: -0.20,
    posY: 11.5,
    posZ: 0.0001,
    targetX: -0.20,
    targetY: 0,
    targetZ: 0,
    clipHeight: 1.20,
    sweepLivingZ: 3.60,
    sweepBathroomX: -1.85,
    sweepKitchenZ: 1.00,
    sweepBedroomZ: 0.85,
    sweepBalconyZ: -1.25,
    doorAngle: 0,
    duration: 0.10,
    ease: 'none'
});

// --- STOP 1: 10% to 20% (Walls extrude, camera dives to front entrance door) ---
tl.to(camState, {
    clipHeight: 2.85,
    sweepLivingZ: 3.60,
    posX: -2.35,
    posY: 1.45,
    posZ: 3.50,
    targetX: -2.35,
    targetY: 1.38,
    targetZ: 2.60,
    doorAngle: 0,
    duration: 0.10,
    ease: 'power2.inOut'
});

// --- STOP 2: 20% to 32% (Entrance Foyer & CameraTarget Pans 90 deg into Bathroom!) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    posX: -2.25,
    posY: 1.45,
    posZ: 1.85,
    // Smooth cinematic pan into the open bathroom door!
    targetX: -1.25,
    targetY: 1.25,
    targetZ: 1.65,
    sweepLivingZ: 1.20,
    sweepBathroomX: -0.65,
    duration: 0.12,
    ease: 'power1.inOut'
});

// --- STOP 3: 32% to 44% (Bathroom Suite Close-Up Inspection) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepLivingZ: 1.20,
    sweepBathroomX: -0.65,
    posX: -2.10,
    posY: 1.45,
    posZ: 1.60,
    targetX: -1.15,
    targetY: 1.25,
    targetZ: 1.60,
    duration: 0.12,
    ease: 'power2.inOut'
});

// --- STOP 4: 44% to 58% (Living Entry & CameraTarget Sweeps across L-Shaped Kitchen!) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    posX: -0.90,
    posY: 1.45,
    posZ: 0.45,
    // Cinematic cameraTarget sweep across the L-shaped Kitchen counters & backsplash!
    targetX: 0.20,
    targetY: 1.15,
    targetZ: 2.10,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -0.40,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 5: 58% to 72% (Living & Dining Sanctuary with Study Desk) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBathroomX: -0.65,
    sweepKitchenZ: 2.65,
    posX: -0.80,
    posY: 1.45,
    posZ: 0.05,
    // CameraTarget pivots forward toward L-shaped sofa, study desk & balcony window
    targetX: -1.55,
    targetY: 1.05,
    targetZ: -1.30,
    sweepLivingZ: -1.50,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 6: 72% to 86% (Master Bedroom Suite & Ceiling Cove Lighting) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepKitchenZ: 2.65,
    sweepLivingZ: -1.50,
    posX: 1.30,
    posY: 1.42,
    posZ: -1.60,
    targetX: 2.10,
    targetY: 1.05,
    targetZ: 0.40,
    sweepBedroomZ: -2.60,
    duration: 0.14,
    ease: 'power2.inOut'
});

// --- STOP 7: 86% to 100% (The Balcony Finale & Golden Hour Sunset) ---
tl.to(camState, {
    clipHeight: 2.85,
    doorAngle: -Math.PI / 2,
    sweepBedroomZ: -2.60,
    posX: -0.30,
    posY: 1.40,
    posZ: -1.65,
    targetX: -2.10,
    targetY: 1.02,
    targetZ: -2.15,
    sweepBalconyZ: -2.65,
    duration: 0.14,
    ease: 'power2.inOut'
});
''')

    # Section 17, 18, 19: Render loop, snapshots, resize
    parts.append('''
// ---------------------------------------------------------
// 17. RENDER LOOP WITH SSAO POST-PROCESSING
// ---------------------------------------------------------
let isCapturing = false;

function render() {
    requestAnimationFrame(render);
    if (isCapturing) return;

    materialGroup.visible = (camState.clipHeight > 1.30);
    clipHeightPlane.constant = camState.clipHeight;

    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;

    bathroomDraftPlane.constant = camState.sweepBathroomX;
    bathroomMaterialPlane.constant = -camState.sweepBathroomX;

    kitchenDraftPlane.constant = -camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = camState.sweepKitchenZ;

    bedroomDraftPlane.constant = camState.sweepBedroomZ;
    bedroomMaterialPlane.constant = -camState.sweepBedroomZ;

    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;

    // Glowing wavefront beam
    if (camState.progress < 0.32) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 3.2 && camState.sweepLivingZ > 1.1);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress < 0.44) {
        sweepBeam.scale.set(0.40, 1.0, 1.0);
        sweepBeam.rotation.y = Math.PI / 2;
        sweepBeam.position.set(camState.sweepBathroomX, 0.008, 1.70);
        sweepLight.position.set(camState.sweepBathroomX, 0.15, 1.70);
        const isSweeping = (camState.sweepBathroomX > -1.82 && camState.sweepBathroomX < -0.68);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else if (camState.progress < 0.58) {
        sweepBeam.scale.set(1.0, 1.0, 1.0);
        sweepBeam.rotation.y = 0;
        sweepBeam.position.set(-1.05, 0.008, camState.sweepLivingZ);
        sweepLight.position.set(-1.05, 0.15, camState.sweepLivingZ);
        const isSweeping = (camState.sweepLivingZ < 1.1 && camState.sweepLivingZ > -1.3);
        sweepBeam.visible = isSweeping;
        sweepLight.visible = isSweeping;
    } else {
        sweepBeam.visible = false;
        sweepLight.visible = false;
    }

    doorPivot.rotation.y = camState.doorAngle;

    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);

    if (skyMesh) {
        skyMesh.visible = (camState.clipHeight > 1.35);
    }

    ssaoPass.enabled = (camState.clipHeight > 1.30);
    composer.render();
}

render();
updateUI();

// ---------------------------------------------------------
// 18. AUTOMATIC SNAPSHOT RECORDER FOR CHECKPOINT 4 (8 STOPS)
// ---------------------------------------------------------
async function captureCheckpointSnapshots() {
    isCapturing = true;
    console.log("Starting Checkpoint 4 automated recording (8 Stops with Bathroom adjacent to Foyer)...");
    const stops = [
        { name: 'checkpoint4_stop0_plan_sheet.jpg', progress: 0.08 },
        { name: 'checkpoint4_stop1_walls_rising.jpg', progress: 0.19 },
        { name: 'checkpoint4_stop2_foyer_transition.jpg', progress: 0.31 },
        { name: 'checkpoint4_stop3_bathroom_suite.jpg', progress: 0.43 },
        { name: 'checkpoint4_stop4_living_reveal.jpg', progress: 0.57 },
        { name: 'checkpoint4_stop5_kitchen_hub.jpg', progress: 0.71 },
        { name: 'checkpoint4_stop6_bedroom_suite.jpg', progress: 0.85 },
        { name: 'checkpoint4_stop7_balcony_finale.jpg', progress: 0.99 }
    ];

    for (const stop of stops) {
        try {
            tl.progress(stop.progress);

            materialGroup.visible = (camState.clipHeight > 1.30);
            clipHeightPlane.constant = camState.clipHeight;
            livingDraftPlane.constant = camState.sweepLivingZ;
            livingMaterialPlane.constant = -camState.sweepLivingZ;
            bathroomDraftPlane.constant = camState.sweepBathroomX;
            bathroomMaterialPlane.constant = -camState.sweepBathroomX;
            kitchenDraftPlane.constant = -camState.sweepKitchenZ;
            kitchenMaterialPlane.constant = camState.sweepKitchenZ;
            bedroomDraftPlane.constant = camState.sweepBedroomZ;
            bedroomMaterialPlane.constant = -camState.sweepBedroomZ;
            balconyDraftPlane.constant = camState.sweepBalconyZ;
            balconyMaterialPlane.constant = -camState.sweepBalconyZ;
            doorPivot.rotation.y = camState.doorAngle;

            camera.position.set(camState.posX, camState.posY, camState.posZ);
            cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
            camera.lookAt(cameraTarget);
            if (skyMesh) skyMesh.visible = (camState.clipHeight > 1.35);
            ssaoPass.enabled = (camState.clipHeight > 1.30);

            composer.render();

            const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
            for (let attempt = 0; attempt < 3; attempt++) {
                try {
                    await fetch('/save_snapshot', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ filename: stop.name, image: dataUrl })
                    });
                    console.log(`Saved ${stop.name}`);
                    break;
                } catch (fetchErr) {
                    if (attempt === 2) throw fetchErr;
                    await new Promise(r => setTimeout(r, 200));
                }
            }
            await new Promise(r => setTimeout(r, 100));
        } catch (err) {
            console.error(`Error capturing ${stop.name}:`, err);
        }
    }

    tl.progress(0);
    materialGroup.visible = false;
    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    doorPivot.rotation.y = camState.doorAngle;
    camera.position.set(camState.posX, camState.posY, camState.posZ);
    cameraTarget.set(camState.targetX, camState.targetY, camState.targetZ);
    camera.lookAt(cameraTarget);
    ssaoPass.enabled = false;
    composer.render();
    isCapturing = false;
}

requestAnimationFrame(() => {
    setTimeout(captureCheckpointSnapshots, 400);
});

// Interactive Scrub Buttons for all 8 stops
window.jumpToStop = function(stopIndex) {
    const totalH = window.innerHeight * 8;
    const targets = [
        0,
        totalH * 0.19,
        totalH * 0.31,
        totalH * 0.43,
        totalH * 0.57,
        totalH * 0.71,
        totalH * 0.85,
        totalH * 0.99
    ];
    if (targets[stopIndex] !== undefined) {
        lenis.scrollTo(targets[stopIndex]);
    }
};

// ---------------------------------------------------------
// 19. WINDOW RESIZE HANDLER
// ---------------------------------------------------------
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    ssaoPass.setSize(window.innerWidth, window.innerHeight);
    ScrollTrigger.refresh();
});
''')

    final_content = "".join(parts)
    with open(r"d:\floor plans\jp-aviva-3d\script.js", "w", encoding="utf-8") as out:
        out.write(final_content)
    print("Updated script.js successfully written! Total chars:", len(final_content))

if __name__ == "__main__":
    create_complete_script()
