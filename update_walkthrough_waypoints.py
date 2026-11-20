import os

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update pbrWarmPlasterWall
old_wall = """const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xEAE6DF,
    roughness: 0.85,
    metalness: 0.0,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.003,
    reflectivity: 0.20,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide
});"""

new_wall = """const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({
    color: 0xEAE6DF,
    roughness: 0.85,
    metalness: 0.0,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.003,
    reflectivity: 0.20,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true
});"""

if old_wall in content:
    content = content.replace(old_wall, new_wall, 1)
    print("[OK] Replaced pbrWarmPlasterWall")
else:
    print("[WARN] old_wall not found directly, checking normalized...")
    # Normalize line endings
    content_norm = content.replace("\r\n", "\n")
    if old_wall in content_norm:
        content = content_norm.replace(old_wall, new_wall, 1)
        print("[OK] Replaced pbrWarmPlasterWall with normalized endings")
    else:
        print("[ERROR] Could not find pbrWarmPlasterWall")

# 2. Update pbrMDFSkirting
old_skirt = """const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane]
});"""

new_skirt = """const pbrMDFSkirting = new THREE.MeshPhysicalMaterial({
    color: 0xF2EFE9, // Painted MDF warm off-white satin
    roughness: 0.45,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.25,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

content = content.replace("\r\n", "\n")
if old_skirt in content:
    content = content.replace(old_skirt, new_skirt, 1)
    print("[OK] Replaced pbrMDFSkirting")

# 3. Update pbrWildMushroom
old_mushroom = """const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane]
});"""

new_mushroom = """const pbrWildMushroom = new THREE.MeshPhysicalMaterial({
    color: 0x998878,
    roughness: 0.85,
    bumpMap: stuccoBumpTex,
    bumpScale: 0.008,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true
});"""

if old_mushroom in content:
    content = content.replace(old_mushroom, new_mushroom, 1)
    print("[OK] Replaced pbrWildMushroom")

# 4. Update pbrScandinavianOak
old_oak = """const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
    color: 0xD4B895,
    map: lightOakDiff,
    roughnessMap: lightOakRough,
    normalMap: lightOakNor,
    roughness: 0.52,
    metalness: 0.0,
    clearcoat: 0.20,
    clearcoatRoughness: 0.35,
    clippingPlanes: [clipHeightPlane]
});"""

new_oak = """const pbrScandinavianOak = new THREE.MeshPhysicalMaterial({
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
});"""

if old_oak in content:
    content = content.replace(old_oak, new_oak, 1)
    print("[OK] Replaced pbrScandinavianOak")

# 5. Update pbrBlackQuartz
old_quartz = """const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane]
});"""

new_quartz = """const pbrBlackQuartz = new THREE.MeshPhysicalMaterial({
    color: 0x1A1A1A,
    roughness: 0.12,
    metalness: 0.05,
    clearcoat: 0.90,
    clearcoatRoughness: 0.08,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});"""

if old_quartz in content:
    content = content.replace(old_quartz, new_quartz, 1)
    print("[OK] Replaced pbrBlackQuartz")

# 6. Update pbrCalacattaFloor
old_marble = """const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    map: marbleColorMap,
    roughnessMap: marbleRoughnessMap,
    normalMap: marbleNormalMap,
    roughness: 0.08,
    metalness: 0.0,
    clearcoat: 1.0,
    clearcoatRoughness: 0.08,
    reflectivity: 0.95,
    clippingPlanes: [clipHeightPlane]
});"""

new_marble = """const pbrCalacattaFloor = new THREE.MeshPhysicalMaterial({
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

if old_marble in content:
    content = content.replace(old_marble, new_marble, 1)
    print("[OK] Replaced pbrCalacattaFloor")

# 7. Update pbrCeilingMat
old_ceil = """const pbrCeilingMat = new THREE.MeshPhysicalMaterial({
    color: 0xFAF8F5,
    roughness: 0.88,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide
});"""

new_ceil = """const pbrCeilingMat = new THREE.MeshPhysicalMaterial({
    color: 0xFAF8F5,
    roughness: 0.88,
    metalness: 0.0,
    clippingPlanes: [clipHeightPlane],
    side: THREE.DoubleSide,
    transparent: false,
    depthWrite: true
});"""

if old_ceil in content:
    content = content.replace(old_ceil, new_ceil, 1)
    print("[OK] Replaced pbrCeilingMat")

# 8. Update pbrTravertineTile
old_trav = """const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
    color: 0xF3EFEA,
    map: travertineTileTex,
    roughness: 0.32,
    metalness: 0.02,
    clearcoat: 0.45,
    clearcoatRoughness: 0.18,
    clippingPlanes: [clipHeightPlane]
});"""

new_trav = """const pbrTravertineTile = new THREE.MeshPhysicalMaterial({
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

if old_trav in content:
    content = content.replace(old_trav, new_trav, 1)
    print("[OK] Replaced pbrTravertineTile")

# 9. Replace Timeline from STOP 3 through STOP 7
old_timeline_start = "// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---"
old_timeline_end = "// ----------------------------------------------------------------------------\n// 13. REAL-TIME RENDERING LOOP"

start_idx = content.find(old_timeline_start)
end_idx = content.find(old_timeline_end)

if start_idx != -1 and end_idx != -1:
    new_timeline = """// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
// Leg 3A1 (38% to 41%): Circulate North along Living Room Floor (Open Corridor)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 55.0,
    posX: 0.85,
    posY: 1.55,
    posZ: 0.05,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -1.00,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A2 (41% to 44%): Glide West Cleanly Through Open Portal Arch into Central Passage
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -0.55,
    posY: 1.55,
    posZ: 0.00,
    targetX: -1.00,
    targetY: 1.35,
    targetZ: -1.20,
    duration: 0.03,
    ease: 'power1.inOut'
});
// Leg 3A3 (44% to 46%): Step North to Kitchen Alcove Presentation Portal
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepKitchenZ: -2.35,
    posX: -0.45,
    posY: 1.50,
    posZ: -0.75,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: -1.95,
    duration: 0.02,
    ease: 'power2.out'
});
// Leg 3B (46% to 52%): Kitchen Alcove Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepKitchenZ: -2.35,
    posX: -0.45,
    posY: 1.50,
    posZ: -0.75,
    targetX: -1.15,
    targetY: 1.10,
    targetZ: -1.95,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen into Central Passage (Align with Bath Door)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.55,
    posZ: -0.10,
    targetX: -1.15,
    targetY: 1.40,
    targetZ: 0.80,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Glide Straight South Through Open Bathroom Doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.15,
    posY: 1.50,
    posZ: 0.55,
    targetX: -1.15,
    targetY: 1.25,
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
    targetY: 1.25,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth 'Rise, Glide, Descend' into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%) — RISE & GLIDE OUT OF BATHROOM:
