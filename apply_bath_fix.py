import re

script_path = r'D:\floor plans\jp-aviva-3d\script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define pbrShowerGlass
old_glass_def = 'const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({'
new_glass_def = '''const pbrShowerGlass = new THREE.MeshPhysicalMaterial({
    color: 0xFFFFFF,
    transmission: 0.98,
    opacity: 1.0,
    transparent: true,
    roughness: 0.02,
    metalness: 0.0,
    ior: 1.50,
    thickness: 0.01,
    reflectivity: 0.08,
    clearcoat: 0.20,
    clearcoatRoughness: 0.02,
    clippingPlanes: [clipHeightPlane]
});

const pbrArchitecturalGlass = new THREE.MeshPhysicalMaterial({'''

if 'const pbrShowerGlass' not in content:
    content = content.replace(old_glass_def, new_glass_def, 1)

# 2. Add pbrShowerGlass to preserved transparent materials in both render() and applyProgressToScene()
content = content.replace(
    'mat === pbrGlass || mat === pbrBalconyGlass || \n                    mat === pbrArchitecturalGlass || mat === pbrSheerCurtain || \n                    mat === pbrAmberGlass || mat.map === blobShadowTex',
    'mat === pbrGlass || mat === pbrBalconyGlass || \n                    mat === pbrArchitecturalGlass || mat === pbrShowerGlass || mat === pbrSheerCurtain || \n                    mat === pbrAmberGlass || mat.map === blobShadowTex'
)
content = content.replace(
    'm === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrGlass || \n                    m === pbrSheerCurtain || m === pbrAmberGlass || m.map === blobShadowTex',
    'm === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass || \n                    m === pbrSheerCurtain || m === pbrAmberGlass || m.map === blobShadowTex'
)

