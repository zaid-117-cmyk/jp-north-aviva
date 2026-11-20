import re

SCRIPT_PATH = r"D:\floor plans\jp-aviva-3d\script.js"

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update buildBathroomSuite
new_bathroom_suite = """function buildBathroomSuite() {
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
    // 3. Compact Floating Scandinavian Oak Vanity Unit (Center-Left: X = -1.22)
    // -------------------------------------------------------------------------
    const vanityGroup = new THREE.Group();
    const vanity = new THREE.Mesh(new RoundedBoxGeometry(0.44, 0.32, 0.38, 4, 0.02), pbrScandinavianOak);
    vanity.position.set(-1.22, 0.54, 1.41);
    vanity.castShadow = true;
    vanityGroup.add(vanity);

    // Brushed steel handle on vanity drawer
    const vHandle = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.010, 0.012, 2, 0.003), pbrBrushedSteel);
    vHandle.position.set(-1.22, 0.56, 1.21);
    vanityGroup.add(vHandle);

    // White Ceramic Vessel Basin
    const basin = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.11, 0.10, 24), pbrWhisperingSmoke);
    basin.position.set(-1.22, 0.75, 1.40);
    basin.castShadow = true;
    vanityGroup.add(basin);

    // Sleek Curved Matte-Black Mixer Tap (TubeGeometry with graceful arch & side lever)
    const tapGroup = new THREE.Group();
    const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.018, 0.012, 20), pbrMatteBlackSteel);
    tapBase.position.set(-1.22, 0.702, 1.51);
    tapGroup.add(tapBase);

    const tapCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(0, 0.12, 0),
        new THREE.Vector3(0, 0.18, -0.02),
        new THREE.Vector3(0, 0.20, -0.06),
        new THREE.Vector3(0, 0.18, -0.10),
        new THREE.Vector3(0, 0.14, -0.11)
    ]);
    const tapGeo = new THREE.TubeGeometry(tapCurve, 32, 0.0055, 16, false);
    const tapMesh = new THREE.Mesh(tapGeo, pbrMatteBlackSteel);
    tapMesh.position.set(-1.22, 0.706, 1.51);
    tapMesh.castShadow = true;
    tapGroup.add(tapMesh);

    const tapNozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.006, 0.014, 16), pbrMatteBlackSteel);
    tapNozzle.position.set(-1.22, 0.844, 1.40);
    tapGroup.add(tapNozzle);

    const valveStem = new THREE.Mesh(new THREE.CylinderGeometry(0.005, 0.005, 0.020, 12), pbrMatteBlackSteel);
    valveStem.rotation.z = Math.PI / 2;
    valveStem.position.set(-1.20, 0.76, 1.51);
    tapGroup.add(valveStem);

    const pinLever = new THREE.Mesh(new THREE.CylinderGeometry(0.0025, 0.0025, 0.055, 12), pbrMatteBlackSteel);
    pinLever.position.set(-1.21, 0.785, 1.51);
    pinLever.rotation.z = -0.40;
    tapGroup.add(pinLever);
    vanityGroup.add(tapGroup);

    // Circular Backlit Mirror with Thin Brushed-Brass Frame & Soft Warm LED Halo (#FFE4B5)
    const mirrorGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.008, 64), new THREE.MeshPhysicalMaterial({
        color: 0xFFFFFF,
        roughness: 0.01,
        metalness: 0.99,
        clearcoat: 1.0,
        clippingPlanes: [clipHeightPlane]
    }));
    mirrorGlass.rotation.x = Math.PI / 2;
    mirrorGlass.position.set(-1.22, 1.38, 1.58);
    vanityGroup.add(mirrorGlass);

    const brassFrameGeo = new THREE.TorusGeometry(0.253, 0.005, 16, 64);
    const brassFrameMesh = new THREE.Mesh(brassFrameGeo, pbrBrushedBrass);
    brassFrameMesh.position.set(-1.22, 1.38, 1.575);
    vanityGroup.add(brassFrameMesh);

    const haloRingGeo = new THREE.TorusGeometry(0.268, 0.012, 16, 64);
    const haloRingMat = new THREE.MeshBasicMaterial({
        color: 0xFFE4B5,
        clippingPlanes: [clipHeightPlane]
    });
    const haloRingMesh = new THREE.Mesh(haloRingGeo, haloRingMat);
    haloRingMesh.position.set(-1.22, 1.38, 1.595);
    vanityGroup.add(haloRingMesh);

    const haloWallLight = new THREE.PointLight(0xFFE4B5, 1.4, 2.2, 1.8);
    haloWallLight.position.set(-1.22, 1.38, 1.595);
    vanityGroup.add(haloWallLight);

    // Designer Vanity Accessories
    const dispBottle = new THREE.Mesh(new RoundedBoxGeometry(0.048, 0.080, 0.048, 4, 0.010), pbrAmberGlass);
    dispBottle.position.set(-1.38, 0.74, 1.35);
    dispBottle.castShadow = true;
    vanityGroup.add(dispBottle);

    const towelBottom = new THREE.Mesh(new RoundedBoxGeometry(0.12, 0.030, 0.15, 6, 0.012), pbrBoucleLinen);
    towelBottom.position.set(-1.05, 0.715, 1.35);
    towelBottom.castShadow = true;
    vanityGroup.add(towelBottom);

    const towelTop = new THREE.Mesh(new RoundedBoxGeometry(0.11, 0.026, 0.13, 6, 0.012), pbrWhisperingSmoke);
    towelTop.position.set(-1.05, 0.743, 1.35);
    towelTop.rotation.y = 0.08;
    towelTop.castShadow = true;
    vanityGroup.add(towelTop);

    createBlobShadow(0.50, 0.45, -1.22, 1.41, vanityGroup, 0.40);
    group.add(vanityGroup);

    // -------------------------------------------------------------------------
    // 4. Modern Wall-Hung Ceramic WC (Commode) with Concealed Dual-Flush Plate (East: X = -0.78)
    // -------------------------------------------------------------------------
    const toiletGroup = new THREE.Group();
    const toiletBowl = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.32, 0.46, 4, 0.04), pbrWhisperingSmoke);
    toiletBowl.position.set(-0.78, 0.40, 1.35);
    toiletBowl.castShadow = true;
    toiletGroup.add(toiletBowl);

    const toiletLid = new THREE.Mesh(new RoundedBoxGeometry(0.33, 0.022, 0.45, 4, 0.02), pbrWhisperingSmoke);
    toiletLid.position.set(-0.78, 0.57, 1.35);
    toiletGroup.add(toiletLid);

    const flushPlate = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.12, 0.012, 2, 0.004), pbrPolishedChrome);
    flushPlate.position.set(-0.78, 1.05, 1.61);
    toiletGroup.add(flushPlate);

    createBlobShadow(0.42, 0.55, -0.78, 1.35, toiletGroup, 0.38);
    group.add(toiletGroup);

    // -------------------------------------------------------------------------
    // 5. Walk-in Frameless Tempered Glass Shower Partition & Rain Shower (West: X = -1.50)
    // -------------------------------------------------------------------------
    const showerGroup = new THREE.Group();
    // 10mm Architectural Glass Screen running along Z from z = 0.55 to 1.15
    const showerGlass = new THREE.Mesh(new THREE.BoxGeometry(0.010, 2.05, 0.60), pbrArchitecturalGlass);
    showerGlass.position.set(-1.50, 1.03, 0.85);
    showerGlass.castShadow = true;
    showerGroup.add(showerGlass);

    // Floor and wall U-channel tracks in matte black steel
    const glassChannel = new THREE.Mesh(new THREE.BoxGeometry(0.022, 2.05, 0.022), pbrMatteBlackSteel);
    glassChannel.position.set(-1.50, 1.03, 1.14);
    showerGroup.add(glassChannel);

    const floorChannel = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.022, 0.60), pbrMatteBlackSteel);
    floorChannel.position.set(-1.50, 0.011, 0.85);
    showerGroup.add(floorChannel);

    // Top horizontal stabilizing support bar anchored to west wall
    const supportBar = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.28, 12), pbrMatteBlackSteel);
    supportBar.rotation.z = Math.PI / 2;
    supportBar.position.set(-1.64, 2.02, 0.85);
    showerGroup.add(supportBar);

    // 220mm Matte-Black Overhead Rain Showerhead
    const rainPlate = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, 0.012, 32), pbrMatteBlackSteel);
    rainPlate.position.set(-1.64, 2.22, 0.75);
    rainPlate.castShadow = true;
    showerGroup.add(rainPlate);

    const showerArm = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.14, 16), pbrMatteBlackSteel);
    showerArm.rotation.z = Math.PI / 2;
    showerArm.position.set(-1.71, 2.25, 0.75);
    showerGroup.add(showerArm);

    // Matte-Black Thermostatic Valve & Handset Diverter
    const thermoKnob = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, 0.030, 16), pbrMatteBlackSteel);
    thermoKnob.rotation.z = Math.PI / 2;
    thermoKnob.position.set(-1.76, 1.05, 0.75);
    showerGroup.add(thermoKnob);

    const handWand = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.18, 12), pbrMatteBlackSteel);
    handWand.position.set(-1.75, 1.18, 0.62);
    showerGroup.add(handWand);

    // Linear floor drain channel in slate tile
    const drainMesh = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.004, 0.40), pbrBrushedSteel);
    drainMesh.position.set(-1.64, 0.004, 0.75);
    showerGroup.add(drainMesh);

    group.add(showerGroup);

    // Overhead Bathroom Suite Ceiling Downlight
    const bathDownlight = new THREE.PointLight(0xFFF2DC, 1.2, 3.0, 1.8);
    bathDownlight.position.set(-1.18, 2.75, 1.00);
    group.add(bathDownlight);

    materialGroup.add(group);
}"""