// Camera smoothly rises to 1.65m and glides North out of the bathroom into central passage.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -1.15,
    posY: 1.65,
    posZ: -0.15,
    targetX: -1.85,
    targetY: 1.45,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%) — GLIDE WEST THROUGH OPEN BEDROOM DOORWAY:
// Camera glides cleanly through the open door frame (x = -1.825, z = -0.20).
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.52,
    posZ: -0.15,
    targetX: -2.85,
    targetY: 1.35,
    targetZ: -0.85,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM ENTRANCE:
// Eye level (Y = 1.45m) looking diagonally across the full bed, headboard, warm pendant light, and window!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15,
    posX: -2.20,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.35,
    targetY: 1.25,
    targetZ: -1.35,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBedroomX: -4.15,
    posX: -2.20,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.35,
    targetY: 1.25,
    targetZ: -1.35,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — GLIDE OUT OF BEDROOM INTO PASSAGE:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.55,
    posZ: -0.10,
    targetX: 0.85,
    targetY: 1.50,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%) — GLIDE ACROSS LIVING & BALCONY SLIDERS OPEN:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.55,
    posZ: -0.55,
    targetX: 1.50,
    targetY: 1.40,
    targetZ: -2.20,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%) — STEP ONTO TEAK BALCONY DECK & LEVEL CAMERA HORIZON:
// Eye level Y = 1.45m looking horizontally out through glass toward Mumbai golden-hour skyline (Y = 1.40m)!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.45,
    posZ: -1.65,
    targetX: 1.50,
    targetY: 1.40,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%) — BALCONY DECK STEADY HOLD (Horizontal Horizon Framing):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.45,
    posZ: -1.65,
    targetX: 1.50,
    targetY: 1.40,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---
// Camera glides smoothly forward to the edge of the glass balustrade overlooking panoramic skyline.
tl.to(camState, {
    clipHeight: 2.85,
    fov: 48.0,
    posX: 1.52,
    posY: 1.45,
    posZ: -2.25,
    targetX: 1.52,
    targetY: 1.40,
    targetZ: -8.00,
    balconyDoorX: -0.90,
    duration: 0.08,
    ease: 'power1.out'
});
"""
    content = content[:start_idx] + new_timeline + content[end_idx:]
    print("[OK] Replaced Timeline from Stop 3 to Stop 7")
else:
    print(f"[ERROR] Could not find timeline boundaries: start={start_idx}, end={end_idx}")

# 10. Add solid material enforcement in applyProgressToScene and render
old_mat_vis = "    materialGroup.visible = (camState.clipHeight > 1.25);"
new_mat_vis = """    materialGroup.visible = (camState.clipHeight > 1.25);
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
    }"""

if old_mat_vis in content:
    content = content.replace(old_mat_vis, new_mat_vis)
    print("[OK] Added solid material enforcement in render and applyProgressToScene")

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] script.js updated successfully!")
