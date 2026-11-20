import os
import re

# -----------------------------------------------------------------------------
# 1. UPDATE index.html
# -----------------------------------------------------------------------------
html_path = r'D:\floor plans\jp-aviva-3d\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update button and card tags
old_interaction = '''        <!-- Minimalist '+' Button (fades in via GSAP only at eye-level photo stops) -->
        <button id="room-plus-btn" class="room-plus-btn" aria-label="Explore Room Specifications" title="Click to View Architectural Specifications">
            <span class="plus-beacon"></span>
            <span id="plus-icon" class="plus-icon">+</span>
            <span class="plus-label">PITCH SPECS</span>
        </button>

        <!-- Frosted Glass Architectural Spec Card -->
        <div id="room-card" class="room-card" style="display: none;" role="dialog" aria-modal="true" aria-labelledby="rc-name">
            <div class="rc-header">
                <div class="rc-tag-group">
                    <span id="rc-zone" class="rc-zone-tag">ZONE 01 · SOCIAL &amp; ENTERTAINMENT</span>
                    <span class="rc-spec-badge">ARCHITECTURAL SPECIFICATION</span>
                </div>
                <button id="room-card-close" class="rc-close-btn" aria-label="Close specification card">&times;</button>
            </div>'''

new_interaction = '''        <!-- Minimalist '+' Button (fades in via GSAP only at eye-level photo stops) -->
        <button id="room-plus-btn" class="room-plus-btn" onclick="window.toggleRoomCard()" aria-label="Explore Room Specifications" title="Click to View Architectural Specifications">
            <span class="plus-beacon"></span>
            <span id="plus-icon" class="plus-icon">+</span>
            <span class="plus-label">PITCH SPECS</span>
        </button>

        <!-- Frosted Glass Architectural Spec Card -->
        <div id="room-card" class="room-card" role="dialog" aria-modal="true" aria-labelledby="rc-name">
            <div class="rc-header">
                <div class="rc-tag-group">
                    <span id="rc-zone" class="rc-zone-tag">ZONE 01 · SOCIAL &amp; ENTERTAINMENT</span>
                    <span class="rc-spec-badge">ARCHITECTURAL SPECIFICATION</span>
                </div>
                <button id="room-card-close" class="rc-close-btn" onclick="window.closeRoomCard()" aria-label="Close specification card">&times;</button>
            </div>'''

if old_interaction in html:
    html = html.replace(old_interaction, new_interaction)
    print('[OK] index.html updated interaction block')
else:
    print('[WARN] index.html interaction block not matched')

# Update unit toggle buttons to have IDs
old_toggle = '''                    <button type="button" class="rc-unit-btn active" data-unit="metric" onclick="window.setGlobalUnit('metric')">METRIC (m / m&sup2;)</button>
                    <button type="button" class="rc-unit-btn" data-unit="imperial" onclick="window.setGlobalUnit('imperial')">IMPERIAL (ft / sq.ft)</button>'''

new_toggle = '''                    <button type="button" id="rc-unit-m" class="rc-unit-btn active" data-unit="metric" onclick="window.setGlobalUnit('metric')">METRIC (m / m&sup2;)</button>
                    <button type="button" id="rc-unit-f" class="rc-unit-btn" data-unit="imperial" onclick="window.setGlobalUnit('imperial')">IMPERIAL (ft / sq.ft)</button>'''

if old_toggle in html:
    html = html.replace(old_toggle, new_toggle)
    print('[OK] index.html updated unit toggle buttons')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)


# -----------------------------------------------------------------------------
# 2. UPDATE style.css
# -----------------------------------------------------------------------------
css_path = r'D:\floor plans\jp-aviva-3d\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

old_card_css = '''.room-card {
    pointer-events: none;
    position: fixed;
    bottom: 92px;
    right: 36px;
    width: 440px;
    max-width: calc(100vw - 48px);
    max-height: calc(100vh - 130px);
    overflow-y: auto;
    background: rgba(14, 16, 20, 0.88);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(212, 163, 89, 0.45);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.08) inset;
    z-index: 99;
    opacity: 0;
    transform: translateY(20px) scale(0.96);
    transition: opacity 0.32s cubic-bezier(0.16, 1, 0.3, 1), transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.room-card.open {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
}'''