# Replace old buildBathroomSuite
pattern = r"function buildBathroomSuite\(\) \{[\s\S]*?materialGroup\.add\(group\);\s*\}"
content = re.sub(pattern, new_bathroom_suite, content)

# 2. Update Wall definitions for Bathroom:
# North wall and east wall of bathroom
old_wc_wall = "addWall(0.12, WALL_H, 1.40, -0.65, WALL_H / 2, 1.00);"
new_wc_wall = "addWall(0.12, WALL_H, 1.30, -0.58, WALL_H / 2, 0.98); // Bathroom East Wall (Enclosing 1.15m x 1.30m Bath & W.C.)"
content = content.replace(old_wc_wall, new_wc_wall)

old_bath_door = """// 4. Bathroom Doorway & North Wall (z = 0.35)
// West solid segment next to bedroom wall (x = -1.85 to -1.55)
addWall(0.30, WALL_H, 0.15, -1.70, WALL_H / 2, 0.35);
// Bathroom Door Lintel overhead (y = 2.10m to 2.85m, x = -1.55 to -0.75)
addWall(0.80, 0.75, 0.15, -1.15, WALL_H - 0.375, 0.35);
// NOTE: Space from y = 0.0 to 2.10m between x = -1.55 and -0.75 is OPEN!"""

