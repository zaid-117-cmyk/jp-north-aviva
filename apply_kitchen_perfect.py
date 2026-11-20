import os

path = 'D:/floor plans/jp-aviva-3d/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
c = content.replace('\r\n', '\n')

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
    // 2. VEINED DARK QUARTZ COUNTERTOP WITH UNDERMOUNT SINK CUTOUT
    // Spans from West Wall (x = -1.75) to Refrigerator Shadow Gap (x = -0.76)
    // ------------------------------------------------------------------------
    const counterY = 0.865;
    const counterThick = 0.045;

    // A. Left Counter Margin (x = -1.75 to -1.60, width: 0.15m, depth: 0.62m)
    const cLeft = new THREE.Mesh(
        new RoundedBoxGeometry(0.15, counterThick, 0.62, 4, 0.008),
        pbrBlackQuartz
    );
    cLeft.position.set(-1.675, counterY, -2.05);
    cLeft.castShadow = true;
    group.add(cLeft);

    // B. Back Counter Bridge Deck (x = -1.60 to -1.16, width: 0.44m, depth: 0.16m, z = -2.36 to -2.20)
    const cBack = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, counterThick, 0.16, 4, 0.008),
        pbrBlackQuartz
    );
    cBack.position.set(-1.38, counterY, -2.28);
    cBack.castShadow = true;
    group.add(cBack);

    // C. Front Counter Rim (x = -1.60 to -1.16, width: 0.44m, depth: 0.10m, z = -1.84 to -1.74)
    const cFront = new THREE.Mesh(
        new RoundedBoxGeometry(0.44, counterThick, 0.10, 4, 0.008),
        pbrBlackQuartz
    );
    cFront.position.set(-1.38, counterY, -1.79);
    cFront.castShadow = true;
    group.add(cFront);

    // D. Right Counter Section under Cooktop & Prep (x = -1.16 to -0.76, width: 0.40m, depth: 0.62m)
    const cRight = new THREE.Mesh(
        new RoundedBoxGeometry(0.40, counterThick, 0.62, 4, 0.008),
        pbrBlackQuartz
    );
    cRight.position.set(-0.96, counterY, -2.05);
    cRight.castShadow = true;
    group.add(cRight);

    // Front Edge Specular Light Catch Strip across full front
    const counterEdge = new THREE.Mesh(
        new THREE.BoxGeometry(0.99, 0.015, 0.012),
        pbrBlackQuartz
    );
    counterEdge.position.set(-1.255, counterY - 0.022, -1.74);
    group.add(counterEdge);

    // Scandinavian Oak Base Cabinets (Carved with recess under sink so basin is clear!)
    // Right base cabinet (under cooktop): full 0.84m height
    const nBaseCabRight = new THREE.Mesh(
        new THREE.BoxGeometry(0.46, 0.84, 0.56),
        pbrScandinavianOak
    );
    nBaseCabRight.position.set(-0.99, 0.42, -2.05);
    nBaseCabRight.castShadow = true;
    group.add(nBaseCabRight);

    // Left base cabinet (under sink): lower 0.66m height, leaving top 18cm hollow for sink basin!
    const nBaseCabLeft = new THREE.Mesh(
        new THREE.BoxGeometry(0.51, 0.66, 0.56),
        pbrScandinavianOak
    );
    nBaseCabLeft.position.set(-1.495, 0.33, -2.05);
    nBaseCabLeft.castShadow = true;
    group.add(nBaseCabLeft);

    // 2 Modular Cabinet Doors with Architectural Reveal & Brushed Steel Bar Handles
    const cabWidths = [-1.50, -1.02];
    for (let cx of cabWidths) {
        const doorPanel = new THREE.Mesh(
            new RoundedBoxGeometry(0.46, 0.78, 0.02, 4, 0.008),
            pbrScandinavianOak
        );
        doorPanel.position.set(cx, 0.43, -1.76);
        doorPanel.castShadow = true;
        group.add(doorPanel);

        const handleBar = new THREE.Mesh(
            new RoundedBoxGeometry(0.18, 0.012, 0.014, 2, 0.003),
            pbrBrushedSteel
        );
        handleBar.position.set(cx, 0.74, -1.735);
        group.add(handleBar);

        for (let so of [-0.07, 0.07]) {
            const standoff = new THREE.Mesh(
                new THREE.CylinderGeometry(0.006, 0.006, 0.018, 12),
                pbrBrushedSteel
            );
            standoff.rotation.x = Math.PI / 2;
            standoff.position.set(cx + so, 0.74, -1.75);
            group.add(standoff);
        }
    }

    // ------------------------------------------------------------------------
    // 3. GLOSSY BEVELED SUBWAY TILE BACKSPLASH & OVERHEAD CABINETS
    // ------------------------------------------------------------------------
    // Full-height subway tile backsplash washing behind counter and chimney hood
    const splashMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(1.01, 1.15),
        new THREE.MeshPhysicalMaterial({
            map: subwayTileTex,
            roughness: 0.08,
            clearcoat: 1.0,
            clearcoatRoughness: 0.04,
            reflectivity: 0.90,
            clippingPlanes: [clipHeightPlane]
        })
    );
    splashMesh.position.set(-1.255, 1.45, -2.36);
    group.add(splashMesh);

    // Left Overhead Modular Cabinet (Above sink/prep, x = -1.75 to -1.26, width: 0.49m)
    const upperCabLeft = new THREE.Mesh(
        new THREE.BoxGeometry(0.49, 0.72, 0.35),
        pbrScandinavianOak
    );
    upperCabLeft.position.set(-1.505, 1.99, -2.18);
    upperCabLeft.castShadow = true;
    group.add(upperCabLeft);

    const uDoor = new THREE.Mesh(
        new RoundedBoxGeometry(0.47, 0.69, 0.02, 4, 0.008),
        pbrScandinavianOak
    );
    uDoor.position.set(-1.505, 1.99, -2.00);
    uDoor.castShadow = true;
    group.add(uDoor);

    const uHandle = new THREE.Mesh(
        new RoundedBoxGeometry(0.012, 0.18, 0.014, 2, 0.003),
        pbrBrushedSteel
    );
    uHandle.position.set(-1.325, 1.76, -1.98);
    group.add(uHandle);

    // Warm Under-Cabinet LED Strip Lighting Channel (#FFE4B5)
    const ledProfile = new THREE.Mesh(
        new THREE.BoxGeometry(0.47, 0.014, 0.025),
        pbrBrushedSteel
    );
    ledProfile.position.set(-1.505, 1.625, -2.18);
    group.add(ledProfile);

    const ledDiffuser = new THREE.Mesh(
        new THREE.BoxGeometry(0.45, 0.006, 0.018),
        new THREE.MeshBasicMaterial({ color: 0xFFE4B5 })
    );
    ledDiffuser.position.set(-1.505, 1.616, -2.18);
    group.add(ledDiffuser);

    // Warm Under-Cabinet LED Spotlight
    const taskSpot = new THREE.PointLight(0xFFE4B5, 1.5, 2.2, 2.0);
    taskSpot.position.set(-1.505, 1.58, -2.12);
    group.add(taskSpot);

    // ------------------------------------------------------------------------
    // 4. REALISTIC UNDERMOUNT SINK & GOOSENECK FAUCET (LEFT COUNTER)
    // ------------------------------------------------------------------------
    const sinkX = -1.38;
    const sinkZ = -2.02;

    const sinkBasinGroup = new THREE.Group();

    // High-finish Brushed Stainless Steel Sink Material
    const pbrSinkBasinMat = new THREE.MeshPhysicalMaterial({
        color: 0xC8CDD2,
        metalness: 0.90,
        roughness: 0.18,
        clearcoat: 0.40,
        clearcoatRoughness: 0.15,
        reflectivity: 0.90,
        clippingPlanes: [clipHeightPlane]
    });

    // Basin Bottom Plate (recessed at y = 0.70m, 16.5cm below quartz deck)
    const basinBottom = new THREE.Mesh(
        new RoundedBoxGeometry(0.42, 0.012, 0.34, 4, 0.015),
        pbrSinkBasinMat
    );
    basinBottom.position.set(sinkX, 0.70, sinkZ);
    sinkBasinGroup.add(basinBottom);

    // Basin Side Walls (recessed below counter from y = 0.70m to 0.865m)
    const bWallL = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.34), pbrSinkBasinMat);
    bWallL.position.set(sinkX - 0.21, 0.782, sinkZ);
    sinkBasinGroup.add(bWallL);
    const bWallR = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.165, 0.34), pbrSinkBasinMat);
    bWallR.position.set(sinkX + 0.21, 0.782, sinkZ);
    sinkBasinGroup.add(bWallR);

    const bWallB = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.165, 0.012), pbrSinkBasinMat);
    bWallB.position.set(sinkX, 0.782, sinkZ - 0.17);
    sinkBasinGroup.add(bWallB);
    const bWallF = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.165, 0.012), pbrSinkBasinMat);
    bWallF.position.set(sinkX, 0.782, sinkZ + 0.17);
    sinkBasinGroup.add(bWallF);

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
        new THREE.PlaneGeometry(0.40, 0.32),
        pbrSinkWater
    );
    waterMesh.rotation.x = -Math.PI / 2;
    waterMesh.position.set(sinkX, 0.715, sinkZ);
    sinkBasinGroup.add(waterMesh);
    group.add(sinkBasinGroup);

    // Curved Pull-Down Chrome Gooseneck Faucet (TubeGeometry)
    const faucetGroup = new THREE.Group();
    faucetGroup.position.set(sinkX, counterY + 0.01, -2.26);

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
    soapGroup.position.set(sinkX - 0.18, counterY + 0.01, -2.25);
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
    const hobX = -0.96;
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
    cooktop.position.set(hobX, counterY + 0.025, hobZ);
    cooktop.castShadow = true;
    group.add(cooktop);

    // Subtle Amber Touch Control Power LED Indicator
    const cooktopLed = new THREE.Mesh(
        new THREE.SphereGeometry(0.004, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFB300 })
    );
    cooktopLed.position.set(hobX, counterY + 0.033, hobZ + 0.22);
    group.add(cooktopLed);

    // Sleek Tempered Black Glass & Stainless Steel Wall Chimney Hood (Above Hob)
    // ZERO NEON-GREEN ARTIFACTS
    const hoodGroup = new THREE.Group();
    hoodGroup.position.set(hobX, 0, hobZ);

    const hoodDuct = new THREE.Mesh(
        new THREE.BoxGeometry(0.24, 0.70, 0.22),
        pbrBrushedSteel
    );
    hoodDuct.position.set(0, 2.02, -0.08);
    hoodDuct.castShadow = true;
    hoodGroup.add(hoodDuct);

    const glassCanopy = new THREE.Mesh(
        new RoundedBoxGeometry(0.50, 0.028, 0.44, 4, 0.008),
        pbrObsidianGlass
    );
    glassCanopy.position.set(0, 1.66, 0.0);
    glassCanopy.castShadow = true;
    hoodGroup.add(glassCanopy);

    const canopyBezel = new THREE.Mesh(
        new THREE.BoxGeometry(0.51, 0.012, 0.45),
        pbrBrushedSteel
    );
    canopyBezel.position.set(0, 1.645, 0.0);
    hoodGroup.add(canopyBezel);

    const baffleFilter = new THREE.Mesh(
        new THREE.BoxGeometry(0.42, 0.010, 0.32),
        pbrBrushedSteel
    );
    baffleFilter.position.set(0, 1.635, 0.0);
    hoodGroup.add(baffleFilter);

    for (let bx of [-0.14, 0.14]) {
        const hoodSpot = new THREE.PointLight(0xFFE4B5, 1.3, 1.8, 2.0);
        hoodSpot.position.set(bx, 1.61, 0.0);
        hoodGroup.add(hoodSpot);
    }
    group.add(hoodGroup);

    // ------------------------------------------------------------------------
    // 6. REPOSITIONED COUNTERTOP APPLIANCES & CHEF PREP ACCENTS
    // (Toaster & Espresso Machine moved neatly to the left margin so sink is in clear view)
    // ------------------------------------------------------------------------
    const toasterGroup = new THREE.Group();
    const toasterX = -1.68;
    const toasterZ = -1.82;

    const toasterBody = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.14, 0.18, 6, 0.02),
        pbrBrushedSteel
    );
    toasterBody.position.set(toasterX, counterY + 0.09, toasterZ);
    toasterBody.castShadow = true;
    toasterGroup.add(toasterBody);

    const toasterTop = new THREE.Mesh(
        new RoundedBoxGeometry(0.115, 0.012, 0.17, 4, 0.008),
        pbrPolishedChrome
    );
    toasterTop.position.set(toasterX, counterY + 0.165, toasterZ);
    toasterGroup.add(toasterTop);

    for (let slotX of [toasterX - 0.025, toasterX + 0.025]) {
        const slot = new THREE.Mesh(new THREE.BoxGeometry(0.014, 0.022, 0.12), pbrObsidianGlass);
        slot.position.set(slotX, counterY + 0.163, toasterZ);
        toasterGroup.add(slot);
    }
    const bDial = new THREE.Mesh(new THREE.CylinderGeometry(0.010, 0.010, 0.010, 16), pbrPolishedChrome);
    bDial.rotation.x = Math.PI / 2;
    bDial.position.set(toasterX, counterY + 0.06, toasterZ + 0.095);
    toasterGroup.add(bDial);
    group.add(toasterGroup);

    // Italian Commercial Espresso Machine (Left Rear Corner against West Wall)
    const espressoGroup = new THREE.Group();
    const espressoX = -1.68;
    const espressoZ = -2.24;

    const espressoMain = new THREE.Mesh(
        new RoundedBoxGeometry(0.12, 0.26, 0.18, 6, 0.015),
        pbrBrushedSteel
    );
    espressoMain.position.set(espressoX, counterY + 0.15, espressoZ);
    espressoMain.castShadow = true;
    espressoGroup.add(espressoMain);

    const rail = new THREE.Mesh(new RoundedBoxGeometry(0.11, 0.012, 0.16, 4, 0.004), pbrPolishedChrome);
    rail.position.set(espressoX, counterY + 0.285, espressoZ);
    espressoGroup.add(rail);

    for (let cupZ of [espressoZ - 0.04, espressoZ + 0.04]) {
        const eCup = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.012, 0.028, 16), pbrCeramicMat);
        eCup.position.set(espressoX, counterY + 0.305, cupZ);
        espressoGroup.add(eCup);
    }

    const gauge = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.008, 16), pbrBrushedBrass);
    gauge.rotation.x = Math.PI / 2;
    gauge.position.set(espressoX, counterY + 0.21, espressoZ + 0.095);
    espressoGroup.add(gauge);

    const pfHandle = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, 0.09, 12), pbrMatteBlackSteel);
    pfHandle.rotation.x = Math.PI / 2 + 0.15;
    pfHandle.position.set(espressoX, counterY + 0.11, espressoZ + 0.15);
    espressoGroup.add(pfHandle);

    const dripTray = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.012, 0.08), pbrPolishedChrome);
    dripTray.position.set(espressoX, counterY + 0.028, espressoZ + 0.08);
    espressoGroup.add(dripTray);
    group.add(espressoGroup);

    // End-Grain Oak Chopping Board & Chef's Knife (Prep Zone in front of Cooktop)
    const boardGroup = new THREE.Group();
    const board = new THREE.Mesh(new RoundedBoxGeometry(0.24, 0.02, 0.20, 4, 0.008), pbrScandinavianOak);
    board.position.set(hobX, counterY + 0.033, -1.74);
    board.castShadow = true;
    boardGroup.add(board);

    const knifeBlade = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.002, 0.16), pbrBrushedSteel);
    knifeBlade.position.set(hobX, counterY + 0.047, -1.74);
    knifeBlade.rotation.y = 0.25;
    boardGroup.add(knifeBlade);
    group.add(boardGroup);

    // Grounded Contact Shadow Plane under Kitchen Counter Base
    createBlobShadow(0.99, 0.65, -1.255, -2.05, group, 0.40);

    materialGroup.add(group);
}
"""

c = c[:start_idx] + new_kitchen_code + "\n" + c[end_idx:]

if is_crlf:
    c = c.replace('\n', '\r\n')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully applied perfect Kitchen Alcove Overhaul to script.js!')