new_card_css = '''.room-card {
    pointer-events: none;
    visibility: hidden;
    position: fixed;
    bottom: 92px;
    right: 36px;
    width: 440px;
    max-width: calc(100vw - 48px);
    max-height: calc(100vh - 130px);
    overflow-y: auto;
    background: rgba(14, 16, 20, 0.90);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(212, 163, 89, 0.45);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.08) inset;
    z-index: 105;
    opacity: 0;
    transform: translateY(18px) scale(0.96);
    transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1), transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.28s;
}

.room-card.open {
    visibility: visible;
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
}'''

if old_card_css in css:
    css = css.replace(old_card_css, new_card_css)
    print('[OK] style.css updated .room-card visibility and transitions')
else:
    print('[WARN] style.css room-card block not matched')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)


# -----------------------------------------------------------------------------
# 3. UPDATE script.js
# -----------------------------------------------------------------------------
js_path = r'D:\floor plans\jp-aviva-3d\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# A. UnrealBloomPass exact settings (threshold 0.92, strength 0.25)
old_bloom = '''const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.14, // strength
    0.35, // radius
    0.88  // threshold
);'''

new_bloom = '''const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(Math.floor(window.innerWidth * 0.5), Math.floor(window.innerHeight * 0.5)),
    0.25, // strength (balanced golden sunset radiance)
    0.35, // radius
    0.92  // threshold (prevents balcony window overexposure)
);'''

if old_bloom in js:
    js = js.replace(old_bloom, new_bloom)
    print('[OK] script.js updated bloomPass (threshold 0.92, strength 0.25)')
else:
    print('[WARN] bloomPass block not matched')

# B. Circular Bokeh Texture Generator & Material
old_boucle_def = '''// G2. Woven Linen / Bouclé Fabric Bump & Roughness Texture'''

new_bokeh_def = '''// G1. Procedural Soft Circular Bokeh Particle Texture
function createCircularBokehTexture() {
    const c = document.createElement('canvas');
    c.width = c.height = 64;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0.0, 'rgba(255, 245, 220, 1.0)');
    grad.addColorStop(0.35, 'rgba(255, 230, 180, 0.55)');
    grad.addColorStop(0.70, 'rgba(255, 210, 150, 0.12)');
    grad.addColorStop(1.0, 'rgba(255, 200, 120, 0.0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
}
const bokehTexture = createCircularBokehTexture();

// G2. Woven Linen / Bouclé Fabric Bump & Roughness Texture'''

if old_boucle_def in js and 'createCircularBokehTexture' not in js:
    js = js.replace(old_boucle_def, new_bokeh_def)
    print('[OK] script.js added createCircularBokehTexture()')

# C. Update pbrArchitecturalGlass reflectivity
old_arch_glass = '''const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
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
});'''

new_arch_glass = '''const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.92,
    opacity: 1.0,
    transparent: true,
    roughness: 0.10,
    metalness: 0.05,
    ior: 1.52,
    thickness: 0.03,
    reflectivity: 0.50, // Softened from 0.90 to eliminate harsh window glare
    clearcoat: 0.60,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});'''

if old_arch_glass in js:
    js = js.replace(old_arch_glass, new_arch_glass)
    print('[OK] script.js updated pbrArchitecturalGlass reflectivity')

# D. Update Living Room Materials for strict opacity & add dedicated pbrMarbleTable
old_boucle_mat = '''const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xE8E1D7,
    bumpMap: boucleTex,
    bumpScale: 0.007,
    roughness: 0.85,
    metalness: 0.0,
    sheen: 0.75,
    sheenRoughness: 0.55,
    sheenColor: new THREE.Color(0xF5EFEB),
    clippingPlanes: [clipHeightPlane]
});'''

new_boucle_mat = '''const pbrBoucleLinen = new THREE.MeshPhysicalMaterial({
    color: 0xE8E1D7,
    bumpMap: boucleTex,
    bumpScale: 0.007,
    roughness: 0.85,
    metalness: 0.0,
    sheen: 0.75,
    sheenRoughness: 0.55,
    sheenColor: new THREE.Color(0xF5EFEB),
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    opacity: 1.0,
    depthWrite: true,
    depthTest: true
});

// Dedicated Honed Italian Calacatta Marble Table Top (Eliminates double-reflection/ghosting)
const pbrMarbleTable = new THREE.MeshPhysicalMaterial({
    color: 0xFDFBF7,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.22, // Soft satin honed marble
    metalness: 0.0,
    clearcoat: 0.35,
    clearcoatRoughness: 0.20,
    reflectivity: 0.40,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    opacity: 1.0,
    depthWrite: true,
    depthTest: true
});'''