new_bath_door = """// 4. Bathroom Doorway & North Wall (z = 0.35)
// West solid segment next to bedroom wall (x = -1.85 to -1.50)
addWall(0.35, WALL_H, 0.15, -1.675, WALL_H / 2, 0.35);
// Bathroom Door Lintel overhead (y = 2.10m to 2.85m, x = -1.50 to -0.65)
addWall(0.85, 0.75, 0.15, -1.075, WALL_H - 0.375, 0.35);
// NOTE: Space from y = 0.0 to 2.10m between x = -1.50 and -0.65 is OPEN!"""

content = content.replace(old_bath_door, new_bath_door)

# 3. Update Timeline Camera Paths for Stop 4, 5, 6
timeline_old = """// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
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
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -1.95,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
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
});"""

timeline_new = """// --- STOP 4: 52% to 65% (Walk into Designer Bathroom Suite) ---
// Leg 4A1 (52% to 56%): Step South out of Kitchen into Central Passage Hub (x = -0.85, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 54.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: -1.05,
    targetY: 1.30,
    targetZ: 0.50,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 4A2 (56% to 60%): Position Camera at Bathroom Doorway (Y = 1.48m, FOV: 52, lookAt Y = 1.15m)
// Pull back & widen angle to reveal the full Bath & W.C. composition: vanity, WC, tiled walls, and shower glass!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomZ: 0.40,
    posX: -1.05,
    posY: 1.48,
    posZ: 0.15,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.25,
    duration: 0.04,
    ease: 'power2.out'
});
// Leg 4B (60% to 65%): Bathroom Suite Steady Hold (Full Architecture Composition)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 52.0,
    sweepBathroomZ: 0.40,
    posX: -1.05,
    posY: 1.48,
    posZ: 0.15,
    targetX: -1.15,
    targetY: 1.15,
    targetZ: 1.25,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 5: 65% to 80% (Smooth 'Rise, Glide, Descend' into Master Bedroom Suite) ---
// Leg 5A1 (65% to 68%) — STEP NORTH OUT OF BATHROOM INTO CENTRAL PASSAGE HUB:
// Camera glides cleanly back into central passage intersection (x = -0.85, z = -0.15)
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: -1.825,
    targetY: 1.40,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 5A2 (68% to 72%) — GLIDE WEST CLEANLY THROUGH OPEN BEDROOM DOORWAY:
// Camera passes strictly through open 0.90m doorway (x = -1.825, z = -0.20) into bedroom entrance
tl.to(camState, {
    clipHeight: 2.85,
    fov: 60.0,
    sweepBedroomX: -4.15,
    posX: -2.05,
    posY: 1.48,
    posZ: -0.20,
    targetX: -2.85,
    targetY: 1.35,
    targetZ: -0.65,
    duration: 0.04,
    ease: 'power2.inOut'
});
// Leg 5A3 (72% to 75%) — SETTLE AT EYE LEVEL BEDROOM ENTRANCE:
// Eye level (Y = 1.45m) looking diagonally across the full bed, headboard, warm pendant light, and window!
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -2.05,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.03,
    ease: 'power2.out'
});
// Leg 5B (75% to 80%) — MASTER BEDROOM STEADY HOLD (Eye Level Diagonal View):
tl.to(camState, {
    clipHeight: 2.85,
    fov: 65.0,
    sweepBedroomX: -4.15,
    posX: -2.05,
    posY: 1.45,
    posZ: -0.15,
    targetX: -3.10,
    targetY: 1.25,
    targetZ: -0.85,
    duration: 0.05,
    ease: 'none'
});

// --- STOP 6: 80% to 92% (Smooth 'Rise, Glide, Descend' to Enclosed Balcony Deck & Utility) ---
// Leg 6A1 (80% to 83%) — GLIDE OUT OF BEDROOM INTO CENTRAL PASSAGE HUB:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 56.0,
    posX: -0.85,
    posY: 1.52,
    posZ: -0.15,
    targetX: 0.125,
    targetY: 1.45,
    targetZ: -0.20,
    duration: 0.03,
    ease: 'power2.inOut'
});
// Leg 6A2 (83% to 86%) — GLIDE EAST THROUGH LIVING PORTAL ARCH & BALCONY SLIDERS OPEN:
tl.to(camState, {
    clipHeight: 2.85,
    fov: 58.0,
    posX: 0.85,
    posY: 1.52,
    posZ: -0.20,
    targetX: 1.35,
    targetY: 1.38,
    targetZ: -1.80,
    balconyDoorX: -0.90,
    duration: 0.03,
    ease: 'power2.inOut'
});"""

