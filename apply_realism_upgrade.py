import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings to LF for replacements then back to CRLF
is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# 1. Environment Map & Tone Mapping
old_env = """renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.localClippingEnabled = true;

// Continuous 3D camera pass with strict frame clearing (zero accumulation or ghosting)
renderer.autoClear = true;
renderer.autoClearColor = true;
renderer.autoClearDepth = true;
renderer.autoClearStencil = true;

RectAreaLightUniformsLib.init();
const maxAniso = renderer.capabilities.getMaxAnisotropy();

// ----------------------------------------------------------------------------
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
scene.environmentIntensity = 0.95;"""

new_env = """renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.10;
renderer.localClippingEnabled = true;

// Continuous 3D camera pass with strict frame clearing (zero accumulation or ghosting)
renderer.autoClear = true;
renderer.autoClearColor = true;
renderer.autoClearDepth = true;
renderer.autoClearStencil = true;

RectAreaLightUniformsLib.init();
const maxAniso = renderer.capabilities.getMaxAnisotropy();

// ----------------------------------------------------------------------------
// 3. HIGH-CONTRAST INTERIOR-WARM PMREM GENERATOR ENVIRONMENT MAP (RoomEnvironment + Warm Window Emitters)
// ----------------------------------------------------------------------------
function createNeutralWarmEnvironment(renderer) {
    const pmrem = new THREE.PMREMGenerator(renderer);
    pmrem.compileEquirectangularShader();

    // High-contrast interior room environment scene
    const envScene = new RoomEnvironment(renderer);

    // 1. Warm Golden Hour Balcony Window Emitter Panel
    const windowEmitterGeo = new THREE.PlaneGeometry(16, 12);
    const windowEmitterMat = new THREE.MeshBasicMaterial({
        color: 0xFFD89B, // Radiant warm golden sunlight
        side: THREE.DoubleSide
    });
    const windowEmitter = new THREE.Mesh(windowEmitterGeo, windowEmitterMat);
    windowEmitter.position.set(12, 8, -14);
    windowEmitter.lookAt(0, 0, 0);
    envScene.add(windowEmitter);

    // 2. High-key softbox ceiling panel for crisp linear specular highlights on marble, glass & faucets
    const softboxGeo = new THREE.PlaneGeometry(18, 14);
    const softboxMat = new THREE.MeshBasicMaterial({
        color: 0xFFF8F0,
        side: THREE.DoubleSide
    });
    const softbox = new THREE.Mesh(softboxGeo, softboxMat);
    softbox.position.set(0, 16, 0);
    softbox.rotation.x = Math.PI / 2;
    envScene.add(softbox);

    // 3. Warm taupe / honey oak floor bounce panel
    const floorBounceGeo = new THREE.PlaneGeometry(24, 24);
    const floorBounceMat = new THREE.MeshBasicMaterial({
        color: 0xB89D82,
        side: THREE.DoubleSide
    });
    const floorBounce = new THREE.Mesh(floorBounceGeo, floorBounceMat);
    floorBounce.position.set(0, -12, 0);
    floorBounce.rotation.x = -Math.PI / 2;
    envScene.add(floorBounce);

    const envTexture = pmrem.fromScene(envScene, 0.04).texture;
    pmrem.dispose();
    return envTexture;
}

const envMap = createNeutralWarmEnvironment(renderer);
scene.environment = envMap;
scene.environmentIntensity = 1.0;"""

assert old_env in c, 'old_env not found'
c = c.replace(old_env, new_env)

# 2. Procedural Venetian Plaster Textures
old_stucco = """// D. Procedural Stucco Wall Bump Texture
function createProceduralStuccoTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const ctx = c.getContext('2d');
    const id = ctx.createImageData(512, 512);
    for (let i = 0; i < id.data.length; i += 4) {
        const v = 200 + Math.floor(Math.random() * 55);
        id.data[i] = id.data[i+1] = id.data[i+2] = v;
        id.data[i+3] = 255;
    }
    ctx.putImageData(id, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const stuccoBumpTex = createProceduralStuccoTexture();"""

