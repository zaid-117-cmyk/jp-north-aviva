# apply_fixes.py
import re

with open('D:/floor plans/jp-aviva-3d/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Renderer autoClear and preserveDrawingBuffer: false
old_renderer = '''const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.0));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.localClippingEnabled = true;'''

new_renderer = '''const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    preserveDrawingBuffer: false, // Prevents frame-accumulation ghosting across room transitions
    powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.0));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.localClippingEnabled = true;

// Continuous 3D camera pass with strict frame clearing (zero accumulation or ghosting)
renderer.autoClear = true;
renderer.autoClearColor = true;
renderer.autoClearDepth = true;
renderer.autoClearStencil = true;'''

assert old_renderer in code, "old_renderer not found"
code = code.replace(old_renderer, new_renderer, 1)

# 2. RenderPass clear settings
old_renderpass = '''const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);'''

new_renderpass = '''const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
renderPass.clear = true;
renderPass.clearDepth = true;
composer.addPass(renderPass);'''

assert old_renderpass in code, "old_renderpass not found"
code = code.replace(old_renderpass, new_renderpass, 1)

# 3. TV Wall and Open Portal Dimensions
old_tvwall = '''// --- Interior Partitions & Real Architectural Door Openings ---
// 1. Living Room to Central Passage Partition (x = 0.125)
// Solid wall separating Living from W.C. & Foyer (z = 0.25 to 1.45, length = 1.20m)
addWall(0.15, WALL_H, 1.20, 0.125, WALL_H / 2, 0.85);
// Lintel overhead across the open passage portal (y = 2.10m to 2.85m, z = -0.65 to 0.25)
addWall(0.15, 0.75, 0.90, 0.125, WALL_H - 0.375, -0.20);
// NOTE: Space from y = 0.0 to 2.10m between z = -0.65 and 0.25 is OPEN for uninterrupted passage.'''

new_tvwall = '''// --- Interior Partitions & Real Architectural Door Openings ---
// 1. Living Room to Central Passage Partition (x = 0.125)
// Solid wall separating Living from W.C. & Central Corridor (z = -0.05 to 1.55, length = 1.60m)
addWall(0.15, WALL_H, 1.60, 0.125, WALL_H / 2, 0.75);
// Lintel overhead across the open passage portal (y = 2.10m to 2.85m, z = -1.15 to -0.05, length = 1.10m)
addWall(0.15, 0.75, 1.10, 0.125, WALL_H - 0.375, -0.60);
// NOTE: Space from y = 0.0 to 2.10m between z = -1.15 and -0.05 is completely OPEN (1.10m wide corridor) for smooth circulation.'''

assert old_tvwall in code, "old_tvwall not found"
code = code.replace(old_tvwall, new_tvwall, 1)

# 4. Skirting along TV wall
old_skirting = '''// Living & Dining Sanctuary junctions
addSkirting(0.03, 3.90, 2.93, 0.95);  // East wall
addSkirting(0.03, 2.70, 0.22, 0.55);  // West partition'''

new_skirting = '''// Living & Dining Sanctuary junctions
addSkirting(0.03, 3.90, 2.93, 0.95);  // East wall
addSkirting(0.03, 1.60, 0.21, 0.75);  // West TV partition (Living Room side)
addSkirting(0.03, 1.60, 0.04, 0.75);  // West TV partition (Passage side)'''

assert old_skirting in code, "old_skirting not found"
code = code.replace(old_skirting, new_skirting, 1)

# 5. TV Group and Media Console
old_tvgroup_pattern = re.compile(
    r'    // 1\. 65" Ultra-Thin 4K OLED Smart TV with Art Canvas & Ambilight Wall Glow.*?'
    r'    group\.add\(tvGroup\);',
    re.DOTALL
)

new_tvgroup = '''    // 1. 65" Ultra-Thin 4K OLED Smart TV with Luxury Fluted Oak Feature Wall & Ambilight Wall Glow
    const tvGroup = new THREE.Group();

    // Architectural Acoustic Fluted Oak Backing Panel (completely backs the TV against the solid wall)
    const tvBackingPanel = new THREE.Mesh(new THREE.BoxGeometry(0.015, 1.30, 1.50), pbrScandinavianOak);
    tvBackingPanel.position.set(0.208, 1.45, 0.75);
    tvBackingPanel.castShadow = true;
    tvGroup.add(tvBackingPanel);

    const tvFrame = new THREE.Mesh(new THREE.BoxGeometry(0.015, 0.82, 1.36), pbrMatteBlackSteel);
    tvFrame.position.set(0.222, 1.45, 0.75);
    tvFrame.castShadow = true;
    tvGroup.add(tvFrame);

    const tvScreenMat = new THREE.MeshBasicMaterial({
        map: tvArtTex,
        clippingPlanes: [clipHeightPlane]
    });
    const tvScreen = new THREE.Mesh(new THREE.PlaneGeometry(1.34, 0.80), tvScreenMat);
    tvScreen.rotateY(Math.PI / 2);
    tvScreen.position.set(0.231, 1.45, 0.75);
    tvGroup.add(tvScreen);

    const tvAmbiLight = new THREE.PointLight(0xFFB066, 1.2, 2.2, 2.0);
    tvAmbiLight.position.set(0.21, 1.45, 0.75);
    tvGroup.add(tvAmbiLight);

    const soundbar = new THREE.Mesh(new RoundedBoxGeometry(0.07, 0.055, 0.95, 4, 0.01), pbrMatteBlackSteel);
    soundbar.position.set(0.25, 0.98, 0.75);
    soundbar.castShadow = true;
    tvGroup.add(soundbar);

    const sbLed = new THREE.Mesh(new THREE.SphereGeometry(0.004, 8, 8), new THREE.MeshBasicMaterial({ color: 0x3399FF }));
    sbLed.position.set(0.29, 0.98, 0.75);
    tvGroup.add(sbLed);

    // Floating Oak Media Console Cabinet (1.50m long, centered at z=0.75, 100% inside the 1.60m wall)
    const consoleBox = new THREE.Mesh(new RoundedBoxGeometry(0.36, 0.30, 1.50, 4, 0.02), pbrScandinavianOak);
    consoleBox.position.set(0.39, 0.46, 0.75);
    consoleBox.castShadow = true;
    tvGroup.add(consoleBox);
    createBlobShadow(0.46, 1.60, 0.39, 0.75, tvGroup, 0.42);
    group.add(tvGroup);'''

match = old_tvgroup_pattern.search(code)
assert match is not None, "old_tvgroup_pattern not found"
code = code[:match.start()] + new_tvgroup + code[match.end():]

# 6. Waypoints for Living -> Kitchen Transition (Leg 3A1, 3A2)
old_leg3 = '''// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
// Leg 3A1 (38% to 41%): Circulate North along Living Room Floor (Open Corridor)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: 0.85,
    posY: 1.55,
    posZ: 0.05,
    targetX: 0.20,
    targetY: 1.45,
    targetZ: -0.15,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A2 (41% to 44%): Glide West Cleanly Through Open Portal Arch into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -0.45,
    posY: 1.55,
    posZ: -0.15,
    targetX: -0.80,
    targetY: 1.35,
    targetZ: -1.60,
    duration: 0.03,
    ease: 'power1.inOut'
});'''

new_leg3 = '''// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
// Leg 3A1 (38% to 41%): Circulate North along Living Room Floor (Open Corridor)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: 0.85,
    posY: 1.55,
    posZ: -0.45,
    targetX: 0.10,
    targetY: 1.45,
    targetZ: -0.55,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A2 (41% to 44%): Glide West Cleanly Through Open Portal Arch into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -0.50,
    posY: 1.55,
    posZ: -0.55,
    targetX: -0.80,
    targetY: 1.35,
    targetZ: -1.60,
    duration: 0.03,
    ease: 'power1.inOut'
});'''

assert old_leg3 in code, "old_leg3 not found"
code = code.replace(old_leg3, new_leg3, 1)

# 7. Waypoints for Master Bedroom -> Balcony Transition (Leg 6A1, 6A2, 6A3)
old_leg6 = '''// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.85,
    posY: 1.50,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch towards Balcony
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 0.95,
    posY: 1.48,
    posZ: -0.55,
    targetX: 1.75,
    targetY: 1.20,
    targetZ: -3.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Approach Open Balcony French Slider Threshold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -0.85,
    targetX: 1.85,
    targetY: 1.08,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});'''

new_leg6 = '''// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Central Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.50,
    posY: 1.50,
    posZ: -0.55,
    targetX: 1.20,
    targetY: 1.35,
    targetZ: -0.55,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Open Portal into Living Room Corridor
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    posX: 1.10,
    posY: 1.48,
    posZ: -0.55,
    targetX: 1.65,
    targetY: 1.20,
    targetZ: -2.80,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Approach Open Balcony French Slider Threshold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBalconyZ: -2.35,
    posX: 1.05,
    posY: 1.48,
    posZ: -0.85,
    targetX: 1.85,
    targetY: 1.08,
    targetZ: -4.50,
    balconyDoorX: 1.18,
    duration: 0.03,
    ease: 'power2.out'
});'''

assert old_leg6 in code, "old_leg6 not found"
code = code.replace(old_leg6, new_leg6, 1)

# 8. Define global enforceOpaqueMaterials() and update render() and applyProgressToScene()
old_traverse_pattern = '''    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        materialGroup.traverse(child => {
            if (child.isMesh && child.material) {
                const m = child.material;
                if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass ||
                    m === pbrSheerCurtain || m === pbrAmberGlass || (m.map && m.map.name === 'blobShadow')) {
                    return;
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
    }'''

new_traverse_render = '''    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        enforceOpaqueMaterials();
    }'''

assert old_traverse_pattern in code, "old_traverse_pattern not found"
# Replace in both render() and applyProgressToScene()
code = code.replace(old_traverse_pattern, new_traverse_render)

# Add enforceOpaqueMaterials helper definition right above render()
helper_func = '''// ----------------------------------------------------------------------------
// ENFORCE 100% OPAQUE INTERIOR MATERIALS (Zero X-Ray / Bleed-Through)
// ----------------------------------------------------------------------------
function enforceOpaqueMaterials() {
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
}

function render() {'''

assert 'function render() {' in code, "function render() not found"
code = code.replace('function render() {', helper_func, 1)

with open('D:/floor plans/jp-aviva-3d/script.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: All ghosting and waypoint fixes cleanly applied to script.js!")
