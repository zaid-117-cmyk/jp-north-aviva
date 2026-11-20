import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

# 1. Add pbrDarkTitaniumSteel and pbrSinkWater materials
old_mats = """const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({
    color: 0xDFE2E6,
    metalness: 0.92,
    roughness: 0.22,
    clippingPlanes: [clipHeightPlane]
});"""

new_mats = """const pbrBrushedSteel = new THREE.MeshPhysicalMaterial({
    color: 0xDFE2E6,
    metalness: 0.92,
    roughness: 0.22,
    clippingPlanes: [clipHeightPlane]
});

// Modern Dark Titanium / Fingerprint-Resistant Brushed Stainless Steel for Refrigerator
const pbrDarkTitaniumSteel = new THREE.MeshPhysicalMaterial({
    color: 0x22252A,
    metalness: 0.85,
    roughness: 0.25,
    clearcoat: 0.30,
    clearcoatRoughness: 0.20,
    reflectivity: 0.85,
    clippingPlanes: [clipHeightPlane],
    transparent: false,
    depthWrite: true
});

// Subtle Water Reflection Inside Undermount Sink Basin
const pbrSinkWater = new THREE.MeshPhysicalMaterial({
    color: 0x88B2C4,
    transmission: 0.88,
    opacity: 0.35,
    transparent: true,
    roughness: 0.02,
    ior: 1.333,
    clearcoat: 1.0,
    clearcoatRoughness: 0.02,
    clippingPlanes: [clipHeightPlane]
});"""

assert old_mats in c, 'old_mats not found'
c = c.replace(old_mats, new_mats)

# 2. Update enforceOpaqueMaterials with pbrSinkWater
old_enforce = """            if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass ||
                m === pbrSheerCurtain || m === pbrAmberGlass || m.isBlobShadow || child.isBlobShadow ||
                m.name === 'blobShadowMat' || (m.map && m.map.name === 'blobShadow')) {"""

new_enforce = """            if (m === pbrBalconyGlass || m === pbrArchitecturalGlass || m === pbrShowerGlass || m === pbrGlass ||
                m === pbrSheerCurtain || m === pbrAmberGlass || m === pbrSinkWater || m.isBlobShadow || child.isBlobShadow ||
                m.name === 'blobShadowMat' || (m.map && m.map.name === 'blobShadow')) {"""

assert old_enforce in c, 'old_enforce not found'
c = c.replace(old_enforce, new_enforce)

# 3. Replace buildKitchenAlcove with Complete Overhaul
kitchen_start = "// B. GOURMET KITCHEN ALCOVE (FULL APPLIANCE SUITE & REALISTIC FINISHES)"
kitchen_end = "// ============================================================================\n// C. DESIGNER BATH SUITE"

start_idx = c.find(kitchen_start)
end_idx = c.find(kitchen_end)

assert start_idx != -1, 'kitchen_start not found'
assert end_idx != -1, 'kitchen_end not found'