# 3. Replace buildBathroomSuite() function entirely with calibrated layout
old_bath_fn_regex = r'function buildBathroomSuite\(\) \{[\s\S]*?\n\}\n\n// ={10,}\n// D\. MASTER BEDROOM'
new_bath_fn = '''function buildBathroomSuite() {
    const group = new THREE.Group();

    // 1. Dark Slate Porcelain Flooring (1.15m x 1.30m)
    const bathFloorGeo = new THREE.PlaneGeometry(1.22, 1.28);
    bathFloorGeo.rotateX(-Math.PI / 2);
    const bathFloor = new THREE.Mesh(bathFloorGeo, pbrSlateTile);
    bathFloor.position.set(-1.18, 0.002, 1.00);
    bathFloor.receiveShadow = true;
    group.add(bathFloor);

    // 2. Travertine / Porcelain Tiled Wall Panels (600x1200mm Tile Grid)
    // Full-height south wet wall behind vanity, WC & mirror (z = 1.62)
    const wetWallGeo = new THREE.PlaneGeometry(1.25, WALL_H);
    const wetWallMesh = new THREE.Mesh(wetWallGeo, pbrTravertineTile);
    wetWallMesh.position.set(-1.18, WALL_H / 2, 1.615);
    wetWallMesh.receiveShadow = true;
    group.add(wetWallMesh);

    // West shower wet wall panel (x = -1.78)
    const showerWallGeo = new THREE.PlaneGeometry(1.25, WALL_H);
    showerWallGeo.rotateY(Math.PI / 2);
    const showerWallMesh = new THREE.Mesh(showerWallGeo, pbrTravertineTile);
    showerWallMesh.position.set(-1.78, WALL_H / 2, 1.00);
    showerWallMesh.receiveShadow = true;
    group.add(showerWallMesh);

    // East side wall panel (x = -0.58)
    const eastWallGeo = new THREE.PlaneGeometry(1.25, WALL_H);
    eastWallGeo.rotateY(-Math.PI / 2);
    const eastWallMesh = new THREE.Mesh(eastWallGeo, pbrTravertineTile);
    eastWallMesh.position.set(-0.58, WALL_H / 2, 1.00);
    eastWallMesh.receiveShadow = true;
    group.add(eastWallMesh);

    // -------------------------------------------------------------------------
    // 3. Compact Floating Scandinavian Oak Vanity Unit (Center-Left: X = -1.14)
    // -------------------------------------------------------------------------
    const vanityGroup = new THREE.Group();
    const vanity = new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.28, 0.32, 4, 0.02), pbrScandinavianOak);
    vanity.position.set(-1.14, 0.52, 1.44);
    vanity.castShadow = true;
    vanityGroup.add(vanity);

    // Brushed brass handle on vanity drawer
    const vHandle = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.010, 0.012, 2, 0.003), pbrBrushedBrass);
    vHandle.position.set(-1.14, 0.54, 1.27);
    vanityGroup.add(vHandle);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.10, 0.09, 32), pbrWhisperingSmoke);
    basin.position.set(-1.14, 0.70, 1.43);
    basin.castShadow = true;
    vanityGroup.add(basin);

    // Sleek Curved Matte-Black Mixer Tap (TubeGeometry with graceful arch & side lever)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.017, 0.012, 20), pbrMatteBlackSteel);
    tapBase.position.set(-1.14, 0.66, 1.54);
    tapGroup.add(tapBase);

    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.11, 0),
        new THREE.Vector3(0, 0.16, -0.02),
        new THREE.Vector3(0, 0.18, -0.06),
        new THREE.Vector3(0, 0.16, -0.10),
        new THREE.Vector3(0, 0.12, -0.11)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.005, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(-1.14, 0.664, 1.54);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.005, 0.012, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(-1.14, 0.784, 1.43);
    tapGroup.add(tapNozzle);

    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.018, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(-1.12, 0.72, 1.54);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.002, 0.002, 0.050, 12), pbrMatteBlackSteel);
    pinLever.position.set(-1.13, 0.745, 1.54);
    pinLever.rotation.z = -0.40;
    tapGroup.add(pinLever);
    vanityGroup.add(tapGroup);

    // Circular Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm LED Halo (#FFE4B5)
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.23, 0.23, 0.008, 64), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.01,
        metalness: 0.99,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.14, 1.34, 1.59);
    vanityGroup.add(mirrorGlass);

    const brassFrameGeo = new THREE.TorusGeometry(0.233, 0.005, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(-1.14, 1.34, 1.585);
    vanityGroup.add(brassFrameMesh);

    const haloRingGeo = new THREE.TorusGeometry(0.245, 0.010, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(-1.14, 1.34, 1.605);
    vanityGroup.add(haloRingMesh);

    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.2, 2.0, 1.8);
    haloWallLight.position.set(-1.14, 1.34, 1.605);
    vanityGroup.add(haloWallLight);

    // Designer Vanity Accessories
    const dispBottle = new THREE.Mesh(new RoundedBoxGeometry(0.045, 0.075, 0.045, 4, 0.010), pbrAmberGlass);
    dispBottle.position.set(-1.27, 0.70, 1.38);
    dispBottle.castShadow = true;
    vanityGroup.add(dispBottle);

    const towelBottom = new THREE.Mesh(new RoundedBoxGeometry(0.11, 0.026, 0.14, 6, 0.012), pbrBoucleLinen);
    towelBottom.position.set(-1.01, 0.675, 1.38);
    towelBottom.castShadow = true;
    vanityGroup.add(towelBottom);

    const towelTop = new THREE.Mesh(new RoundedBoxGeometry(0.10, 0.022, 0.12, 6, 0.012), pbrWhisperingSmoke);
    towelTop.position.set(-1.01, 0.700, 1.38);
    towelTop.rotation.y = 0.08;
    towelTop.castShadow = true;
    vanityGroup.add(towelTop);

    createBlobShadow(0.44, 0.38, -1.14, 1.44, vanityGroup, 0.40);
    group.add(vanityGroup);

    // -------------------------------------------------------------------------
    // 4. Modern Wall-Hung Ceramic WC (Commode) with Concealed Dual-Flush Plate (East: X = -0.74)
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const toiletBowl = new THREE.Mesh(new RoundedBoxGeometry(0.30, 0.28, 0.42, 6, 0.04), pbrWhisperingSmoke);
    toiletBowl.position.set(-0.74, 0.38, 1.36);
    toiletBowl.castShadow = true;
    toiletGroup.add(toiletBowl);

    const toiletLid = new THREE.Mesh(new RoundedBoxGeometry(0.29, 0.020, 0.41, 4, 0.02), pbrWhisperingSmoke);
    toiletLid.position.set(-0.74, 0.53, 1.36);
    toiletGroup.add(toiletLid);

    // Concealed dual-flush plate on south wall
    const flushPlate = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.11, 0.010, 4, 0.003), pbrPolishedChrome);
    flushPlate.position.set(-0.74, 0.98, 1.61);
    toiletGroup.add(flushPlate);

    // Dual circular buttons
    const btnLeft = new THREE.Mesh(new THREE.CylinderGeometry(0.020, 0.020, 0.004, 20), pbrBrushedSteel);
    btnLeft.rotation.x = Math.PI / 2;
    btnLeft.position.set(-0.77, 0.98, 1.615);
    toiletGroup.add(btnLeft);

    const btnRight = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.004, 20), pbrBrushedSteel);
    btnRight.rotation.x = Math.PI / 2;
    btnRight.position.set(-0.71, 0.98, 1.615);
    toiletGroup.add(btnRight);

    createBlobShadow(0.38, 0.48, -0.74, 1.36, toiletGroup, 0.36);
    group.add(toiletGroup);

    // -------------------------------------------------------------------------
    // 5. Walk-in Frameless Tempered Glass Shower Screen & Rain Shower (West: X = -1.40)
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();
    // 10mm Crystal Clear Tempered Glass Screen running along Z from z = 0.825 to 1.475
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.010, 2.05, 0.65), pbrShowerGlass);
    showerGlass.position.set(-1.40, 1.03, 1.15);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Slim floor track in matte black steel
    const floorChannel = new THREE.Mesh(new THREE.BoxGeometry(0.020, 0.020, 0.65), pbrMatteBlackSteel);
    floorChannel.position.set(-1.40, 0.010, 1.15);
    showerGroup.add(floorChannel);

    // Top horizontal stabilizing support bar anchored from west wall (x = -1.78) to glass (x = -1.40)
    const supportBar = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.38, 12), pbrMatteBlackSteel);
    supportBar.rotation.z = Math.PI / 2;
    supportBar.position.set(-1.59, 2.02, 1.15);
    showerGroup.add(supportBar);

    // 220mm Matte-Black Overhead Rain Showerhead
    const rainPlate = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.012, 32), pbrMatteBlackSteel);
    rainPlate.position.set(-1.59, 2.10, 1.20);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.19, 16), pbrMatteBlackSteel);
    showerArm.rotation.z = Math.PI / 2;
    showerArm.position.set(-1.685, 2.13, 1.20);
    showerGroup.add(showerArm);

    // Matte-Black Thermostatic Valve & Handset Diverter on West wall
    const thermoKnob = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.025, 16), pbrMatteBlackSteel);
    thermoKnob.rotation.z = Math.PI / 2;
    thermoKnob.position.set(-1.765, 1.05, 1.20);
    showerGroup.add(thermoKnob);

    const handWand = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.18, 12), pbrMatteBlackSteel);
    handWand.position.set(-1.75, 1.15, 1.05);
    showerGroup.add(handWand);

    // Linear floor drain channel in slate tile
    const drainMesh = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.004, 0.40), pbrBrushedSteel);
    drainMesh.position.set(-1.59, 0.004, 0.95);
    showerGroup.add(drainMesh);

    group.add(showerGroup);

    // Overhead Bathroom Suite Ceiling Downlight
    const bathDownlight = new THREE.PointLight(0xFFF2DC, 1.2, 3.0, 1.8);
    bathDownlight.position.set(-1.14, 2.75, 1.05);
    group.add(bathDownlight);

    materialGroup.add(group);
}

// ============================================================================
// D. MASTER BEDROOM'''