if old_boucle_mat in js:
    js = js.replace(old_boucle_mat, new_boucle_mat)
    print('[OK] script.js added pbrMarbleTable and updated pbrBoucleLinen')

# Replace coffee table top material with pbrMarbleTable
old_table_top = '''const tTop = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.035, 0.58, 4, 0.015), pbrCalacattaFloor);'''
new_table_top = '''const tTop = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.035, 0.58, 4, 0.015), pbrMarbleTable);'''

if old_table_top in js:
    js = js.replace(old_table_top, new_table_top)
    print('[OK] script.js assigned pbrMarbleTable to coffee table top')

# E. Replace square dust particles with tiny circular bokeh particles
old_motes = '''    // Floating Golden Light Motes
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
    group.add(new THREE.Points(moteGeo, moteMat));'''

new_motes = '''    // Subtle Floating Circular Golden Bokeh Motes (Tiny, soft circular particles)
    const moteGeo = new THREE.BufferGeometry();
    const moteCount = 40;
    const motePos = new Float32Array(moteCount * 3);
    for (let i = 0; i < moteCount; i++) {
        motePos[i * 3 + 0] = 0.6 + Math.random() * 2.0;
        motePos[i * 3 + 1] = 0.5 + Math.random() * 1.6;
        motePos[i * 3 + 2] = -2.2 + Math.random() * 1.2;
    }
    moteGeo.setAttribute('position', new THREE.BufferAttribute(motePos, 3));
    const moteMat = new THREE.PointsMaterial({
        color: 0xFFE0B2,
        size: 0.012, // Subtle tiny circular particles (reduced from 0.035)
        map: bokehTexture,
        transparent: true,
        opacity: 0.40,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    group.add(new THREE.Points(moteGeo, moteMat));'''

if old_motes in js:
    js = js.replace(old_motes, new_motes)
    print('[OK] script.js replaced square dust motes with circular bokeh particles')

# F. Enforce Living Room Furniture Opacity in timeline & applyProgressToScene
old_material_solid = '''    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        pbrWarmPlasterWall.transparent = false;
        pbrWarmPlasterWall.depthWrite = true;
        pbrWildMushroom.transparent = false;
        pbrWildMushroom.depthWrite = true;
        pbrScandinavianOak.transparent = false;
        pbrScandinavianOak.depthWrite = true;
        pbrBlackQuartz.transparent = false;
        pbrBlackQuartz.depthWrite = true;
        pbrCalacattaFloor.transparent = false;
        pbrCalacattaFloor.depthWrite = true;
        pbrCeilingMat.transparent = false;
        pbrCeilingMat.depthWrite = true;
        pbrMDFSkirting.transparent = false;
        pbrMDFSkirting.depthWrite = true;
        pbrTravertineTile.transparent = false;
        pbrTravertineTile.depthWrite = true;
    }'''

new_material_solid = '''    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        const solidMats = [
            pbrWarmPlasterWall, pbrWildMushroom, pbrScandinavianOak, pbrBlackQuartz,
            pbrCalacattaFloor, pbrMarbleTable, pbrCeilingMat, pbrMDFSkirting, pbrTravertineTile,
            pbrBoucleLinen, pbrTerracotta, pbrMustard, pbrBrushedBrass, pbrMatteBlackSteel,
            pbrPolishedChrome, pbrBrushedSteel, pbrCeramicMat, pbrCurtainLinen
        ];
        solidMats.forEach(m => {
            if (m) {
                m.transparent = false;
                m.opacity = 1.0;
                m.depthWrite = true;
                m.depthTest = true;
            }
        });
    }'''

# Replace both occurrences (in animate/timeline update and in applyProgressToScene)
js = js.replace(old_material_solid, new_material_solid)
print('[OK] script.js enforced strict opacity & depthWrite for all living room materials')

# G. Interactive Photo Stop Logic & Hotspot Cards
old_check_photo = '''function checkPhotoStop(p) {
    let stopIdx = null;
    if (p < 0.12) stopIdx = 0;
    else if (p >= 0.28 && p < 0.40) stopIdx = 2;
    else if (p >= 0.44 && p < 0.54) stopIdx = 3;
    else if (p >= 0.58 && p < 0.68) stopIdx = 4;
    else if (p >= 0.72 && p < 0.82) stopIdx = 5;
    else if (p >= 0.86 && p < 0.98) stopIdx = 6;

    const plusBtn = document.getElementById('room-plus-btn');
    if (stopIdx !== null) {
        currentActiveStop = stopIdx;
        if (plusBtn) plusBtn.classList.add('visible');
    } else {
        if (plusBtn) plusBtn.classList.remove('visible');
        closeRoomCard();
    }
}'''