new_stucco = """// D. Procedural Venetian Plaster & Warm Stucco Texture Generators (Albedo + Bump + Roughness)
function createVenetianPlasterTextures() {
    const w = 1024, h = 1024;
    
    // 1. Albedo Canvas (Handcrafted multi-pass Italian trowel marbling)
    const cAlbedo = document.createElement('canvas');
    cAlbedo.width = w; cAlbedo.height = h;
    const ctxA = cAlbedo.getContext('2d');
    
    // Warm alabaster / Roman lime plaster base (#EAE6DF)
    ctxA.fillStyle = '#EAE6DF';
    ctxA.fillRect(0, 0, w, h);

    // Multi-pass broad trowel strokes and smooth cloudy variations
    for (let pass = 0; pass < 28; pass++) {
        const rad = 140 + Math.random() * 260;
        const cx = Math.random() * w;
        const cy = Math.random() * h;
        const grad = ctxA.createRadialGradient(cx, cy, 10, cx, cy, rad);
        const warmDelta = (Math.random() - 0.5) * 14;
        const r = Math.round(236 + warmDelta);
        const g = Math.round(232 + warmDelta);
        const b = Math.round(224 + warmDelta * 0.85);
        grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${0.12 + Math.random() * 0.16})`);
        grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);
        ctxA.fillStyle = grad;
        ctxA.beginPath();
        ctxA.ellipse(cx, cy, rad, rad * 0.65, Math.random() * Math.PI, 0, Math.PI * 2);
        ctxA.fill();
    }

    // Directional trowel blade sweeps
    for (let s = 0; s < 40; s++) {
        ctxA.strokeStyle = `rgba(222, 216, 206, ${0.08 + Math.random() * 0.12})`;
        ctxA.lineWidth = 14 + Math.random() * 32;
        ctxA.beginPath();
        let sx = Math.random() * w;
        let sy = Math.random() * h;
        ctxA.moveTo(sx, sy);
        ctxA.bezierCurveTo(sx + 120, sy + 35, sx + 240, sy - 25, sx + 360, sy + 45);
        ctxA.stroke();
    }

    // Micro-mineral grain
    const imgData = ctxA.getImageData(0, 0, w, h);
    const data = imgData.data;
    for (let i = 0; i < data.length; i += 4) {
        const grain = (Math.random() - 0.5) * 6;
        data[i] = Math.min(255, Math.max(0, data[i] + grain));
        data[i+1] = Math.min(255, Math.max(0, data[i+1] + grain));
        data[i+2] = Math.min(255, Math.max(0, data[i+2] + grain * 0.7));
    }
    ctxA.putImageData(imgData, 0, 0);

    const albedoTex = new THREE.CanvasTexture(cAlbedo);
    albedoTex.wrapS = albedoTex.wrapT = THREE.RepeatWrapping;
    albedoTex.repeat.set(4, 4);
    albedoTex.colorSpace = THREE.SRGBColorSpace;
    albedoTex.anisotropy = maxAniso;

    // 2. Bump Map Canvas (fine mineral grain & subtle trowel edge relief)
    const cBump = document.createElement('canvas');
    cBump.width = w; cBump.height = h;
    const ctxB = cBump.getContext('2d');
    ctxB.fillStyle = '#808080';
    ctxB.fillRect(0, 0, w, h);
    const bumpData = ctxB.getImageData(0, 0, w, h);
    for (let i = 0; i < bumpData.data.length; i += 4) {
        const n = 128 + Math.floor((Math.random() - 0.5) * 26);
        bumpData.data[i] = bumpData.data[i+1] = bumpData.data[i+2] = n;
        bumpData.data[i+3] = 255;
    }
    ctxB.putImageData(bumpData, 0, 0);

    for (let s = 0; s < 32; s++) {
        ctxB.strokeStyle = `rgba(${128 + Math.floor((Math.random() - 0.5) * 44)}, 128, 128, 0.28)`;
        ctxB.lineWidth = 6 + Math.random() * 10;
        ctxB.beginPath();
        let sx = Math.random() * w;
        let sy = Math.random() * h;
        ctxB.moveTo(sx, sy);
        ctxB.quadraticCurveTo(sx + 90, sy + 45, sx + 220, sy + 15);
        ctxB.stroke();
    }

    const bumpTex = new THREE.CanvasTexture(cBump);
    bumpTex.wrapS = bumpTex.wrapT = THREE.RepeatWrapping;
    bumpTex.repeat.set(4, 4);

    return { albedo: albedoTex, bump: bumpTex };
}
const venetianPlasterTex = createVenetianPlasterTextures();
const stuccoBumpTex = venetianPlasterTex.bump;"""

assert old_stucco in c, 'old_stucco not found'
c = c.replace(old_stucco, new_stucco)

