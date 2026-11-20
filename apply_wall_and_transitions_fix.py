import re

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update pbrWarmPlasterWall to THREE.DoubleSide
content = content.replace(
    'const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({\n    color: 0xEAE6DF,\n    roughness: 0.85,\n    metalness: 0.0,\n    bumpMap: stuccoBumpTex,\n    bumpScale: 0.003,\n    reflectivity: 0.20,\n    clippingPlanes: [clipHeightPlane],\n    side: THREE.FrontSide,\n    transparent: false,\n    depthWrite: true\n});',
    'const pbrWarmPlasterWall = new THREE.MeshPhysicalMaterial({\n    color: 0xEAE6DF,\n    roughness: 0.85,\n    metalness: 0.0,\n    bumpMap: stuccoBumpTex,\n    bumpScale: 0.003,\n    reflectivity: 0.20,\n    clippingPlanes: [clipHeightPlane],\n    side: THREE.DoubleSide,\n    transparent: false,\n    depthWrite: true\n});'
)

# 2. Update Master Bedroom Headboard & East Nightstand
old_headboard = '''    // Padded "Wild Mushroom" Upholstered Headboard
    const headboard = new THREE.Mesh(new RoundedBoxGeometry(2.35, 1.15, 0.10, 6, 0.03), pbrWildMushroom);
    headboard.position.set(-2.95, 0.85, 0.18);'''

new_headboard = '''    // Padded "Wild Mushroom" Upholstered Headboard (Centered 2.05m width, leaving ample clearance to doorway)
    const headboard = new THREE.Mesh(new RoundedBoxGeometry(2.05, 1.15, 0.10, 6, 0.03), pbrWildMushroom);
    headboard.position.set(-3.05, 0.85, 0.18);'''

content = content.replace(old_headboard, new_headboard)

old_nightstand = '''    // 2. Twin Floating Nightstands & Suspended Brass Pendants
    for (let nx of [-4.00, -1.90]) {'''

new_nightstand = '''    // 2. Twin Floating Nightstands & Suspended Brass Pendants (East nightstand cleared 22cm from doorway threshold)
    for (let nx of [-4.05, -2.05]) {'''

content = content.replace(old_nightstand, new_nightstand)

# 3. Update Camera Timeline (Stops 3, 4, 5, 6)
old_timeline_pattern = re.compile(
    r'// --- STOP 3: 38% to 52% \(Walk into Gourmet Kitchen Alcove\) ---.*?// --- STOP 7: 92% to 100% \(MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING\) ---',
    re.DOTALL
)

new_timeline_code = '''// --- STOP 3: 38% to 52% (Walk into Gourmet Kitchen Alcove) ---
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
});
// Leg 3A3 (44% to 46%): Step North Through Kitchen Portal Opening to Presentation Framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 66.0,
    sweepKitchenZ: -2.35,
    posX: -0.55,
    posY: 1.48,
    posZ: -0.65,
    targetX: -0.80,
    targetY: 1.12,
    targetZ: -2.05,
    duration: 0.02,
    ease: 'power2.out'
});
// Leg 3B (46% to 52%): Kitchen Alcove Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 66.0,
    sweepKitchenZ: -2.35,
    posX: -0.55,
    posY: 1.48,
    posZ: -0.65,
    targetX: -0.80,
    targetY: 1.12,
    targetZ: -2.05,
    duration: 0.06,
    ease: 'none'
});

// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: -1.05,
    posY: 1.52,
    posZ: -0.10,
    targetX: -1.18,
    targetY: 1.25,
    targetZ: 0.90,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Glide South Through Open Bathroom Doorway into Full Composition View
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.18,
    targetY: 1.18,
    targetZ: 1.35,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold (Full Architecture Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 62.0,
    sweepBathroomZ: 0.40,
    posX: -1.18,
    posY: 1.48,
    posZ: 0.45,
    targetX: -1.18,
    targetY: 1.18,
    targetZ: 1.35,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.18,
    posY: 1.52,
    posZ: -0.15,
    targetX: -2.50,
    targetY: 1.35,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%): Glide West Straight Through Open Bedroom Doorway (x = -1.825, z = -0.20)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.85,
    posY: 1.50,
    posZ: -0.20,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%): Settle at Doorway Framing (Diagonally Across Bed, Headboard, Wardrobe & Window)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.50,
    posZ: -0.28,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%): Master Bedroom Steady Hold (Open & Naturally Lit Doorway Perspective)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.50,
    posZ: -0.28,
    targetX: -3.35,
    targetY: 1.15,
    targetZ: -1.05,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth Circulation to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%): Glide East Cleanly out of Bedroom Doorway into Passage Hub
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.85,
    targetY: 1.45,
    targetZ: -0.30,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%): Glide East Through Living Portal Arch & Balcony Sliders Open
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.52,
    posZ: -0.30,
    targetX: 1.45,
    targetY: 1.45,
    targetZ: -1.95,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A3 (86% to 89%): Step Through Open Sliding Door Onto Teak Balcony Deck (Y = 1.55m)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 6B (89% to 92%): Balcony Deck Steady Hold (Expansive Skyline View)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    sweepBalconyZ: -2.35,
    posX: 1.45,
    posY: 1.55,
    posZ: -1.95,
    targetX: 1.55,
    targetY: 1.50,
    targetZ: -7.50,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'none'
});

// --- STOP 7: 92% to 100% (MUMBAI GOLDEN SUNSET FINALE & PITCH CLOSING) ---'''

content = old_timeline_pattern.sub(new_timeline_code, content, count=1)

# 4. Update solid material handling in render() and applyProgressToScene()
old_solid_block = '''    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        const solidMats = [
            pbrWarmPlasterWall, pbrWildMushroom, pbrScandinavianOak, pbrBlackQuartz,
            pbrCalacattaFloor, pbrMarbleTable, pbrCeilingMat, pbrMDFSkirting, pbrTravertineTile,
            pbrBoucleLinen, pbrTerracotta, pbrMustard, pbrBrushedBrass, pbrMatteBlackSteel,
            pbrPolishedChrome, pbrBrushedSteel, pbrCeramicMat, pbrCurtainLinen, pbrSlateTile
        ];
        solidMats.forEach(m => {
            if (m) {
                m.transparent = false;
                m.opacity = 1.0;
                m.depthWrite = true;
                m.depthTest = true;
                m.side = THREE.FrontSide;
            }
        });
    }'''

new_solid_block = '''    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
        materialGroup.traverse(child => {
            if (child.isMesh && child.material) {
                const m = child.material;
                if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrGlass ||
                    m === pbrCurtainSheer || m === pbrAmberGlass || (m.map && m.map.name === 'blobShadow')) {
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

content = content.replace(old_solid_block, new_solid_block)

with open(r'D:\floor plans\jp-aviva-3d\script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully applied fixes to script.js!')