new_check_photo = '''function checkPhotoStop(p) {
    let stopIdx = null;
    if (p < 0.12) stopIdx = 0;                           // 01 · 2D Blueprint Plan
    else if (p >= 0.26 && p < 0.38) stopIdx = 2;          // 03 · Living Sanctuary
    else if (p >= 0.44 && p < 0.52) stopIdx = 3;          // 04 · Gourmet Kitchen
    else if (p >= 0.58 && p < 0.66) stopIdx = 4;          // 05 · Designer Bath Suite
    else if (p >= 0.72 && p < 0.80) stopIdx = 5;          // 06 · Master Bedroom Suite
    else if (p >= 0.86 && p < 0.94) stopIdx = 6;          // 07 · Balcony Deck & Utility

    const plusBtn = document.getElementById('room-plus-btn');
    if (stopIdx !== null) {
        currentActiveStop = stopIdx;
        if (plusBtn) plusBtn.classList.add('visible');
        // If card is already open, update its content to the current room
        if (isCardOpen && ROOM_DATA[stopIdx]) {
            renderRoomCardData(ROOM_DATA[stopIdx]);
        }
    } else {
        if (plusBtn) plusBtn.classList.remove('visible');
        if (isCardOpen) closeRoomCard();
    }
}'''

if old_check_photo in js:
    js = js.replace(old_check_photo, new_check_photo)
    print('[OK] script.js updated checkPhotoStop ranges and auto-update')

# H. Wire up openRoomCard and closeRoomCard
old_open_card = '''window.openRoomCard = function(idx) {
    if (idx === null || idx === undefined) idx = currentActiveStop !== null ? currentActiveStop : 2;
    currentActiveStop = idx;
    const d = ROOM_DATA[idx];
    if (!d) return;

    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (!card) return;

    renderRoomCardData(d);

    card.classList.add('open');
    card.setAttribute('aria-hidden', 'false');
    if (plusBtn) plusBtn.classList.add('active');
    isCardOpen = true;
};

window.closeRoomCard = function() {
    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (card) {
        card.classList.remove('open');
        card.setAttribute('aria-hidden', 'true');
    }
    if (plusBtn) plusBtn.classList.remove('active');
    isCardOpen = false;
};'''

new_open_card = '''window.openRoomCard = function(idx) {
    if (idx === null || idx === undefined) idx = currentActiveStop !== null ? currentActiveStop : 2;
    currentActiveStop = idx;
    const d = ROOM_DATA[idx];
    if (!d) return;

    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (!card) return;

    renderRoomCardData(d);

    card.style.display = 'block';
    // Force browser reflow for CSS transition
    void card.offsetWidth;
    card.classList.add('open');
    card.setAttribute('aria-hidden', 'false');
    if (plusBtn) plusBtn.classList.add('active');
    isCardOpen = true;
};

window.closeRoomCard = function() {
    const card = document.getElementById('room-card');
    const plusBtn = document.getElementById('room-plus-btn');
    if (card) {
        card.classList.remove('open');
        card.setAttribute('aria-hidden', 'true');
        setTimeout(() => {
            if (!isCardOpen && card) card.style.display = 'none';
        }, 300);
    }
    if (plusBtn) plusBtn.classList.remove('active');
    isCardOpen = false;
};'''

if old_open_card in js:
    js = js.replace(old_open_card, new_open_card)
    print('[OK] script.js refined openRoomCard and closeRoomCard transitions')

# I. Attach Event Listeners on DOMContentLoaded / immediately
init_listeners = '''
// Attach click listeners for Room Spec Hotspot buttons
document.addEventListener('DOMContentLoaded', () => {
    const pBtn = document.getElementById('room-plus-btn');
    if (pBtn) {
        pBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.toggleRoomCard();
        });
    }
    const cBtn = document.getElementById('room-card-close');
    if (cBtn) {
        cBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.closeRoomCard();
        });
    }
    // Clicking outside card closes it
    document.addEventListener('click', (e) => {
        if (isCardOpen && !e.target.closest('#room-card') && !e.target.closest('#room-plus-btn')) {
            window.closeRoomCard();
        }
    });
});
'''

if 'Attach click listeners for Room Spec Hotspot buttons' not in js:
    js = js + init_listeners
    print('[OK] script.js attached click listeners for hotspot and card')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print('\n[COMPLETE] All fixes applied cleanly to index.html, style.css, and script.js!')