# 3. Contact Blob Shadow Generator & Exemption Tagging
old_blob = """// H. Contact Blob Shadow Generator
function createContactBlobShadowTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    grad.addColorStop(0, 'rgba(10, 8, 5, 0.75)');
    grad.addColorStop(0.45, 'rgba(15, 12, 8, 0.40)');
    grad.addColorStop(0.80, 'rgba(25, 20, 15, 0.12)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
}
const blobShadowTex = createContactBlobShadowTexture();

function createBlobShadow(w, d, x, z, parentGroup, opacity = 0.38) {
    const geo = new THREE.PlaneGeometry(w, d);
    geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({
        map: blobShadowTex,
        transparent: true,
        opacity: opacity,
        depthWrite: false,
        clippingPlanes: [clipHeightPlane]
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(x, 0.003, z);
    parentGroup.add(mesh);
    return mesh;
}"""

new_blob = """// H. Contact Blob Shadow Generator
function createContactBlobShadowTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    grad.addColorStop(0, 'rgba(10, 8, 5, 0.75)');
    grad.addColorStop(0.45, 'rgba(15, 12, 8, 0.40)');
    grad.addColorStop(0.80, 'rgba(25, 20, 15, 0.12)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 256, 256);
    const tex = new THREE.CanvasTexture(c);
    tex.name = 'blobShadow';
    return tex;
}
const blobShadowTex = createContactBlobShadowTexture();
blobShadowTex.name = 'blobShadow';

function createBlobShadow(w, d, x, z, parentGroup, opacity = 0.38) {
    const geo = new THREE.PlaneGeometry(w, d);
    geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({
        map: blobShadowTex,
        transparent: true,
        opacity: opacity,
        depthWrite: false,
        clippingPlanes: [clipHeightPlane]
    });
    mat.name = 'blobShadowMat';
    mat.isBlobShadow = true;
    const mesh = new THREE.Mesh(geo, mat);
    mesh.name = 'blobShadowMesh';
    mesh.isBlobShadow = true;
    mesh.position.set(x, 0.003, z);
    parentGroup.add(mesh);
    return mesh;
}"""

assert old_blob in c, 'old_blob not found'
c = c.replace(old_blob, new_blob)

# 4. PBR Materials Upgrade
old_mats = """// Warm off-white matte plaster / eggshell paint (#EAE6DF, roughness: 0.85, metalness: 0.0)
const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xEAE6DF,
    roughness: 0.85,
    metalness: 0.0,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.003,
    reflectivity: 0.20,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide,
    transparent: false,
    depthWrite: true
});

const pbrWhisperingSmoke = pbrWarmPlasterWall;

const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});



const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true
});

const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.52,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.35,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.08,
    metalness: 0.0,
    clearcoat: 1.0,
    clearcoatRoughness: 0.08,
    reflectivity: 0.95,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

new_mats = """// Warm Venetian lime plaster / Italian stucco paint (#EAE6DF, roughness: 0.82, metalness: 0.0)
const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: venetianPlasterTex.albedo,
    bumpMap: venetianPlasterTex.bump,
    bumpScale: 0.0035,
    roughness: 0.82,
    metalness: 0.0,
    reflectivity: 0.25,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide,
    transparent: false,
    depthWrite: true
});

const pbrWhisperingSmoke = pbrWarmPlasterWall;

const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});



const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true
});

const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.48,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.28,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Authentic Honed Italian Vitrified Floor Tiles (roughness: 0.22, clearcoat: 0.40)
const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.22,
    metalness: 0.0,
    clearcoat: 0.40,
    clearcoatRoughness: 0.15,
    reflectivity: 0.85,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

assert old_mats in c, 'old_mats not found'
c = c.replace(old_mats, new_mats)

# 5. Wardrobe Shadow Plane
old_wardrobe = """        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);"""

new_wardrobe = """        wardrobeGroup.add(handle);
    }
    group.add(wardrobeGroup);
    // Grounded contact shadow plane under built-in wardrobe
    createBlobShadow(0.70, 1.75, -3.95, -1.50, group, 0.42);"""

assert old_wardrobe in c, 'old_wardrobe not found'
c = c.replace(old_wardrobe, new_wardrobe)

# 6. Balcony Armchair & Bistro Table Shadow Planes (Eliminates Stray Black Diamond at 17% Scroll!)
old_balc = """    // 3. Contemporary Woven Rope Outdoor Armchair
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.40, 0, -1.95);
    chairGroup.rotation.y = -Math.PI / 4;

    const acFrame = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.65, 0.62, 4, 0.02), pbrMatteBlackSteel);
    acFrame.position.set(0, 0.35, 0);
    acFrame.castShadow = true;
    chairGroup.add(acFrame);

    const acCushion = new THREE.Mesh(new RoundedBoxGeometry(0.54, 0.12, 0.54, 4, 0.03), pbrBoucleLinen);
    acCushion.position.set(0, 0.32, 0);
    chairGroup.add(acCushion);

    createBlobShadow(0.72, 0.72, 2.40, -1.75, chairGroup, 0.38);
    group.add(chairGroup);

    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups (Elevated to 0.72m standard architectural height)
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.70, 0.72, -1.95);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.71, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.70, 0.355, -1.95);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.70 + Math.cos(cAngle) * 0.12, 0.75, -1.95 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }
    createBlobShadow(0.55, 0.55, 1.65, -1.75, bTableGroup, 0.35);
    group.add(bTableGroup);"""