content = re.sub(old_bath_fn_regex, new_bath_fn, content)

# 4. Update Stop 4 Camera Spline in timeline (Leg 4A1, Leg 4A2, Leg 4B, Leg 5A1)
old_stop4_regex = r'// --- STOP 4: 52% to 65%[\s\S]*?// --- STOP 5: 65% to 80% \(Smooth Circulation into Master Bedroom Suite\) ---\n// Leg 5A1 \(65% to 68%\): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West\ntl\.to\(camState, \{[\s\S]*?targetZ: -0\.20,\n    duration: 0\.03,\n    ease: \'power2\.inOut\'\n\}\);'

new_stop4 = '''// --- STOP 4: 52% to 65% (05 - BATH & W.C. 1.15M x 1.30M Doorway Framing) ---
// Leg 4A1 (52% to 56%): Glide South out of Kitchen Portal into Central Passage Hub directly facing Bathroom doorway
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -1.05,
    posY: 1.50,
    posZ: -0.10,
    targetX: -1.14,
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
    posX: -1.08,
    posY: 1.48,
    posZ: 0.30,
    targetX: -1.14,
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
    posX: -1.08,
    posY: 1.48,
    posZ: 0.30,
    targetX: -1.14,
    targetY: 1.10,
    targetZ: 1.45,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth Circulation into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%): Glide North Cleanly out of Bathroom Doorway into Passage Hub, Turning West
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -1.08,
    posY: 1.50,
    posZ: -0.15,
    targetX: -2.40,
    targetY: 1.30,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});'''

content = re.sub(old_stop4_regex, new_stop4, content)

# 5. Update stage label in updateUI()
content = content.replace(
    "else if (p < 0.66) labelElem.textContent = '05 · Designer Bath Suite (1.15m × 1.30m)';",
    "else if (p < 0.66) labelElem.textContent = '05 · BATH & W.C. (1.15M x 1.30M)';"
)

# 6. Update ROOM_SPECS[4]
old_room_spec = '''    4: {
        zone: "Zone 03 · Wellness & Hygiene Suite",
        name: "Designer Bathroom & W.C.",
        subtitle: "Wing A · Separate Bath & Toilet Enclaves",
        dimsM: "1.15 × 1.30 M + 1.00 × 1.30 M",
        dimsF: "3'9\\" × 4'3\\" + 3'3\\" × 4'3\\" FT",
        areaM: "3.08 SQ.M. Total Area",
        areaF: "33.2 SQ.FT. Total Area",'''

new_room_spec = '''    4: {
        zone: "Zone 03 · Wellness & Hygiene Suite",
        name: "BATH & W.C. (1.15M x 1.30M)",
        subtitle: "Wing A · Integrated Bath & W.C. Suite",
        dimsM: "1.15 × 1.30 M",
        dimsF: "3'9\\" × 4'3\\" FT",
        areaM: "1.50 SQ.M. Carpet",
        areaF: "16.1 SQ.FT. Carpet",'''

content = content.replace(old_room_spec, new_room_spec)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied bath refinements successfully!")