content = content.replace(timeline_old, timeline_new)

# 4. Enforce solid opaque walls in render() and applyProgressToScene(p)
render_update_old = """    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    materialGroup.visible = (camState.clipHeight > 1.25);
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
    }"""

render_update_new = """    if (camState.progress >= 0.18) {
        clipHeightPlane.constant = 50.0;
    } else {
        clipHeightPlane.constant = camState.clipHeight;
    }
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
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
    }"""

content = content.replace(render_update_old, render_update_new)

# Also update applyProgressToScene
apply_update_old = """    tl.progress(p);
    camState.progress = p;
    clipHeightPlane.constant = camState.clipHeight;
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    materialGroup.visible = (camState.clipHeight > 1.25);
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
    }"""

apply_update_new = """    tl.progress(p);
    camState.progress = p;
    if (p >= 0.18) {
        clipHeightPlane.constant = 50.0;
    } else {
        clipHeightPlane.constant = camState.clipHeight;
    }
    livingDraftPlane.constant = camState.sweepLivingZ;
    livingMaterialPlane.constant = -camState.sweepLivingZ;
    kitchenDraftPlane.constant = camState.sweepKitchenZ;
    kitchenMaterialPlane.constant = -camState.sweepKitchenZ;
    bathroomDraftPlane.constant = camState.sweepBathroomZ;
    bathroomMaterialPlane.constant = -camState.sweepBathroomZ;
    bedroomDraftPlane.constant = camState.sweepBedroomX;
    bedroomMaterialPlane.constant = -camState.sweepBedroomX;
    balconyDraftPlane.constant = camState.sweepBalconyZ;
    balconyMaterialPlane.constant = -camState.sweepBalconyZ;
    doorPivot.rotation.y = camState.doorAngle;
    if (balconyDoorPivot) balconyDoorPivot.position.x = 1.575 + camState.balconyDoorX;

    wallGroup.visible = (camState.clipHeight <= 1.30);
    materialGroup.visible = (camState.clipHeight > 1.25);
    if (camState.clipHeight > 1.25 || camState.progress >= 0.15) {
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
    }"""

content = content.replace(apply_update_old, apply_update_new)

with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated script.js with bathroom layout and camera pathing refinements!")