new_balc = """    // 3. Contemporary Woven Rope Outdoor Armchair
    const chairGroup = new THREE.Group();
    chairGroup.position.set(2.40, 0, -1.95);
    chairGroup.rotation.y = -Math.PI / 4;

    const acFrame = new THREE.Mesh(new RoundedBoxGeometry(0.62, 0.65, 0.62, 4, 0.02), pbrMatteBlackSteel);
    acFrame.position.set(0, 0.35, 0);
    acFrame.castShadow = true;
    chairGroup.add(acFrame);

    const acCushion = new THREE.Mesh(new RoundedBoxGeometry(0.54, 0.12, 0.54, 4, 0.03), pbrBoucleLinen);
    acCushion.position.set(0, 0.32, 0);
    chairGroup.add(acCushion);

    group.add(chairGroup);
    // Grounded contact shadow directly at world position of the armchair on the balcony floor
    createBlobShadow(0.72, 0.72, 2.40, -1.95, group, 0.38);

    // 4. Terrazzo Bistro Table with 2 Ceramic Espresso Cups (Elevated to 0.72m standard architectural height)
    const bTableGroup = new THREE.Group();
    const bTable = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.025, 24), pbrCalacattaFloor);
    bTable.position.set(1.70, 0.72, -1.95);
    bTable.castShadow = true;
    bTableGroup.add(bTable);

    const bLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.71, 16), pbrMatteBlackSteel);
    bLeg.position.set(1.70, 0.355, -1.95);
    bLeg.castShadow = true;
    bTableGroup.add(bLeg);

    for (let cAngle of [0.5, 2.5]) {
        const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.02, 0.045, 12), pbrWhisperingSmoke);
        cup.position.set(1.70 + Math.cos(cAngle) * 0.12, 0.75, -1.95 + Math.sin(cAngle) * 0.12);
        bTableGroup.add(cup);
    }
    group.add(bTableGroup);
    // Grounded contact shadow directly at world position of bistro table
    createBlobShadow(0.55, 0.55, 1.70, -1.95, group, 0.35);"""

assert old_balc in c, 'old_balc not found'
c = c.replace(old_balc, new_balc)

# 7. Enforce Opaque Materials Exemption for Blob Shadows
old_enforce = """function enforceOpaqueMaterials() {
    materialGroup.traverse(child => {
        if (!child.isMesh || !child.material) return;
        const mats = Array.isArray(child.material) ? child.material : [child.material];
        for (const m of mats) {
            if (!m) continue;
            // Exempt only genuine architectural glass, curtains, amber cosmetic bottles, and ground shadow planes
            if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass ||
                m === pbrSheerCurtain || m === pbrAmberGlass || (m.map && m.map.name === 'blobShadow')) {
                continue;
            }
            m.transparent = false;
            m.opacity = 1.0;
            m.depthWrite = true;
            m.depthTest = true;
            if (m !== pbrCeilingMat) {
                m.side = THREE.DoubleSide;
            } else {
                m.side = THREE.FrontSide;
            }
        }
    });
}"""

new_enforce = """function enforceOpaqueMaterials() {
    materialGroup.traverse(child => {
        if (!child.isMesh || !child.material) return;
        const mats = Array.isArray(child.material) ? child.material : [child.material];
        for (const m of mats) {
            if (!m) continue;
            // Exempt only genuine architectural glass, curtains, amber cosmetic bottles, and ground shadow planes
            if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass ||
                m === pbrSheerCurtain || m === pbrAmberGlass || m.isBlobShadow || child.isBlobShadow ||
                m.name === 'blobShadowMat' || (m.map && m.map.name === 'blobShadow')) {
                continue;
            }
            m.transparent = false;
            m.opacity = 1.0;
            m.depthWrite = true;
            m.depthTest = true;
            if (m !== pbrCeilingMat) {
                m.side = THREE.DoubleSide;
            } else {
                m.side = THREE.FrontSide;
            }
        }
    });
}"""

assert old_enforce in c, 'old_enforce not found'
c = c.replace(old_enforce, new_enforce)

# Restore CRLF if needed
if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully applied all 7 realism upgrades to script.js!')