new_kitchen_code = """// B. GOURMET KITCHEN ALCOVE (FULL APPLIANCE SUITE & REALISTIC FINISHES)
// ============================================================================
function buildKitchenAlcove() {
    const group = new THREE.Group();

    // ------------------------------------------------------------------------
    // 1. REBUILT MODERN DOUBLE-DOOR / BOTTOM-FREEZER REFRIGERATOR (RIGHT SIDE)
    // Dimensions: Width: 0.72m, Height: 1.85m, Depth: 0.68m
    // Material: Brushed dark titanium / fingerprint-resistant stainless steel
    // ------------------------------------------------------------------------
    const fridgeGroup = new THREE.Group();
    const fridgeX = -0.38;
    const fridgeY = 0.925;
    const fridgeZ = -2.02;

    // Main Outer Carcass Casing (0.70m x 1.83m x 0.62m) with rounded corners
    const fridgeCarcass = new THREE.Mesh(
        new RoundedBoxGeometry(0.70, 1.83, 0.62, 4, 0.015),
        pbrDarkTitaniumSteel
    );
    fridgeCarcass.position.set(fridgeX, fridgeY, fridgeZ - 0.02);
    fridgeCarcass.castShadow = true;
    fridgeGroup.add(fridgeCarcass);

    // Recessed Black Toe-Kick Plinth Base
    const fridgePlinth = new THREE.Mesh(
        new THREE.BoxGeometry(0.68, 0.04, 0.12),
        pbrMatteBlackSteel
    );
    fridgePlinth.position.set(fridgeX, 0.02, fridgeZ + 0.23);
    fridgeGroup.add(fridgePlinth);

    // Double Upper French Doors (Height: 1.12m, Width: 0.342m each, Thickness: 0.038m)
    const fDoorLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.342, 1.12, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    fDoorLeft.position.set(fridgeX - 0.175, 1.27, fridgeZ + 0.305);
    fDoorLeft.castShadow = true;
    fridgeGroup.add(fDoorLeft);

    const fDoorRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.342, 1.12, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    fDoorRight.position.set(fridgeX + 0.175, 1.27, fridgeZ + 0.305);
    fDoorRight.castShadow = true;
    fridgeGroup.add(fDoorRight);

    // Crisp Center Vertical Door Reveal (8mm dark gasket line)
    const fCenterReveal = new THREE.Mesh(
        new THREE.BoxGeometry(0.008, 1.11, 0.032),
        pbrMatteBlackSteel
    );
    fCenterReveal.position.set(fridgeX, 1.27, fridgeZ + 0.30);
    fridgeGroup.add(fCenterReveal);

    // Bottom Pull-Out Freezer Drawer (Height: 0.64m, Width: 0.692m, Thickness: 0.038m)
    const freezerDrawer = new THREE.Mesh(
        new RoundedBoxGeometry(0.692, 0.64, 0.038, 4, 0.012),
        pbrDarkTitaniumSteel
    );
    freezerDrawer.position.set(fridgeX, 0.35, fridgeZ + 0.305);
    freezerDrawer.castShadow = true;
    fridgeGroup.add(freezerDrawer);

    // Crisp Horizontal Door Gap (14mm shadow gap separating upper doors from freezer drawer)
    const fHorizReveal = new THREE.Mesh(
        new THREE.BoxGeometry(0.69, 0.014, 0.034),
        pbrMatteBlackSteel
    );
    fHorizReveal.position.set(fridgeX, 0.69, fridgeZ + 0.30);
    fridgeGroup.add(fHorizReveal);

    // Vertical Recessed Brushed-Chrome Pocket Handles
    const fHandleLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.014, 0.45, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    fHandleLeft.position.set(fridgeX - 0.025, 1.15, fridgeZ + 0.32);
    fridgeGroup.add(fHandleLeft);

    const fHandleRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.014, 0.45, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    fHandleRight.position.set(fridgeX + 0.025, 1.15, fridgeZ + 0.32);
    fridgeGroup.add(fHandleRight);

    const freezerHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.014, 0.016, 2, 0.003),
        pbrPolishedChrome
    );
    freezerHandle.position.set(fridgeX, 0.66, fridgeZ + 0.32);
    fridgeGroup.add(freezerHandle);

    // Subtle Glowing Digital Temperature Display (Right Upper Door)
    const dispPanel = new THREE.Mesh(
        new THREE.PlaneGeometry(0.09, 0.045),
        pbrObsidianGlass
    );
    dispPanel.position.set(fridgeX + 0.18, 1.48, fridgeZ + 0.326);
    fridgeGroup.add(dispPanel);

    const dispLed = new THREE.Mesh(
        new THREE.PlaneGeometry(0.075, 0.024),
        new THREE.MeshBasicMaterial({ color: 0x90E0EF })
    );
    dispLed.position.set(fridgeX + 0.18, 1.48, fridgeZ + 0.327);
    fridgeGroup.add(dispLed);

    // Overhead Refrigerator Bridge Cabinet (Separated by 0.03m Shadow Gap)
    const fridgeTopCab = new THREE.Mesh(
        new THREE.BoxGeometry(0.70, 0.44, 0.62),
        pbrScandinavianOak
    );
    fridgeTopCab.position.set(fridgeX, 2.10, fridgeZ - 0.02);
    fridgeTopCab.castShadow = true;
    fridgeGroup.add(fridgeTopCab);

    // Grounded Contact Shadow Plane under Refrigerator
    createBlobShadow(0.76, 0.72, fridgeX, fridgeZ, group, 0.44);
    group.add(fridgeGroup);

    // ------------------------------------------------------------------------
    // 2. VEINED DARK QUARTZ COUNTERTOP & BASE CABINETS (LEFT RUN)
    // Spans from West Wall (x = -1.75) to Refrigerator Shadow Gap (x = -0.76)
    // ------------------------------------------------------------------------
    const counterW = 0.98;
    const counterCenterX = -1.26;
    const counterCenterZ = -2.05;

    // Dark Quartz Countertop with Chamfered Bullnose Profile
    const nCounter = new THREE.Mesh(
        new RoundedBoxGeometry(counterW, 0.045, 0.62, 4, 0.008),
        pbrBlackQuartz
    );
    nCounter.position.set(counterCenterX, 0.865, counterCenterZ);
    nCounter.castShadow = true;
    group.add(nCounter);

    const counterEdge = new THREE.Mesh(
        new THREE.BoxGeometry(counterW, 0.015, 0.012),
        pbrBlackQuartz
    );
    counterEdge.position.set(counterCenterX, 0.84, counterCenterZ + 0.31);
    group.add(counterEdge);

    // Scandinavian Oak Base Cabinets
    const nBaseCab = new THREE.Mesh(
        new THREE.BoxGeometry(counterW - 0.02, 0.84, 0.56),
        pbrScandinavianOak
    );
    nBaseCab.position.set(counterCenterX, 0.42, counterCenterZ);
    nBaseCab.castShadow = true;
    group.add(nBaseCab);

    // 2 Modular Cabinet Doors with Architectural Reveal & Brushed Steel Bar Handles
    const cabWidths = [counterCenterX - 0.24, counterCenterX + 0.24];
    for (let cx of cabWidths) {
        const doorPanel = new THREE.Mesh(
            new RoundedBoxGeometry(0.46, 0.78, 0.02, 4, 0.008),
            pbrScandinavianOak
        );
        doorPanel.position.set(cx, 0.43, counterCenterZ + 0.29);
        doorPanel.castShadow = true;
        group.add(doorPanel);

        const handleBar = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.012, 0.014, 2, 0.003),
            pbrBrushedSteel
        );
        handleBar.position.set(cx, 0.74, counterCenterZ + 0.315);
        group.add(handleBar);

        for (let so of [-0.07, 0.07]) {
            const standoff = new THREE.Mesh(
                new THREE.CylinderGeometry(0.006, 0.006, 0.018, 12),
                pbrBrushedSteel
            );
            standoff.rotation.x = Math.PI / 2;
            standoff.position.set(cx + so, 0.74, counterCenterZ + 0.30);
            group.add(standoff);
        }
    }

    // ------------------------------------------------------------------------
    // 3. GLOSSY BEVELED SUBWAY TILE BACKSPLASH & OVERHEAD CABINETS
    // ------------------------------------------------------------------------
    const splashMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(counterW, 0.76),
        new THREE.MeshPhysicalMaterial({
            map: subwayTileTex,
            roughness: 0.08,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            reflectivity: 0.90,
            clippingPlanes: [clipHeightPlane]
        })
    );
    splashMesh.position.set(counterCenterX, 1.26, -2.36);
    group.add(splashMesh);

    // Overhead Scandinavian Oak Modular Upper Cabinets
    const upperCab = new THREE.Mesh(
        new THREE.BoxGeometry(counterW, 0.72, 0.35),
        pbrScandinavianOak
    );
    upperCab.position.set(counterCenterX, 1.99, -2.18);
    upperCab.castShadow = true;
    group.add(upperCab);

    // 2 Upper Cabinet Doors with Vertical Brushed Steel Handles
    for (let ux of [counterCenterX - 0.24, counterCenterX + 0.24]) {
        const uDoor = new THREE.Mesh(
            new RoundedBoxGeometry(0.46, 0.69, 0.02, 4, 0.008),
            pbrScandinavianOak
        );
        uDoor.position.set(ux, 1.99, -2.00);
        uDoor.castShadow = true;
        group.add(uDoor);

        const uHandle = new THREE.Mesh(
            new RoundedBoxGeometry(0.012, 0.18, 0.014, 2, 0.003),
            pbrBrushedSteel
        );
        uHandle.position.set(ux + 0.18, 1.76, -1.98);
        group.add(uHandle);
    }

    // Warm Under-Cabinet LED Strip Lighting Channel (#FFE4B5)
    const ledProfile = new THREE.Mesh(
        new THREE.BoxGeometry(counterW - 0.02, 0.014, 0.025),
        pbrBrushedSteel
    );
    ledProfile.position.set(counterCenterX, 1.625, -2.18);
    group.add(ledProfile);

    const ledDiffuser = new THREE.Mesh(
        new THREE.BoxGeometry(counterW - 0.04, 0.006, 0.018),
        new THREE.MeshBasicMaterial({ color: 0xFFE4B5 })
    );
    ledDiffuser.position.set(counterCenterX, 1.616, -2.18);
    group.add(ledDiffuser);

    // 2 Warm Under-Cabinet LED Spotlights Washing Counter & Subway Tiles
    for (let lx of [counterCenterX - 0.24, counterCenterX + 0.24]) {
        const taskSpot = new THREE.PointLight(0xFFE4B5, 1.4, 2.2, 2.0);
        taskSpot.position.set(lx, 1.58, -2.12);
        group.add(taskSpot);
    }

    // ------------------------------------------------------------------------
    // 4. REALISTIC UNDERMOUNT SINK & GOOSENECK FAUCET (LEFT COUNTER)
    // ------------------------------------------------------------------------
    const sinkX = -1.45;
    const sinkY = 0.865;
    const sinkZ = -2.02;

    const sinkBasinGroup = new THREE.Group();

    // Basin Bottom Plate
    const basinBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.012, 0.32, 4, 0.015),
        pbrBrushedSteel
    );
    basinBottom.position.set(sinkX, 0.70, sinkZ);
    sinkBasinGroup.add(basinBottom);

    // Basin Walls (recessed below counter from y = 0.70m to 0.865m)
    const bWallMat = pbrBrushedSteel;
    const bWallL = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.32), bWallMat);
    bWallL.position.set(sinkX - 0.21, 0.782, sinkZ);
    sinkBasinGroup.add(bWallL);
    const bWallR = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.32), bWallMat);
    bWallR.position.set(sinkX + 0.21, 0.782, sinkZ);
    sinkBasinGroup.add(bWallR);

    const bWallB = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.165, 0.012), bWallMat);
    bWallB.position.set(sinkX, 0.782, sinkZ - 0.16);
    sinkBasinGroup.add(bWallB);
    const bWallF = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.165, 0.012), bWallMat);
    bWallF.position.set(sinkX, 0.782, sinkZ + 0.16);
    sinkBasinGroup.add(bWallF);

    // Beveled Stainless Steel Undermount Flange Rim
    const sinkRim = new THREE.Mesh(
        new RoundedBoxGeometry(0.46, 0.010, 0.36, 4, 0.008),
        pbrBrushedSteel
    );
    sinkRim.position.set(sinkX, 0.868, sinkZ);
    sinkBasinGroup.add(sinkRim);

    // Stainless Steel Drain Strainer & Waste Flange
    const drainFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(0.045, 0.045, 0.006, 24),
        pbrPolishedChrome
    );
    drainFlange.position.set(sinkX, 0.708, sinkZ);
    sinkBasinGroup.add(drainFlange);

    const drainCup = new THREE.Mesh(
        new THREE.CylinderGeometry(0.024, 0.020, 0.008, 16),
        pbrBrushedSteel
    );
    drainCup.position.set(sinkX, 0.710, sinkZ);
    sinkBasinGroup.add(drainCup);

    const drainKnob = new THREE.Mesh(
        new THREE.CylinderGeometry(0.005, 0.005, 0.012, 12),
        pbrPolishedChrome
    );
    drainKnob.position.set(sinkX, 0.718, sinkZ);
    sinkBasinGroup.add(drainKnob);

    // Subtle Water Reflection Plane Inside Basin
    const waterMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.38, 0.28),
        pbrSinkWater
    );
    waterMesh.rotation.x = -Math.PI / 2;
    waterMesh.position.set(sinkX, 0.715, sinkZ);
    sinkBasinGroup.add(waterMesh);
    group.add(sinkBasinGroup);

    // Curved Pull-Down Chrome Gooseneck Faucet (TubeGeometry)
    const faucetGroup = new THREE.Group();
    faucetGroup.position.set(sinkX, 0.875, sinkZ - 0.22);

    const escutcheon = new THREE.Mesh(
        new THREE.CylinderGeometry(0.026, 0.030, 0.022, 24),
        pbrPolishedChrome
    );
    escutcheon.position.set(0, 0.011, 0);
    faucetGroup.add(escutcheon);

    const faucetCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 0.02, 0),
        new THREE.Vector3(0, 0.22, 0),
        new THREE.Vector3(0, 0.35, 0.04),
        new THREE.Vector3(0, 0.40, 0.12),
        new THREE.Vector3(0, 0.35, 0.20),
        new THREE.Vector3(0, 0.26, 0.20)
    ]);
    const faucetGeo = new THREE.TubeGeometry(faucetCurve, 36, 0.012, 16, false);
    const faucetMesh = new THREE.Mesh(faucetGeo, pbrPolishedChrome);
    faucetMesh.castShadow = true;
    faucetGroup.add(faucetMesh);

    const nozzle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.015, 0.012, 0.035, 16),
        pbrPolishedChrome
    );
    nozzle.position.set(0, 0.245, 0.20);
    faucetGroup.add(nozzle);

    const mixerBody = new THREE.Mesh(
        new THREE.CylinderGeometry(0.012, 0.012, 0.030, 12),
        pbrPolishedChrome
    );
    mixerBody.rotation.z = Math.PI / 2;
    mixerBody.position.set(0.028, 0.08, 0);
    faucetGroup.add(mixerBody);

    const mixerLever = new THREE.Mesh(
        new THREE.CylinderGeometry(0.005, 0.005, 0.075, 12),
        pbrPolishedChrome
    );
    mixerLever.position.set(0.042, 0.11, 0);
    mixerLever.rotation.z = -0.35;
    faucetGroup.add(mixerLever);
    group.add(faucetGroup);

    // Dish Soap Pump (Mounted on Left Deck)
    const soapGroup = new THREE.Group();
    soapGroup.position.set(sinkX - 0.18, 0.875, sinkZ - 0.19);
    const soapBase = new THREE.Mesh(
        new THREE.CylinderGeometry(0.016, 0.020, 0.014, 16),
        pbrPolishedChrome
    );
    soapBase.position.set(0, 0.007, 0);
    soapGroup.add(soapBase);

    const soapPump = new THREE.Mesh(
        new THREE.CylinderGeometry(0.010, 0.010, 0.042, 16),
        pbrPolishedChrome
    );
    soapPump.position.set(0, 0.035, 0);
    soapGroup.add(soapPump);

    const soapSpout = new THREE.Mesh(
        new THREE.CylinderGeometry(0.004, 0.004, 0.055, 12),
        pbrPolishedChrome
    );
    soapSpout.rotation.x = Math.PI / 2 - 0.20;
    soapSpout.position.set(0, 0.052, 0.025);
    soapGroup.add(soapSpout);
    group.add(soapGroup);

    // ------------------------------------------------------------------------
    // 5. INDUCTION HOB & SLEEK BLACK GLASS CHIMNEY HOOD (RIGHT COUNTER RUN)
    // ------------------------------------------------------------------------
    const hobX = -0.98;
    const hobZ = -2.02;

    // Schott Ceran 2-Burner Obsidian Induction Hob
    const cooktop = new THREE.Mesh(
        new THREE.BoxGeometry(0.36, 0.012, 0.50),
        new THREE.MeshPhysicalMaterial({
            map: inductionTex,
            roughness: 0.04,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            clippingPlanes: [clipHeightPlane]
        })
    );
    cooktop.position.set(hobX, 0.89, hobZ);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle Amber Touch Control Power LED Indicator
    const cooktopLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.004, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFB300 })
    );
    cooktopLed.position.set(hobX, 0.898, hobZ + 0.22);
    group.add(cooktopLed);

    // Sleek Tempered Black Glass & Stainless Steel Wall Chimney Hood (Above Hob)
    // ZERO NEON-GREEN ARTIFACTS
    const hoodGroup = new THREE.Group();
    hoodGroup.position.set(hobX, 0, hobZ);

    const hoodDuct = new THREE.Mesh(
        new THREE.BoxGeometry(0.24, 0.68, 0.22),
        pbrBrushedSteel
    );
    hoodDuct.position.set(0, 2.01, -0.08);
    hoodDuct.castShadow = true;
    hoodGroup.add(hoodDuct);

    const glassCanopy = new THREE.Mesh(
        new RoundedBoxGeometry(0.58, 0.028, 0.44, 4, 0.008),
        pbrObsidianGlass
    );
    glassCanopy.position.set(0, 1.66, 0.0);
    glassCanopy.castShadow = true;
    hoodGroup.add(glassCanopy);

    const canopyBezel = new THREE.Mesh(
        new THREE.BoxGeometry(0.59, 0.012, 0.45),
        pbrBrushedSteel
    );
    canopyBezel.position.set(0, 1.645, 0.0);
    hoodGroup.add(canopyBezel);

    const baffleFilter = new THREE.Mesh(
        new THREE.BoxGeometry(0.48, 0.010, 0.32),
        pbrBrushedSteel
    );
    baffleFilter.position.set(0, 1.635, 0.0);
    hoodGroup.add(baffleFilter);

    for (let bx of [-0.14, 0.14]) {
        const hoodSpot = new THREE.PointLight(0xFFE4B5, 1.2, 1.8, 2.0);
        hoodSpot.position.set(bx, 1.61, 0.0);
        hoodGroup.add(hoodSpot);
    }
    group.add(hoodGroup);

    // ------------------------------------------------------------------------
    // 6. REPOSITIONED COUNTERTOP APPLIANCES & CHEF PREP ACCENTS
    // (Toaster & Espresso Machine moved neatly to the left so sink is in clear view)
    // ------------------------------------------------------------------------
    const toasterGroup = new THREE.Group();
    const toasterX = -1.68;
    const toasterZ = -1.80;

    const toasterBody = new THREE.Mesh(
        new RoundedBoxGeometry(0.13, 0.14, 0.20, 6, 0.02),
        pbrBrushedSteel
    );
    toasterBody.position.set(toasterX, 0.955, toasterZ);
    toasterBody.castShadow = true;
    toasterGroup.add(toasterBody);

    const toasterTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.125, 0.012, 0.19, 4, 0.008),
        pbrPolishedChrome
    );
    toasterTop.position.set(toasterX, 1.03, toasterZ);
    toasterGroup.add(toasterTop);

    for (let slotX of [toasterX - 0.028, toasterX + 0.028]) {
        const slot = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.022, 0.13), pbrObsidianGlass);
        slot.position.set(slotX, 1.028, toasterZ);
        toasterGroup.add(slot);
    }
    const bDial = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.010, 16), pbrPolishedChrome);
    bDial.rotation.x = Math.PI / 2;
    bDial.position.set(toasterX, 0.925, toasterZ + 0.105);
    toasterGroup.add(bDial);
    group.add(toasterGroup);

    // Italian Commercial Espresso Machine (Left Rear Corner)
    const espressoGroup = new THREE.Group();
    const espressoX = -1.68;
    const espressoZ = -2.22;

    const espressoMain = new THREE.Mesh(
        new RoundedBoxGeometry(0.18, 0.26, 0.20, 6, 0.015),
        pbrBrushedSteel
    );
    espressoMain.position.set(espressoX, 1.02, espressoZ);
    espressoMain.castShadow = true;
    espressoGroup.add(espressoMain);

    const rail = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.012, 0.18, 4, 0.004), pbrPolishedChrome);
    rail.position.set(espressoX, 1.155, espressoZ);
    espressoGroup.add(rail);

    for (let cupX of [espressoX - 0.04, espressoX + 0.04]) {
        const eCup = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.014, 0.030, 16), pbrCeramicMat);
        eCup.position.set(cupX, 1.175, espressoZ);
        espressoGroup.add(eCup);
    }

    const gauge = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.008, 16), pbrBrushedBrass);
    gauge.rotation.x = Math.PI / 2;
    gauge.position.set(espressoX, 1.08, espressoZ + 0.105);
    espressoGroup.add(gauge);

    const pfHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.10, 12), pbrMatteBlackSteel);
    pfHandle.rotation.x = Math.PI / 2 + 0.15;
    pfHandle.position.set(espressoX, 0.98, espressoZ + 0.18);
    espressoGroup.add(pfHandle);

    const dripTray = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.012, 0.10), pbrPolishedChrome);
    dripTray.position.set(espressoX, 0.895, espressoZ + 0.09);
    espressoGroup.add(dripTray);
    group.add(espressoGroup);

    // End-Grain Oak Chopping Board & Chef's Knife (Prep Zone in front of Cooktop)
    const boardGroup = new THREE.Group();
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.02, 0.20, 4, 0.008), pbrScandinavianOak);
    board.position.set(hobX, 0.898, -1.74);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.16), pbrBrushedSteel);
    knifeBlade.position.set(hobX, 0.912, -1.74);
    knifeBlade.rotation.y = 0.25;
    boardGroup.add(knifeBlade);
    group.add(boardGroup);

    // Grounded Contact Shadow Plane under Kitchen Counter Base
    createBlobShadow(counterW, 0.65, counterCenterX, counterCenterZ, group, 0.40);

    materialGroup.add(group);
}
"""

c = c[:start_idx] + new_kitchen_code + "\n" + c[end_idx:]

# 4. Refine Kitchen camera framing at Stop 3 (lines 3248 to 3274)
old_cam = """// Leg 3A3 (44% to 46%): Step North Through Kitchen Portal Opening to Presentation Framing
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
});"""

new_cam = """// Leg 3A3 (44% to 46%): Step North Through Kitchen Portal Opening to Presentation Framing
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepKitchenZ: -2.35,
    posX: -0.62,
    posY: 1.48,
    posZ: -0.60,
    targetX: -0.92,
    targetY: 1.12,
    targetZ: -2.05,
    duration: 0.02,
    ease: 'power2.out'
});
// Leg 3B (46% to 52%): Kitchen Alcove Steady Hold
tl.to(camState, {
    clipHeight: 2.85,
    fov: 64.0,
    sweepKitchenZ: -2.35,
    posX: -0.62,
    posY: 1.48,
    posZ: -0.60,
    targetX: -0.92,
    targetY: 1.12,
    targetZ: -2.05,
    duration: 0.06,
    ease: 'none'
});"""

assert old_cam in c, 'old_cam not found'
c = c.replace(old_cam, new_cam)

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully applied Kitchen Alcove Overhaul to script.js!')
